from abc import ABC, abstractmethod

from src.domain.entities.filter_match import FilterMatch


class FilterMatchRepository(ABC):
    @abstractmethod
    def add(self, filter_match: FilterMatch) -> FilterMatch:
        pass

    @abstractmethod
    def exists(self, filter_id: int, listing_id: int) -> bool:
        pass