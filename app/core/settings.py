"""Application settings."""

from dataclasses import dataclass

from app.core.constants import (
    APP_NAME,
    APP_VERSION,
    ENVIRONMENT,
    HOST,
    LOG_LEVEL,
    PORT,
)


@dataclass(slots=True)
class Settings:
    """Application configuration."""

    app_name: str = APP_NAME
    app_version: str = APP_VERSION
    environment: str = ENVIRONMENT
    host: str = HOST
    port: int = PORT
    log_level: str = LOG_LEVEL


_settings = Settings()


def get_settings() -> Settings:
    """Return the application settings singleton."""
    return _settings


settings = get_settings()
