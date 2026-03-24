from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchFilter:
    id: int | None
    user_id: int
    name: str
    olx_url: str
    is_active: bool = True
    check_interval_minutes: int = 5
    created_at: datetime | None = None