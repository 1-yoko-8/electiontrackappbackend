from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class RefreshToken(SQLModel, table=True):       # table name - refreshtoken - lowercase of class name
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    token_hash: str = Field(unique=True)
    expires_at: datetime
    revoked: bool = False