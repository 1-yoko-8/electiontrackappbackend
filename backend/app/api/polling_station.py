from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.pollingstation import PollingStation
from app.core.deps import get_current_user
from app.schemas.polling_station import PollingStationResponse

router = APIRouter()

@router.get("/pollingstation", response_model=PollingStationResponse)
def get_polling_stations(
    username: str = Query(..., description="Username to fetch polling stations for"),
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    statement = select(PollingStation).where(PollingStation.username == username)
    results = session.exec(statement).all()

    if not results:
        raise HTTPException(status_code=404, detail="No polling stations found for this username")

    locations = [station.location_name for station in results]

    return PollingStationResponse(locations=locations)