from pydantic import BaseModel, field_validator
from datetime import datetime

class LocationPingRequest(BaseModel):
    userId: str
    timestamp: datetime
    latitude: float
    longitude: float
    currentTask: str

    @field_validator("timestamp")
    def ensure_timezone(cls, v):
        if v.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware")
        return v