"""OpenAI client."""

from __future__ import annotations

from app.providers.transport import (
    HTTPResponse,
    HTTPTransport,
)


class OpenAIClient:
    """Low-level OpenAI API client."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        timeout: float = 30.0,
    ) -> None:

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.transport = HTTPTransport(timeout)

    @property
    def headers(self) -> dict[str, str]:
        """Return request headers."""

        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def post(
        self,
        endpoint: str,
        payload: dict,
    ) -> HTTPResponse:
        """Send a POST request."""

        return self.transport.post(
            url=f"{self.base_url}/{endpoint.lstrip('/')}",
            headers=self.headers,
            payload=payload,
        )

    def health(self) -> bool:
        """Basic client health check."""

        return bool(self.api_key)
