from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.application.ports.notification_repository import NotificationRepository
from src.domain.entities.notification import Notification
from src.infrastructure.db.models.notification_model import NotificationModel


class PostgresNotificationRepository(NotificationRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, notification: Notification) -> Notification:
        notification_model = NotificationModel(
            user_id=notification.user_id,
            filter_id=notification.filter_id,
            listing_id=notification.listing_id,
            channel=notification.channel,
            status=notification.status,
            attempts=notification.attempts,
            last_error=notification.last_error,
        )
        self.session.add(notification_model)
        self.session.commit()
        self.session.refresh(notification_model)

        return Notification(
            id=notification_model.id,
            user_id=notification_model.user_id,
            filter_id=notification_model.filter_id,
            listing_id=notification_model.listing_id,
            channel=notification_model.channel,
            status=notification_model.status,
            attempts=notification_model.attempts,
            last_error=notification_model.last_error,
            created_at=notification_model.created_at,
            sent_at=notification_model.sent_at,
        )

    def list_pending(self) -> list[Notification]:
        notification_models = (
            self.session.query(NotificationModel)
            .filter(NotificationModel.status == "pending")
            .all()
        )

        return [
            Notification(
                id=model.id,
                user_id=model.user_id,
                filter_id=model.filter_id,
                listing_id=model.listing_id,
                channel=model.channel,
                status=model.status,
                attempts=model.attempts,
                last_error=model.last_error,
                created_at=model.created_at,
                sent_at=model.sent_at,
            )
            for model in notification_models
        ]

    def mark_sent(self, notification_id: int) -> None:
        notification_model = self.session.get(NotificationModel, notification_id)
        if notification_model is None:
            return

        notification_model.status = "sent"
        notification_model.sent_at = datetime.now(timezone.utc)
        self.session.commit()

    def mark_failed(self, notification_id: int, error: str) -> None:
        notification_model = self.session.get(NotificationModel, notification_id)
        if notification_model is None:
            return

        notification_model.status = "failed"
        notification_model.attempts += 1
        notification_model.last_error = error[:1000]
        self.session.commit()