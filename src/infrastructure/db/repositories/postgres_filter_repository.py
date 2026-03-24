from sqlalchemy.orm import Session

from src.application.ports.filter_repository import FilterRepository
from src.domain.entities.search_filter import SearchFilter
from src.infrastructure.db.models.search_filter_model import SearchFilterModel


class PostgresFilterRepository(FilterRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, search_filter: SearchFilter) -> SearchFilter:
        filter_model = SearchFilterModel(
            user_id=search_filter.user_id,
            name=search_filter.name,
            olx_url=search_filter.olx_url,
            is_active=search_filter.is_active,
            check_interval_minutes=search_filter.check_interval_minutes,
        )
        self.session.add(filter_model)
        self.session.commit()
        self.session.refresh(filter_model)

        return SearchFilter(
            id=filter_model.id,
            user_id=filter_model.user_id,
            name=filter_model.name,
            olx_url=filter_model.olx_url,
            is_active=filter_model.is_active,
            check_interval_minutes=filter_model.check_interval_minutes,
            created_at=filter_model.created_at,
        )

    def get_by_id(self, filter_id: int) -> SearchFilter | None:
        filter_model = self.session.get(SearchFilterModel, filter_id)
        if filter_model is None:
            return None

        return SearchFilter(
            id=filter_model.id,
            user_id=filter_model.user_id,
            name=filter_model.name,
            olx_url=filter_model.olx_url,
            is_active=filter_model.is_active,
            check_interval_minutes=filter_model.check_interval_minutes,
            created_at=filter_model.created_at,
        )

    def list_by_user(self, user_id: int) -> list[SearchFilter]:
        filter_models = (
            self.session.query(SearchFilterModel)
            .filter(SearchFilterModel.user_id == user_id)
            .all()
        )

        return [
            SearchFilter(
                id=filter_model.id,
                user_id=filter_model.user_id,
                name=filter_model.name,
                olx_url=filter_model.olx_url,
                is_active=filter_model.is_active,
                check_interval_minutes=filter_model.check_interval_minutes,
                created_at=filter_model.created_at,
            )
            for filter_model in filter_models
        ]

    def list_active(self) -> list[SearchFilter]:
        filter_models = (
            self.session.query(SearchFilterModel)
            .filter(SearchFilterModel.is_active.is_(True))
            .all()
        )

        return [
            SearchFilter(
                id=filter_model.id,
                user_id=filter_model.user_id,
                name=filter_model.name,
                olx_url=filter_model.olx_url,
                is_active=filter_model.is_active,
                check_interval_minutes=filter_model.check_interval_minutes,
                created_at=filter_model.created_at,
            )
            for filter_model in filter_models
        ]

    def update(self, search_filter: SearchFilter) -> SearchFilter:
        filter_model = self.session.get(SearchFilterModel, search_filter.id)
        if filter_model is None:
            raise ValueError("Filter not found")

        filter_model.name = search_filter.name
        filter_model.olx_url = search_filter.olx_url
        filter_model.is_active = search_filter.is_active
        filter_model.check_interval_minutes = search_filter.check_interval_minutes

        self.session.commit()
        self.session.refresh(filter_model)

        return SearchFilter(
            id=filter_model.id,
            user_id=filter_model.user_id,
            name=filter_model.name,
            olx_url=filter_model.olx_url,
            is_active=filter_model.is_active,
            check_interval_minutes=filter_model.check_interval_minutes,
            created_at=filter_model.created_at,
        )