from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.task_event import TaskEvent
from app.models.report import Report
from app.core.deps import get_current_user
from app.schemas.tasks import TaskEventRequest

router = APIRouter()


@router.post("/task-event")
def create_task_event(
    data: TaskEventRequest,
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    # ---------------- SAVE TASK EVENT ----------------
    event = TaskEvent(
        username=data.username,
        taskName=data.taskName,
        timestamp=data.timestamp,
        latitude=data.latitude,
        longitude=data.longitude,
        location=data.location
    )
    session.add(event)

    # ---------------- FETCH OR CREATE REPORT ----------------
    report = session.exec(
        select(Report).where(Report.username == data.username)
    ).first()

    if not report:
        report = Report(username=data.username)
        session.add(report)
        session.flush()

    task = data.taskName.upper()

    # ---------------- UPDATE REPORT USING EVENT TIMESTAMP ----------------

    # ---- COLLECTED ----
    if task == "COLLECTED_AND_STARTED":
        if report.ballot_box_collected_status != "Completed":
            report.ballot_box_collected_status = "Completed"
            report.collected_timestamp = data.timestamp

    # ---- HANDED OVER ----
    elif task == "REACHED_AND_HANDED_OVER":
        if report.ballot_box_handed_over_status != "Completed":
            report.ballot_box_handed_over_status = "Completed"
            report.handed_over_timestamp = data.timestamp

    # ---------------- SAVE ----------------
    session.add(report)
    session.commit()

    return {"status": "ok"}