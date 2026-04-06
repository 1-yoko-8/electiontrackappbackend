from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    accessToken: str
    refreshToken: str
    token_type: str = "bearer"

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str