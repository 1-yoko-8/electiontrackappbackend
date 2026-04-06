from pydantic import BaseModel
from datetime import datetime

class LocationPingRequest(BaseModel):
    userId: str           # username
    timestamp: datetime
    latitude: float
    longitude: float
    currentTask: str