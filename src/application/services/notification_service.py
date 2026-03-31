import logging
from collections import defaultdict

from src.application.ports.email_sender import EmailSender
from src.application.ports.listing_repository import ListingRepository
from src.application.ports.notification_repository import NotificationRepository
from src.application.ports.user_repository import UserRepository

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(
        self,
        notification_repository: NotificationRepository,
        user_repository: UserRepository,
        listing_repository: ListingRepository,
        email_sender: EmailSender,
    ):
        self.notification_repository = notification_repository
        self.user_repository = user_repository
        self.listing_repository = listing_repository
        self.email_sender = email_sender

    def dispatch_pending_notifications(self) -> int:
        pending_notifications = self.notification_repository.list_pending()
        logger.info("pending_notifications=%s", len(pending_notifications))

        notifications_by_user: dict[int, list] = defaultdict(list)

        for notification in pending_notifications:
            notifications_by_user[notification.user_id].append(notification)

        sent_email_count = 0

        for user_id, user_notifications in notifications_by_user.items():
            notification_ids = [notification.id for notification in user_notifications]

            try:
                user = self.user_repository.get_by_id(user_id)
                if user is None:
                    raise ValueError("User not found")

                listings = []
                for notification in user_notifications:
                    listing = self.listing_repository.get_by_id(notification.listing_id)
                    if listing is not None:
                        listings.append(listing)

                if not listings:
                    raise ValueError("No listings found for pending notifications")

                subject = (
                    "Ai 1 anunț nou OLX"
                    if len(listings) == 1
                    else f"Ai {len(listings)} anunțuri noi OLX"
                )

                lines = [
                    "Au apărut anunțuri noi pentru filtrele tale:",
                    "",
                ]

                for index, listing in enumerate(listings, start=1):
                    lines.append(f"{index}. {listing.title}")
                    if listing.price is not None:
                        lines.append(f"   Preț: {listing.price}")
                    if listing.location:
                        lines.append(f"   Locație: {listing.location}")
                    lines.append(f"   Link: {listing.url}")
                    lines.append("")

                body = "\n".join(lines)

                self.email_sender.send(
                    to_email=user.email,
                    subject=subject,
                    body=body,
                )

                self.notification_repository.mark_many_sent(notification_ids)
                sent_email_count += 1

                logger.info(
                    "sent grouped email to user_id=%s listings_count=%s",
                    user_id,
                    len(listings),
                )

            except Exception as exc:
                self.notification_repository.mark_many_failed(notification_ids, str(exc))
                logger.exception(
                    "failed to send grouped email to user_id=%s error=%s",
                    user_id,
                    exc,
                )

        logger.info("dispatch_pending_notifications finished sent_email_count=%s", sent_email_count)
        return sent_email_count