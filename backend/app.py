"""FastAPI application factory."""

from fastapi import FastAPI

from backend.exception_handlers import register_exception_handlers
from backend.lifespan import lifespan
from backend.middleware import register_middleware
from backend.router import create_application_router
from backend.version import get_application_version
from config.settings import get_settings

APPLICATION_DESCRIPTION = "Karuna AI OS backend infrastructure."


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    settings = get_settings()
    app = FastAPI(
        title=settings.application.app_name,
        version=get_application_version(),
        description=APPLICATION_DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    register_middleware(app)
    register_exception_handlers(app)
    app.include_router(create_application_router())

    return app


app = create_app()
