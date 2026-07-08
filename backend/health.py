"""Infrastructure health endpoints."""

from fastapi import APIRouter, Request

from backend.version import get_application_version
from config.settings import Settings

router = APIRouter(tags=["health"])


def _base_metadata(settings: Settings) -> dict[str, str]:
    """Return public service metadata."""

    return {
        "application": settings.application.app_name,
        "environment": settings.application.app_env.value,
        "version": get_application_version(),
    }


@router.get("/")
async def root(request: Request) -> dict[str, str]:
    """Return basic service metadata."""

    settings: Settings = request.app.state.settings
    metadata = _base_metadata(settings)
    metadata["status"] = "ok"
    return metadata


@router.get("/health")
async def health(request: Request) -> dict[str, str]:
    """Return aggregate infrastructure health metadata."""

    settings: Settings = request.app.state.settings
    metadata = _base_metadata(settings)
    metadata["status"] = "ok"
    return metadata


@router.get("/health/live")
async def liveness() -> dict[str, str]:
    """Return liveness status without dependency checks."""

    return {"status": "alive"}


@router.get("/health/ready")
async def readiness(request: Request) -> dict[str, str]:
    """Return readiness status for initialized backend infrastructure."""

    ready = all(
        hasattr(request.app.state, attribute)
        for attribute in ("settings", "document_repository", "workflow_builder")
    )
    return {"status": "ready" if ready else "not_ready"}


@router.get("/version")
async def version_info(request: Request) -> dict[str, str]:
    """Return public version metadata."""

    settings: Settings = request.app.state.settings
    return _base_metadata(settings)
