"""OpenAI client."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

from app.providers.errors import (
    ProviderAuthenticationError,
    ProviderConnectionError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderTimeoutError,
)
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
        payload: dict[str, Any],
    ) -> HTTPResponse | str:
        """Send a POST request."""

        response = self.transport.post(
            url=self._url(endpoint),
            headers=self.headers,
            payload=payload,
        )

        if isinstance(response, HTTPResponse):
            self._raise_for_status(response)

        return response

    def stream(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> Iterator[dict[str, Any]]:
        """Stream JSON events from the OpenAI API."""

        try:
            lines = self.transport.stream(
                url=self._url(endpoint),
                headers=self.headers,
                payload=payload,
            )

            for line in lines:
                if not line.startswith("data:"):
                    continue

                data = line[5:].strip()

                if not data:
                    continue

                if data == "[DONE]":
                    break

                try:
                    event = json.loads(data)
                except json.JSONDecodeError as exc:
                    raise ProviderResponseError(
                        "Invalid JSON in OpenAI stream response."
                    ) from exc

                if not isinstance(event, dict):
                    raise ProviderResponseError(
                        "Invalid OpenAI stream event."
                    )

                yield event

        except (
            ProviderAuthenticationError,
            ProviderConnectionError,
            ProviderRateLimitError,
            ProviderResponseError,
            ProviderTimeoutError,
        ):
            raise

    def health(self) -> bool:
        """Basic client health check."""

        return bool(
            self.config.api_key
            and self.config.base_url
        )

    def _url(
        self,
        endpoint: str,
    ) -> str:
        """Build an endpoint URL."""

        return (
            f"{self.config.base_url.rstrip('/')}/"
            f"{endpoint.lstrip('/')}"
        )

    @staticmethod
    def _raise_for_status(
        response: HTTPResponse,
    ) -> None:
        """Map HTTP failures to provider exceptions."""

        status = response.status_code

        if 200 <= status < 300:
            return

        if status in (401, 403):
            raise ProviderAuthenticationError(
                "OpenAI authentication failed."
            )

        if status == 429:
            raise ProviderRateLimitError(
                "OpenAI rate limit exceeded."
            )

        if status in (408, 504):
            raise ProviderTimeoutError(
                "OpenAI request timed out."
            )

        if 400 <= status < 500:
            raise ProviderResponseError(
                f"OpenAI request failed with status {status}."
            )

        if status >= 500:
            raise ProviderConnectionError(
                f"OpenAI server error: {status}."
            )

        raise ProviderResponseError(
            f"Unexpected OpenAI response status: {status}."
        )
