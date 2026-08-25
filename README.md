# Election Track App — Backend

A FastAPI backend for tracking field workers (e.g. police personnel) responsible for collecting and handing over ballot boxes on election day. It authenticates workers, records their GPS location and task progress in real time, and rolls that activity up into a daily report per worker.

## Problem it solves

On election day, coordinators need a live picture of where ballot-collection teams are and what stage they're at—collecting the ballot box or handing it back over—without relying on phone calls or manual paperwork.

This API gives a mobile client a single place to:

- Authenticate workers
- Log GPS pings
- Record task events
- Retrieve assigned polling stations
- Access active election-day configuration
- Generate daily worker activity reports

## Key features

- **JWT authentication** — Login with username/password, short-lived access tokens, longer-lived refresh tokens stored server-side, and refresh-token revocation on password change.
- **GPS tracking** — Endpoint for a mobile client to push periodic location pings tied to a user and their current task.
- **Task event logging** — Records when a worker collects or hands over a ballot box and automatically creates or updates a per-worker daily `Report` row.
- **Polling station lookup** — Returns the polling stations assigned to a given worker.
- **Day configuration** — Exposes the list of dates when the app should be active, such as election and training days.
- **User profile** — Returns the logged-in worker's details, including name, rank, station, and contact number.

## Tech stack

- **FastAPI** — Web framework
- **SQLModel** — ORM and data models built on SQLAlchemy and Pydantic
- **PostgreSQL** — Database, built and tested against a Supabase-hosted instance
- **python-jose** — JWT creation and verification
- **passlib (bcrypt)** — Password hashing
- **Gunicorn + Uvicorn workers** — Production ASGI serving
- **Docker + Docker Compose + Nginx** — Containerized deployment with Nginx as a reverse proxy

## How it works

1. A worker logs in using `POST /auth/login` with a username and password and receives an access token and refresh token. The refresh token is persisted in the `refreshtoken` table so it can be revoked.
2. The access token is sent as a Bearer token on subsequent requests and verified per request in `app/core/deps.py`.
3. The mobile client periodically posts GPS coordinates to `POST /location-ping`, which are stored as `GPSPing` rows.
4. When a worker completes a step—collecting or handing over a ballot box—the client posts a task event to `POST /task-event`. The API finds or creates that worker's `Report` for the day and updates the relevant status and timestamp.
5. Supporting endpoints such as `/profile`, `/pollingstation`, and `/dayconfig` return the reference data required by the mobile client.
6. On startup, the app creates any missing database tables using `SQLModel.metadata.create_all()`.

## Project structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/                       # Route handlers
│   │   │   ├── auth.py                # Login, refresh, change password
│   │   │   ├── profile.py             # GET /profile
│   │   │   ├── tasks.py               # POST /task-event + daily report logic
│   │   │   ├── gps.py                 # POST /location-ping
│   │   │   ├── dayconfig.py           # GET /dayconfig
│   │   │   └── polling_station.py     # GET /pollingstation
│   │   ├── core/
│   │   │   ├── security.py            # Password hashing and JWT creation
│   │   │   └── deps.py                # Current-user authentication dependency
│   │   ├── db/
│   │   │   └── session.py             # Database engine and session dependency
│   │   ├── models/                    # SQLModel table definitions
│   │   ├── schemas/                   # Request and response models
│   │   ├── config.py                  # Environment configuration
│   │   └── main.py                    # FastAPI app, routers, CORS, startup
│   ├── Dockerfile
│   ├── nginx.conf
│   └── requirements.txt
├── docker-compose.yml
└── .env.example
