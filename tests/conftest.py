"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_application


@pytest.fixture
def client() -> TestClient:
    """
    Create a test client for the application.

    Returns:
        TestClient: FastAPI test client
    """
    app = create_application()
    return TestClient(app)


@pytest.fixture
def test_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Override settings for testing.

    Args:
        monkeypatch: Pytest monkeypatch fixture
    """
    monkeypatch.setenv("ENVIRONMENT", "testing")
    monkeypatch.setenv("DEBUG", "True")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
