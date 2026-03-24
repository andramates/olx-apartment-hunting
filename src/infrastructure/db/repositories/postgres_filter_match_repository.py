from sqlalchemy.orm import Session

from src.application.ports.filter_match_repository import FilterMatchRepository
from src.domain.entities.filter_match import FilterMatch
from src.infrastructure.db.models.filter_match_model import FilterMatchModel


class PostgresFilterMatchRepository(FilterMatchRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, filter_match: FilterMatch) -> FilterMatch:
        filter_match_model = FilterMatchModel(
            filter_id=filter_match.filter_id,
            listing_id=filter_match.listing_id,
        )
        self.session.add(filter_match_model)
        self.session.commit()
        self.session.refresh(filter_match_model)

        return FilterMatch(
            id=filter_match_model.id,
            filter_id=filter_match_model.filter_id,
            listing_id=filter_match_model.listing_id,
            matched_at=filter_match_model.matched_at,
        )

    def exists(self, filter_id: int, listing_id: int) -> bool:
        filter_match_model = (
            self.session.query(FilterMatchModel)
            .filter(
                FilterMatchModel.filter_id == filter_id,
                FilterMatchModel.listing_id == listing_id,
            )
            .first()
        )
        return filter_match_model is not None