from src.application.ports.email_sender import EmailSender
from src.application.ports.notification_repository import NotificationRepository
from src.application.ports.user_repository import UserRepository
from src.application.ports.listing_repository import ListingRepository


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
        sent_count = 0

        for notification in pending_notifications:
            try:
                user = self.user_repository.get_by_id(notification.user_id)
                if user is None:
                    raise ValueError("User not found")

                listing = None
                for item in self.listing_repository.list_all():
                    if item.id == notification.listing_id:
                        listing = item
                        break

                if listing is None:
                    raise ValueError("Listing not found")

                subject = f"Anunț nou OLX: {listing.title}"
                body = f"{listing.title}\n\n{listing.url}"

                self.email_sender.send(
                    to_email=user.email,
                    subject=subject,
                    body=body,
                )

                self.notification_repository.mark_sent(notification.id)
                sent_count += 1

            except Exception as exc:
                self.notification_repository.mark_failed(notification.id, str(exc))

        return sent_count