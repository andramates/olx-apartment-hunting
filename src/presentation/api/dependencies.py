from collections.abc import Generator

from src.application.services.filter_service import FilterService
from src.application.services.user_service import UserService
from src.infrastructure.db.repositories.postgres_filter_repository import (
    PostgresFilterRepository,
)
from src.infrastructure.db.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from src.infrastructure.db.session import SessionLocal

from src.application.services.listing_monitor_service import ListingMonitorService
from src.infrastructure.db.repositories.postgres_filter_match_repository import (
    PostgresFilterMatchRepository,
)
from src.infrastructure.db.repositories.postgres_listing_repository import (
    PostgresListingRepository,
)
from src.infrastructure.scraping.olx_scraper import OlxScraper

from src.application.services.notification_service import NotificationService
from src.infrastructure.db.repositories.postgres_notification_repository import (
    PostgresNotificationRepository,
)
from src.infrastructure.notifications.smtp_email_sender import SmtpEmailSender
from src.infrastructure.db.repositories.postgres_listing_repository import (
    PostgresListingRepository,
)


def get_db() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_user_service(db) -> UserService:
    user_repository = PostgresUserRepository(db)
    return UserService(user_repository)


def get_filter_service(db) -> FilterService:
    user_repository = PostgresUserRepository(db)
    filter_repository = PostgresFilterRepository(db)
    return FilterService(filter_repository, user_repository)

def get_listing_monitor_service(db) -> ListingMonitorService:
    filter_repository = PostgresFilterRepository(db)
    listing_repository = PostgresListingRepository(db)
    filter_match_repository = PostgresFilterMatchRepository(db)
    listing_scraper = OlxScraper()
    notification_repository = PostgresNotificationRepository(db)
    user_repository = PostgresUserRepository(db)

    return ListingMonitorService(
        filter_repository=filter_repository,
        listing_repository=listing_repository,
        filter_match_repository=filter_match_repository,
        listing_scraper=listing_scraper,
        notification_repository=notification_repository,
        user_repository=user_repository,
    )

def get_notification_service(db) -> NotificationService:
    notification_repository = PostgresNotificationRepository(db)
    user_repository = PostgresUserRepository(db)
    listing_repository = PostgresListingRepository(db)
    email_sender = SmtpEmailSender()

    return NotificationService(
        notification_repository=notification_repository,
        user_repository=user_repository,
        listing_repository=listing_repository,
        email_sender=email_sender,
    )