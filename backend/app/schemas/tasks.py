from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class TaskEventRequest(BaseModel):
    username: str
    taskName: str
    timestamp: datetime
    latitude: float
    longitude: float
    location: Optional[str] = None

    @field_validator("timestamp")
    def ensure_timezone(cls, v):
        if v.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware")
        return v