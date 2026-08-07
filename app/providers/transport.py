"""Shared HTTP transport."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.providers.errors import (
    ProviderAuthenticationError,
    ProviderConnectionError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderTimeoutError,
)


@dataclass(slots=True)
class HTTPResponse:
    """HTTP response."""

    status_code: int
    body: dict


class HTTPTransport:
    """Simple HTTP transport."""

    def __init__(
        self,
        timeout: float = 30.0,
    ) -> None:
        self.timeout = timeout

    def post(
        self,
        url: str,
        headers: dict[str, str],
        payload: dict,
    ) -> HTTPResponse:
        """Send a POST request."""

        request = Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urlopen(
                request,
                timeout=self.timeout,
            ) as response:

                body = json.loads(
                    response.read().decode("utf-8")
                )

                return HTTPResponse(
                    status_code=response.status,
                    body=body,
                )

        except HTTPError as exc:

            if exc.code == 401:
                raise ProviderAuthenticationError(
                    "Authentication failed."
                ) from exc

            if exc.code == 429:
                raise ProviderRateLimitError(
                    "Rate limit exceeded."
                ) from exc

            raise ProviderResponseError(
                f"HTTP {exc.code}"
            ) from exc

        except URLError as exc:

            raise ProviderConnectionError(
                str(exc)
            ) from exc

        except TimeoutError as exc:

            raise ProviderTimeoutError(
                "Request timed out."
            ) from exc
