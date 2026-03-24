from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.presentation.api.dependencies import get_db, get_notification_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/dispatch")
def dispatch_notifications(
    db: Session = Depends(get_db),
):
    service = get_notification_service(db)
    sent_count = service.dispatch_pending_notifications()

    return {"sent_count": sent_count}