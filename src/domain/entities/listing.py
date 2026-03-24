from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Listing:
    id: int | None
    external_id: str
    title: str
    url: str
    price: Decimal | None = None
    location: str | None = None
    first_seen_at: datetime | None = None