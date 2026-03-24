from fastapi import FastAPI

from src.infrastructure.config.settings import get_settings
from src.presentation.api.routers.filters_router import router as filters_router
from src.presentation.api.routers.users_router import router as users_router
from src.presentation.api.routers.notifications_router import router as notifications_router

settings = get_settings()

app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(users_router)
app.include_router(filters_router)
app.include_router(notifications_router)