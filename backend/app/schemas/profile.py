from pydantic import BaseModel

class ProfileResponse(BaseModel):
    userId: int
    name: str
    rank: str
    policestation: str
    subdivision: str
    cugphno: str