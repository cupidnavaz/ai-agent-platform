"""Application settings."""

import os


class Settings:
    """Application configuration."""

    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")

        self.default_provider = os.getenv(
            "DEFAULT_PROVIDER",
            "mock",
        )

        self.log_level = os.getenv(
            "LOG_LEVEL",
            "INFO",
        )


settings = Settings()
