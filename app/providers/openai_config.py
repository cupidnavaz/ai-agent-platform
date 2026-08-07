"""OpenAI runtime configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass

from app.providers.runtime_config import ProviderRuntimeConfig


@dataclass(slots=True)
class OpenAIConfig(ProviderRuntimeConfig):
    """OpenAI runtime configuration."""

    model: str = "gpt-4.1-mini"

    @classmethod
    def from_env(cls) -> "OpenAIConfig":
        """Load configuration from environment."""

        api_key = os.getenv(
            "OPENAI_API_KEY",
            "",
        ).strip()

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not set."
            )

        return cls(
            api_key=api_key,
            base_url=os.getenv(
                "OPENAI_BASE_URL",
                "https://api.openai.com/v1",
            ),
            timeout=float(
                os.getenv(
                    "OPENAI_TIMEOUT",
                    "30",
                )
            ),
            model=os.getenv(
                "OPENAI_MODEL",
                "gpt-4.1-mini",
            ),
        )
