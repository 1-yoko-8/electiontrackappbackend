from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from datetime import date

from app.db.session import get_session
from app.core.deps import get_current_user
from app.models.DayConfig import DayConfig
from app.schemas.DayConfig import DayConfigResponse

router = APIRouter()

@router.get("/dayconfig", response_model=List[DayConfigResponse])
def get_day_config(
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Query all allowed days, sorted
    rows = session.exec(
        select(DayConfig.allowedDays).order_by(DayConfig.allowedDays)
    ).all()

    # Extract date values from rows
    days: List[date] = [row[0] if isinstance(row, tuple) else row for row in rows]

    # Wrap each date in DayConfigResponse
    response = [DayConfigResponse(allowedDays=day) for day in days]

    return response  # FastAPI automatically converts to JSON