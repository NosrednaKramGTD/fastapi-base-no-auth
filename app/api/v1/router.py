"""API v1 router configuration."""

from fastapi import APIRouter

from app.api.v1.endpoints import health, htmx, items

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(htmx.router, prefix="/htmx", tags=["htmx"])
