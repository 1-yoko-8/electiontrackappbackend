from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# ---------------- CREATE ----------------
class ReportCreate(BaseModel):
    username: str
    name: Optional[str] = None
    rank: Optional[str] = None
    contact_number: Optional[str]

    polling_stations: int = Field(default=0, ge=0)
    polling_locations: int = Field(default=0, ge=0)
    ballot_boxes: int = Field(default=0, ge=0)


# ---------------- UPDATE (COLLECTED) ----------------
class ReportUpdateCollected(BaseModel):
    ballot_box_collected_status: Literal["Completed", "Not Completed"]


# ---------------- UPDATE (HANDED OVER) ----------------
class ReportUpdateHandedOver(BaseModel):
    ballot_box_handed_over_status: Literal["Completed", "Not Completed"]


# ---------------- RESPONSE ----------------
class ReportResponse(BaseModel):
    id: int

    username: str
    name: Optional[str]
    rank: Optional[str]
    contact_number: Optional[str]

    polling_stations: int
    polling_locations: int
    ballot_boxes: int

    ballot_box_collected_status: str
    collected_timestamp: Optional[datetime]

    ballot_box_handed_over_status: str
    handed_over_timestamp: Optional[datetime]

    class Config:
        from_attributes = True