from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # checks token, expiry, signature - if anything wrong, JWTError
        user_id = int(payload.get("sub"))

        if payload.get("type") != "access":
            raise HTTPException(status_code=401)

        return user_id

    except JWTError:
        raise HTTPException(status_code=401)