"""Backend API router registration."""

from fastapi import APIRouter

from backend.api.v1.router import router as api_v1_router
from backend.health import router as health_router


def create_application_router() -> APIRouter:
    """Create the root backend router."""

    router = APIRouter()
    router.include_router(health_router)
    router.include_router(api_v1_router)
    return router
