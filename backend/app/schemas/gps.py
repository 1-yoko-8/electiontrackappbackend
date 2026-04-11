from pydantic import BaseModel, field_validator
from datetime import datetime
from zoneinfo import ZoneInfo

class LocationPingRequest(BaseModel):
    userId: str
    timestamp: datetime
    latitude: float
    longitude: float
    currentTask: str

    @field_validator("timestamp", mode="before")
    def convert_to_ist_naive(cls, v):
        if isinstance(v, str):
            v = datetime.fromisoformat(v)

        if v.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware")

        v = v.astimezone(ZoneInfo("Asia/Kolkata"))
        return v.replace(tzinfo=None)