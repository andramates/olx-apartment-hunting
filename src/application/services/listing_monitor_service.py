from src.application.ports.filter_match_repository import FilterMatchRepository
from src.application.ports.filter_repository import FilterRepository
from src.application.ports.listing_repository import ListingRepository
from src.application.ports.listing_scraper import ListingScraper
from src.application.ports.notification_repository import NotificationRepository
from src.application.ports.user_repository import UserRepository
from src.domain.entities.filter_match import FilterMatch
from src.domain.entities.notification import Notification


class ListingMonitorService:
    def __init__(
        self,
        filter_repository: FilterRepository,
        listing_repository: ListingRepository,
        filter_match_repository: FilterMatchRepository,
        listing_scraper: ListingScraper,
        notification_repository: NotificationRepository,
        user_repository: UserRepository,
    ):
        self.filter_repository = filter_repository
        self.listing_repository = listing_repository
        self.filter_match_repository = filter_match_repository
        self.listing_scraper = listing_scraper
        self.notification_repository = notification_repository
        self.user_repository = user_repository

    def run_filter_check(self, filter_id: int) -> int:
        search_filter = self.filter_repository.get_by_id(filter_id)
        if search_filter is None:
            raise ValueError("Filter not found")

        if not search_filter.is_active:
            return 0

        user = self.user_repository.get_by_id(search_filter.user_id)
        if user is None:
            raise ValueError("User not found")

        scraped_listings = self.listing_scraper.fetch(search_filter.olx_url)
        new_matches_count = 0

        for scraped_listing in scraped_listings:
            existing_listing = self.listing_repository.get_by_external_id(
                scraped_listing.external_id
            )

            if existing_listing is None:
                existing_listing = self.listing_repository.add(scraped_listing)

            already_matched = self.filter_match_repository.exists(
                filter_id=search_filter.id,
                listing_id=existing_listing.id,
            )

            if already_matched:
                continue

            self.filter_match_repository.add(
                FilterMatch(
                    id=None,
                    filter_id=search_filter.id,
                    listing_id=existing_listing.id,
                )
            )

            self.notification_repository.add(
                Notification(
                    id=None,
                    user_id=user.id,
                    filter_id=search_filter.id,
                    listing_id=existing_listing.id,
                    channel="email",
                    status="pending",
                )
            )

            new_matches_count += 1

        return new_matches_count