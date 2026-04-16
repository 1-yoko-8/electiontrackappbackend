from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

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
    try:
        # 🚫 basic validation
        if data.latitude == 0.0 and data.longitude == 0.0:
            raise HTTPException(status_code=400, detail="Invalid location")

        # 🔍 check if user already has a row
        existing = session.exec(
            select(GPSPing).where(GPSPing.userId == data.userId)
        ).first()

        if existing:
            # ✅ UPDATE
            existing.timestamp = data.timestamp
            existing.latitude = data.latitude
            existing.longitude = data.longitude
            existing.currentTask = data.currentTask

            print(f"UPDATED: {data.userId}")

        else:
            # ✅ INSERT
            new_ping = GPSPing(
                userId=data.userId,
                timestamp=data.timestamp,
                latitude=data.latitude,
                longitude=data.longitude,
                currentTask=data.currentTask
            )
            session.add(new_ping)

            print(f"CREATED: {data.userId}")

        session.commit()

        return {"status": "ok"}

    except Exception as e:
        session.rollback()
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Failed to process ping")