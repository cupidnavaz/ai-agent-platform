"""Shared runtime configuration for AI providers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ProviderRuntimeConfig:
    """Base runtime configuration."""

    api_key: str
    base_url: str
    timeout: float = 30.0
