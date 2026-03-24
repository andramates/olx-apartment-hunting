from dataclasses import dataclass
from datetime import datetime


@dataclass
class FilterMatch:
    id: int | None
    filter_id: int
    listing_id: int
    matched_at: datetime | None = None