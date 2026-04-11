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

    @field_validator("timestamp", mode="before")
    def convert_to_ist_naive(cls, v):
        # 🔹 Step 1: Convert string → datetime (important)
        if isinstance(v, str):
            v = datetime.fromisoformat(v)

        # 🔹 Step 2: Ensure timezone exists
        if v.tzinfo is None:
            raise ValueError("Timestamp must be timezone-aware")

        # 🔹 Step 3: Convert to IST
        v = v.astimezone(ZoneInfo("Asia/Kolkata"))

        # 🔹 Step 4: Remove timezone (store as plain IST)
        return v.replace(tzinfo=None)