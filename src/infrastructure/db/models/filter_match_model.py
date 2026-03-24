from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.base import Base


class FilterMatchModel(Base):
    __tablename__ = "filter_matches"
    __table_args__ = (
        UniqueConstraint("filter_id", "listing_id", name="uq_filter_listing"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    filter_id: Mapped[int] = mapped_column(ForeignKey("search_filters.id"), nullable=False)
    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"), nullable=False)
    matched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )