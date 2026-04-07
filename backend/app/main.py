from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.gps_ping import GPSPing
from app.models.task_event import TaskEvent
from app.models.pollingstation import PollingStation
from app.models.DayConfig import DayConfig
from sqlmodel import SQLModel
from app.db.session import engine

from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.tasks import router as task_router
from app.api.gps import router as gps_router
from app.api.dayconfig import router as dayconfig_router
from app.api.polling_station import router as polling_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine, checkfirst=True)
    print("Tables created")
    yield

app = FastAPI(title="Field Worker Tracking API", lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://electiontrackapp.onrender.com", # app backend public ip
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(profile_router, tags=["profile"])
app.include_router(task_router, tags=["tasks"])
app.include_router(gps_router, tags=["gps"])
app.include_router(dayconfig_router, tags=["dayconfig"])
app.include_router(polling_router, tags=["pollingstation"])