"""Health check endpoints."""

from datetime import datetime
from typing import Dict

import structlog
from fastapi import APIRouter

from app.core.config import settings

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    """
    Basic health check endpoint.

    Returns:
        Dict containing health status and timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.VERSION,
    }


@router.get("/ready", response_model=Dict[str, str])
async def readiness_check() -> Dict[str, str]:
    """
    Readiness check endpoint.

    This can be extended to check database connectivity, external services, etc.

    Returns:
        Dict containing readiness status
    """
    # TODO: Add database connectivity check when database is configured
    # TODO: Add external service checks as needed

    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/live", response_model=Dict[str, str])
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check endpoint.

    Returns:
        Dict containing liveness status
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
    }
