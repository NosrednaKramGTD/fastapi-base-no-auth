"""Application configuration management."""

from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Project metadata
    PROJECT_NAME: str = Field(default="CHANGEME_PROJECT_NAME")
    PROJECT_DESCRIPTION: str = Field(default="CHANGEME_PROJECT_DESCRIPTION")
    VERSION: str = Field(default="0.1.0")

    # Environment
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)

    # API Configuration
    API_V1_PREFIX: str = Field(default="/api/v1")

    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8000"]
    )

    # Database Configuration (ready for future use)
    DATABASE_URL: str = Field(
        default="sqlite:///./app.db",
        description="Database connection URL",
    )
    DATABASE_ECHO: bool = Field(
        default=False,
        description="Echo SQL queries (useful for debugging)",
    )

    # Security Configuration (ready for authentication layer)
    SECRET_KEY: str = Field(
        default="CHANGEME_SECRET_KEY_IN_PRODUCTION",
        description="Secret key for cryptographic operations",
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="Algorithm for JWT token encoding",
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes",
    )

    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(
        default="json",
        description="Log format: 'json' for production, 'console' for development",
    )

    # Application Settings
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8910)


# Create a singleton settings instance
settings = Settings()
