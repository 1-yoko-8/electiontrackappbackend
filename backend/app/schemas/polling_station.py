from pydantic import BaseModel
from typing import List

class PollingStationResponse(BaseModel):
    locations: List[str]