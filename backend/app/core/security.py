from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # deprecated - useful in case of change of bcrypt to argon2 later as the earlier created hashed uses bcrypt

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed):    # hashed from db
    return pwd_context.verify(password, hashed)

# Access & Refresh Tokens
def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire
    }
    token_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def create_refresh_token(user_id: int):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire
    }
    token_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt,expire

print(hash_password("password123"))