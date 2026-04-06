from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.models.task_event import TaskEvent
from app.core.deps import get_current_user
from app.schemas.tasks import TaskEventRequest

router = APIRouter()

@router.post("/task-event")
def create_task_event(
    data: TaskEventRequest,
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    event = TaskEvent(
        username=data.username,
        taskName=data.taskName,
        timestamp=data.timestamp,
        latitude=data.latitude,
        longitude=data.longitude,
        location=data.location
    )

    session.add(event)
    session.commit()
    return {"status": "ok"}