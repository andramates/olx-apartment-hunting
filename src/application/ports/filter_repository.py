from abc import ABC, abstractmethod
from src.domain.entities.search_filter import SearchFilter


class FilterRepository(ABC):
    @abstractmethod
    def add(self, search_filter: SearchFilter) -> SearchFilter:
        pass

    @abstractmethod
    def get_by_id(self, filter_id: int) -> SearchFilter | None:
        pass

    @abstractmethod
    def list_by_user(self, user_id: int) -> list[SearchFilter]:
        pass

    @abstractmethod
    def list_active(self) -> list[SearchFilter]:
        pass

    @abstractmethod
    def update(self, search_filter: SearchFilter) -> SearchFilter:
        pass