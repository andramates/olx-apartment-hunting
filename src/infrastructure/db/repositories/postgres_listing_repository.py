from sqlalchemy.orm import Session

from src.application.ports.listing_repository import ListingRepository
from src.domain.entities.listing import Listing
from src.infrastructure.db.models.listing_model import ListingModel


class PostgresListingRepository(ListingRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, listing: Listing) -> Listing:
        listing_model = ListingModel(
            external_id=listing.external_id,
            title=listing.title,
            url=listing.url,
            price=listing.price,
            location=listing.location,
        )
        self.session.add(listing_model)
        self.session.commit()
        self.session.refresh(listing_model)

        return Listing(
            id=listing_model.id,
            external_id=listing_model.external_id,
            title=listing_model.title,
            url=listing_model.url,
            price=listing_model.price,
            location=listing_model.location,
            first_seen_at=listing_model.first_seen_at,
        )

    def get_by_external_id(self, external_id: str) -> Listing | None:
        listing_model = (
            self.session.query(ListingModel)
            .filter(ListingModel.external_id == external_id)
            .first()
        )
        if listing_model is None:
            return None

        return Listing(
            id=listing_model.id,
            external_id=listing_model.external_id,
            title=listing_model.title,
            url=listing_model.url,
            price=listing_model.price,
            location=listing_model.location,
            first_seen_at=listing_model.first_seen_at,
        )

    def list_all(self) -> list[Listing]:
        listing_models = self.session.query(ListingModel).all()

        return [
            Listing(
                id=listing_model.id,
                external_id=listing_model.external_id,
                title=listing_model.title,
                url=listing_model.url,
                price=listing_model.price,
                location=listing_model.location,
                first_seen_at=listing_model.first_seen_at,
            )
            for listing_model in listing_models
        ]