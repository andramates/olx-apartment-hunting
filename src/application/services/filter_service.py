from src.application.ports.filter_repository import FilterRepository
from src.application.ports.user_repository import UserRepository
from src.domain.entities.search_filter import SearchFilter


class FilterService:
    def __init__(
        self,
        filter_repository: FilterRepository,
        user_repository: UserRepository,
    ):
        self.filter_repository = filter_repository
        self.user_repository = user_repository

    def create_filter(
        self,
        user_id: int,
        name: str,
        olx_url: str,
        check_interval_minutes: int = 5,
    ) -> SearchFilter:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        search_filter = SearchFilter(
            id=None,
            user_id=user_id,
            name=name,
            olx_url=olx_url,
            is_active=True,
            check_interval_minutes=check_interval_minutes,
        )
        return self.filter_repository.add(search_filter)

    def list_user_filters(self, user_id: int) -> list[SearchFilter]:
        return self.filter_repository.list_by_user(user_id)

    def deactivate_filter(self, filter_id: int) -> SearchFilter:
        search_filter = self.filter_repository.get_by_id(filter_id)
        if search_filter is None:
            raise ValueError("Filter not found")

        search_filter.is_active = False
        return self.filter_repository.update(search_filter)

    def activate_filter(self, filter_id: int) -> SearchFilter:
        search_filter = self.filter_repository.get_by_id(filter_id)
        if search_filter is None:
            raise ValueError("Filter not found")

        search_filter.is_active = True
        return self.filter_repository.update(search_filter)