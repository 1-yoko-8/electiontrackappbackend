from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

class TaskEventRequest(BaseModel):
    username: str
    taskName: str
    timestamp: datetime
    latitude: float
    longitude: float
    location: Optional[str] = None

    @field_validator("timestamp")
    def convert_to_ist_naive(cls, v):
        if v.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware")

        # Convert to IST (safe)
        v = v.astimezone(ZoneInfo("Asia/Kolkata"))

        # Remove timezone → store as plain IST
        return v.replace(tzinfo=None)