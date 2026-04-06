from sqlmodel import SQLModel, Field

class PollingStation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    dataset_id: int
    s_no: int
    username: str = Field(index=True)
    location_name: str
    polling_areas: str | None = None
    latitude: float | None = None
    longitude: float | None = None