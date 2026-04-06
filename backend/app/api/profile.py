from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.models.user import User
from app.core.deps import get_current_user
from app.schemas.profile import ProfileResponse

router = APIRouter()

@router.get("/profile", response_model=ProfileResponse)
def get_profile(user_id: int = Depends(get_current_user), session: Session = Depends(get_session)):

    user = session.get(User, user_id)

    return {
        "userId": user.id,
        "name": user.name,
        "rank": user.rank,
        "policestation": user.policestation,
        "subdivision": user.subdivision,
        "cugphno": user.cugphno
    }