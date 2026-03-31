from apscheduler.schedulers.asyncio import AsyncIOScheduler
from zoneinfo import ZoneInfo
from apscheduler.triggers.interval import IntervalTrigger

scheduler = AsyncIOScheduler(timezone=ZoneInfo("Europe/Bucharest"))

from src.infrastructure.scheduling.jobs import (
    dispatch_notifications_job,
    run_active_filters_job,
)

def configure_scheduler() -> None:
    scheduler.add_job(
        run_active_filters_job,
        trigger=IntervalTrigger(minutes=10),
        id="run_active_filters",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.add_job(
        dispatch_notifications_job,
        trigger=IntervalTrigger(hours=2),
        id="dispatch_notifications",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )