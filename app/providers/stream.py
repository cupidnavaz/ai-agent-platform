"""Streaming models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ChatChunk:
    """A streamed chat chunk."""

    content: str
    finished: bool = False
