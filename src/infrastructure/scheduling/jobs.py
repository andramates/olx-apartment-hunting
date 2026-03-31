from src.application.services.listing_monitor_service import ListingMonitorService
from src.application.services.notification_service import NotificationService
from src.infrastructure.db.repositories.postgres_filter_match_repository import (
    PostgresFilterMatchRepository,
)
from src.infrastructure.db.repositories.postgres_filter_repository import (
    PostgresFilterRepository,
)
from src.infrastructure.db.repositories.postgres_listing_repository import (
    PostgresListingRepository,
)
from src.infrastructure.db.repositories.postgres_notification_repository import (
    PostgresNotificationRepository,
)
from src.infrastructure.db.repositories.postgres_user_repository import (
    PostgresUserRepository,
)
from src.infrastructure.db.session import SessionLocal
from src.infrastructure.notifications.smtp_email_sender import SmtpEmailSender
from src.infrastructure.scraping.olx_scraper import OlxScraper


def run_active_filters_job() -> None:
    session = SessionLocal()
    try:
        filter_repository = PostgresFilterRepository(session)
        listing_repository = PostgresListingRepository(session)
        filter_match_repository = PostgresFilterMatchRepository(session)
        notification_repository = PostgresNotificationRepository(session)
        user_repository = PostgresUserRepository(session)
        listing_scraper = OlxScraper()

        monitor_service = ListingMonitorService(
            filter_repository=filter_repository,
            listing_repository=listing_repository,
            filter_match_repository=filter_match_repository,
            listing_scraper=listing_scraper,
            notification_repository=notification_repository,
            user_repository=user_repository,
        )

        active_filters = filter_repository.list_active()
        for search_filter in active_filters:
            try:
                monitor_service.run_filter_check(search_filter.id)
            except Exception as exc:
                print(f"[run_active_filters_job] filter_id={search_filter.id} error={exc}")

    finally:
        print("[scheduler] running active filters job")
        session.close()


def dispatch_notifications_job() -> None:
    session = SessionLocal()
    try:
        notification_repository = PostgresNotificationRepository(session)
        user_repository = PostgresUserRepository(session)
        listing_repository = PostgresListingRepository(session)
        email_sender = SmtpEmailSender()

        notification_service = NotificationService(
            notification_repository=notification_repository,
            user_repository=user_repository,
            listing_repository=listing_repository,
            email_sender=email_sender,
        )

        notification_service.dispatch_pending_notifications()

    finally:
        print("[scheduler] dispatching notifications")
        session.close()