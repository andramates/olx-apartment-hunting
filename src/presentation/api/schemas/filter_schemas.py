from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class CreateFilterRequest(BaseModel):
    user_id: int
    name: str
    olx_url: str
    check_interval_minutes: int = 5


class FilterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    olx_url: str
    is_active: bool
    check_interval_minutes: int
    created_at: datetime | None = None