from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime

class TaskEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    taskName: str
    timestamp: datetime = Field(
        sa_column=Column(DateTime(timezone=False), nullable=False)
    )
    latitude: float
    longitude: float
    location: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True