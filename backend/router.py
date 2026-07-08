"""Backend API router registration."""

from fastapi import APIRouter

from backend.health import router as health_router


def create_application_router() -> APIRouter:
    """Create the root backend router."""

    router = APIRouter()
    router.include_router(health_router)
    return router
