from abc import ABC, abstractmethod


class EmailSender(ABC):
    @abstractmethod
    def send(self, to_email: str, subject: str, body: str) -> None:
        pass