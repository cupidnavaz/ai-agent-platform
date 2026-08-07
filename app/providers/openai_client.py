"""OpenAI client."""

from __future__ import annotations

from app.providers.openai_config import OpenAIConfig
from app.providers.transport import (
    HTTPResponse,
    HTTPTransport,
)


class OpenAIClient:
    """Low-level OpenAI API client."""

    def __init__(
        self,
        config: OpenAIConfig,
    ) -> None:
        """Initialize the client."""

        self.config = config
        self.transport = HTTPTransport(config.timeout)

    @property
    def headers(self) -> dict[str, str]:
        """Return request headers."""

        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

    def post(
        self,
        endpoint: str,
        payload: dict,
    ) -> HTTPResponse:
        """Send a POST request."""

        return self.transport.post(
            url=f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}",
            headers=self.headers,
            payload=payload,
        )

    def health(self) -> bool:
        """Basic client health check."""

        return bool(self.config.api_key)
