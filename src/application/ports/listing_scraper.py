from abc import ABC, abstractmethod

from src.domain.entities.listing import Listing


class ListingScraper(ABC):
    @abstractmethod
    def fetch(self, url: str) -> list[Listing]:
        pass