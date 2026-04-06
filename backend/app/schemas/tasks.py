from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskEventRequest(BaseModel):
    username: str
    taskName: str
    timestamp: datetime
    latitude: float
    longitude: float
    location: Optional[str] = None