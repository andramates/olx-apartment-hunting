from abc import ABC, abstractmethod

from src.domain.entities.notification import Notification


class NotificationRepository(ABC):
    @abstractmethod
    def add(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    def list_pending(self) -> list[Notification]:
        pass

    @abstractmethod
    def mark_sent(self, notification_id: int) -> None:
        pass

    @abstractmethod
    def mark_failed(self, notification_id: int, error: str) -> None:
        pass