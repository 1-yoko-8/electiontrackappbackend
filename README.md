# Election Track App — Backend

A FastAPI backend for tracking field workers (e.g. police personnel) responsible for
collecting and handing over ballot boxes on election day. It authenticates workers,
records their GPS location and task progress in real time, and rolls that activity
up into a daily report per worker.

## Problem it solves

On election day, coordinators need a live picture of where ballot-collection teams
are and what stage they're at (collected the ballot box vs. handed it back over),
without relying on phone calls or manual paperwork. This API gives a mobile client
a single place to authenticate, log GPS pings, log task events, and pull the
information a field worker needs for their shift (assigned polling stations,
active election days).

## Key features

- **JWT authentication** — login with username/password, short-lived access
  tokens, longer-lived refresh tokens stored server-side, and refresh-token
  revocation on password change.
- **GPS tracking** — endpoint for a mobile client to push periodic location
  pings tied to a user and their current task.
- **Task event logging** — records when a worker collects or hands over a
  ballot box; automatically creates/updates a per-worker daily `Report` row
  from those events.
- **Polling station lookup** — returns the polling stations assigned to a
  given worker.
- **Day configuration** — exposes the list of dates the app should be active
  (e.g. election day, training days).
- **User profile** — returns the logged-in worker's details (name, rank,
  station, contact number).

## Tech stack

- **FastAPI** — web framework
- **SQLModel** (SQLAlchemy + Pydantic) — ORM and data models
- **PostgreSQL** — database (built and tested against a Supabase-hosted instance)
- **python-jose** — JWT creation/verification
- **passlib (bcrypt)** — password hashing
- **Gunicorn + Uvicorn workers** — production ASGI serving
- **Docker / docker-compose + Nginx** — containerized deployment with Nginx as
  a reverse proxy in front of the API

## How it works

1. A worker logs in (`POST /auth/login`) with username/password and receives
   an access token and a refresh token. The refresh token is persisted in the
   `refreshtoken` table so it can be revoked.
2. The access token is sent as a Bearer token on subsequent requests; it's
   verified per-request in `app/core/deps.py`.
3. The mobile client periodically posts GPS coordinates
   (`POST /location-ping`), which are stored as `GPSPing` rows.
4. When a worker completes a step (collecting or handing over a ballot box),
   the client posts a task event (`POST /task-event`). The API finds or
   creates that worker's `Report` for the day and updates the relevant status
   and timestamp.
5. Supporting endpoints (`/profile`, `/pollingstation`, `/dayconfig`) return
   read-only reference data the client needs to render its UI.
6. On startup, the app creates any missing database tables from the SQLModel
   metadata (`SQLModel.metadata.create_all`).

## Project structure

```
text

backend/
├── app/
│   ├── api/                # Route handlers, one file per feature
│   │   ├── auth.py         # login, refresh, change-password
│   │   ├── profile.py      # GET /profile
│   │   ├── tasks.py        # POST /task-event (+ daily report logic)
│   │   ├── gps.py          # POST /location-ping
│   │   ├── dayconfig.py    # GET /dayconfig
│   │   └── polling_station.py  # GET /pollingstation
│   ├── core/
│   │   ├── security.py     # password hashing, JWT creation
│   │   └── deps.py         # get_current_user auth dependency
│   ├── db/
│   │   └── session.py      # SQLAlchemy engine + session dependency
│   ├── models/              # SQLModel table definitions
│   ├── schemas/              # Pydantic request/response models
│   ├── config.py            # loads and validates environment variables
│   └── main.py               # FastAPI app, routers, CORS, startup
├── Dockerfile
├── nginx.conf
└── requirements.txt
docker-compose.yml
.env.example

```

## Setup and installation

**Requirements:** Python 3.11+, a PostgreSQL database (e.g. a free
[Supabase](https://supabase.com) project).

\```bash
git clone <repo-url>
cd electiontrackappbackend

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# install dependencies
pip install -r backend/requirements.txt

# configure environment variables
cp .env.example .env
# then edit .env with your own SECRET_KEY and DATABASE_URL
\```

## Running the project

### Option 1 — locally with Uvicorn

\```bash
cd backend
uvicorn app.main:app --reload
\```

The API will be available at `http://localhost:8000`, with interactive docs
at `http://localhost:8000/docs`.

### Option 2 — with Docker

\```bash
docker-compose up --build
\```

This builds the API image, runs it behind Gunicorn/Uvicorn workers, and puts
an Nginx reverse proxy in front of it on `http://localhost:80`.

## Example usage

Log in and use the returned access token to call an authenticated endpoint:

\```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "jdoe", "password": "yourpassword"}'

# -> { "accessToken": "...", "refreshToken": "...", "token_type": "bearer" }

curl http://localhost:8000/profile \
  -H "Authorization: Bearer <accessToken>"
\```

## API endpoints

| Method | Endpoint              | Auth required | Description                                  |
|--------|------------------------|:--------------:|-----------------------------------------------|
| POST   | `/auth/login`           | No             | Log in, get access + refresh tokens           |
| POST   | `/auth/refresh`         | No             | Exchange a refresh token for a new access token |
| POST   | `/auth/change-password` | Yes            | Change password, revoke existing refresh tokens |
| GET    | `/profile`               | Yes            | Get the logged-in worker's profile            |
| POST   | `/location-ping`         | Yes            | Submit a GPS location update                  |
| POST   | `/task-event`             | Yes            | Log a ballot-box collection/hand-over event   |
| GET    | `/dayconfig`               | Yes            | List the configured active dates             |
| GET    | `/pollingstation`           | Yes            | List polling stations assigned to a username |

Full interactive documentation is auto-generated by FastAPI at `/docs` once
the server is running.
