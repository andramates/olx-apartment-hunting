from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.config.settings import get_settings
from src.infrastructure.scheduling.scheduler import configure_scheduler, scheduler
from src.presentation.api.routers.filters_router import router as filters_router
from src.presentation.api.routers.notifications_router import router as notifications_router
from src.presentation.api.routers.users_router import router as users_router
from src.shared.utils.logger import setup_logging

settings = get_settings()
setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_scheduler()
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown(wait=False)


app = FastAPI(title=settings.app_name, lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(users_router)
app.include_router(filters_router)
app.include_router(notifications_router)