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

    @abstractmethod
    def mark_many_sent(self, notification_ids: list[int]) -> None:
        pass

    @abstractmethod
    def mark_many_failed(self, notification_ids: list[int], error: str) -> None:
        pass