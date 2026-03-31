import logging

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

logger = logging.getLogger(__name__)


def run_active_filters_job() -> None:
    logger.info("run_active_filters_job started")

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
        logger.info("found %s active filters", len(active_filters))

        for search_filter in active_filters:
            try:
                new_matches = monitor_service.run_filter_check(search_filter.id)
                logger.info(
                    "filter_id=%s name=%s new_matches=%s",
                    search_filter.id,
                    search_filter.name,
                    new_matches,
                )
            except Exception as exc:
                logger.exception(
                    "run_active_filters_job failed for filter_id=%s error=%s",
                    search_filter.id,
                    exc,
                )

    finally:
        session.close()
        logger.info("run_active_filters_job finished")


def dispatch_notifications_job() -> None:
    logger.info("dispatch_notifications_job started")

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

        sent_count = notification_service.dispatch_pending_notifications()
        logger.info("dispatch_notifications_job sent_count=%s", sent_count)

    finally:
        session.close()
        logger.info("dispatch_notifications_job finished")