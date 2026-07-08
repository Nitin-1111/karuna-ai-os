"""Version 1 REST API router composition."""

from fastapi import APIRouter

from backend.api.v1.agents import router as agents_router
from backend.api.v1.documents import router as documents_router
from backend.api.v1.workflows import router as workflows_router

API_V1_PREFIX = "/api/v1"

router = APIRouter(prefix=API_V1_PREFIX)
router.include_router(agents_router)
router.include_router(workflows_router)
router.include_router(documents_router)
