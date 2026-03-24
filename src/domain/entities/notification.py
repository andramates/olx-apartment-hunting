from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notification:
    id: int | None
    user_id: int
    filter_id: int
    listing_id: int
    channel: str = "email"
    status: str = "pending"
    attempts: int = 0
    last_error: str | None = None
    created_at: datetime | None = None
    sent_at: datetime | None = None