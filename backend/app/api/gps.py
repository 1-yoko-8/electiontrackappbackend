from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.models.gps_ping import GPSPing
from app.core.deps import get_current_user
from app.schemas.gps import LocationPingRequest

router = APIRouter()


@router.post("/location-ping")
def location_ping(
    data: LocationPingRequest,
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    ping = GPSPing(
        userId=data.user_id,
        timestamp=data.timestamp,
        latitude=data.latitude,
        longitude=data.longitude,
        currentTask=data.currentTask
    )

    session.add(ping)
    session.commit()

    print(f"PING STORED: {ping.userId} | {ping.latitude}, {ping.longitude}")

    return {"status": "ok"}