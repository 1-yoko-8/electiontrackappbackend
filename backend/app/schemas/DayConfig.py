from pydantic import BaseModel
from datetime import date

class DayConfigResponse(BaseModel):
    allowedDays: date