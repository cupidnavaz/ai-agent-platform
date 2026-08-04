"""Application settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_HOST,
    DEFAULT_LOG_LEVEL,
    DEFAULT_PORT,
    ENV_DEVELOPMENT,
)


class Settings(BaseSettings):
    """Application configuration."""

    app_name: str = APP_NAME
    app_version: str = APP_VERSION

    environment: str = ENV_DEVELOPMENT

    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT

    log_level: str = DEFAULT_LOG_LEVEL

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()
