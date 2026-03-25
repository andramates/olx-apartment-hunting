from abc import ABC, abstractmethod

from src.domain.entities.listing import Listing


class ListingRepository(ABC):
    @abstractmethod
    def add(self, listing: Listing) -> Listing:
        pass

    @abstractmethod
    def get_by_external_id(self, external_id: str) -> Listing | None:
        pass

    @abstractmethod
    def get_by_id(self, listing_id: int) -> Listing | None:
        pass

    @abstractmethod
    def list_all(self) -> list[Listing]:
        pass