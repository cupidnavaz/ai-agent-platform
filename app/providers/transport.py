"""Shared HTTP transport."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Iterator
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.providers.errors import (
    ProviderAuthenticationError,
    ProviderConnectionError,
    ProviderRateLimitError,
    ProviderResponseError,
    ProviderTimeoutError,
)

DEBUG_TRANSPORT = (
    os.getenv("AIEP_DEBUG_TRANSPORT") == "1"
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

            raw_body = exc.read().decode("utf-8")

            if DEBUG_TRANSPORT:
                print("\n========== PROVIDER ERROR ==========")
                print(f"HTTP {exc.code}")
                print(raw_body)
                print("====================================\n")

            try:
                body = json.loads(raw_body)
                message = body.get(
                    "error",
                    {},
                ).get(
                    "message",
                    raw_body,
                )
            except Exception:
                message = raw_body

            if exc.code == 401:
                raise ProviderAuthenticationError(
                    message
                ) from exc

            if exc.code == 429:
                raise ProviderRateLimitError(
                    message
                ) from exc

            raise ProviderResponseError(
                f"HTTP {exc.code}: {message}"
            ) from exc

        except URLError as exc:

            raise ProviderConnectionError(
                str(exc)
            ) from exc

        except TimeoutError as exc:

            raise ProviderTimeoutError(
                "Request timed out."
            ) from exc

    def stream(
        self,
        url: str,
        headers: dict[str, str],
        payload: dict,
    ) -> Iterator[str]:
        """Stream a POST response line by line."""

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

                for line in response:
                    text = line.decode("utf-8").strip()

                    if text:
                        yield text

        except HTTPError as exc:

            raw_body = exc.read().decode("utf-8")

            if DEBUG_TRANSPORT:
                print("\n========== PROVIDER ERROR ==========")
                print(f"HTTP {exc.code}")
                print(raw_body)
                print("====================================\n")

            try:
                body = json.loads(raw_body)
                message = body.get(
                    "error",
                    {},
                ).get(
                    "message",
                    raw_body,
                )
            except Exception:
                message = raw_body

            if exc.code == 401:
                raise ProviderAuthenticationError(
                    message
                ) from exc

            if exc.code == 429:
                raise ProviderRateLimitError(
                    message
                ) from exc

            raise ProviderResponseError(
                f"HTTP {exc.code}: {message}"
            ) from exc

        except URLError as exc:

            raise ProviderConnectionError(
                str(exc)
            ) from exc

        except TimeoutError as exc:

            raise ProviderTimeoutError(
                "Request timed out."
            ) from exc
