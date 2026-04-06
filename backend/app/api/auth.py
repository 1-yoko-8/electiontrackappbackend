from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, ChangePasswordRequest
from app.core.security import verify_password,hash_password,create_access_token,create_refresh_token
from app.core.deps import get_current_user
from app.models.refresh_token import RefreshToken

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, session: Session = Depends(get_session)):

    statement = select(User).where(User.username == data.username)
    user = session.exec(statement).first()

    if not user or not verify_password(data.password, user.password_hash):  # writing them in single block to prevent username enumeration
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access = create_access_token(user.id)
    refresh,expire = create_refresh_token(user.id)

    # Save to DB
    refresh_token_obj = RefreshToken(
        user_id=user.id,
        token_hash=refresh,
        expires_at=expire,
        revoked=False
    )

    try:
        session.add(refresh_token_obj)
        session.commit()
    except IntegrityError:
        session.rollback()   # ignore duplicate token insertion

    return {
        "accessToken": access,
        "refreshToken": refresh
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(token: str, session: Session = Depends(get_session)):

    statement = select(RefreshToken).where(RefreshToken.token_hash == token)
    token_obj = session.exec(statement).first()

    if not token_obj:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if token_obj.revoked:
        raise HTTPException(status_code=401, detail="Token revoked")

    if token_obj.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired")

    new_access = create_access_token(token_obj.user_id)

    return {
        "accessToken": new_access,
        "refreshToken": token
    }


@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    user = session.get(User, user_id)

    if not verify_password(data.old_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    user.password_hash = hash_password(data.new_password)

    # revoke all refresh tokens
    tokens = session.exec(
        select(RefreshToken).where(RefreshToken.user_id == user_id)
    ).all()

    for t in tokens:
        t.revoked = True

    session.commit()
    return {"message": "Password updated"}