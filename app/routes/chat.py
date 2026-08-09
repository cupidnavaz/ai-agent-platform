"""Chat API routes."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.container import Container
from app.providers.mock import MockProvider
from app.runtime import Runtime

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


container = Container(
    provider=MockProvider(),
)

runtime = Runtime(container)


class ChatRequest(BaseModel):
    """Chat request payload."""

    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    """Chat response payload."""

    session_id: str
    reply: str


@router.post(
    "/",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
):
    """Send a message through a runtime session."""

    session_id = request.session_id

    if session_id is None:
        session_id = runtime.create_session()

    reply = runtime.chat(
        session_id,
        request.message,
    )

    return ChatResponse(
        session_id=session_id,
        reply=reply,
    )


@router.get("/history")
async def history(
    session_id: str,
):
    """Return chat history for a session."""

    return runtime.history(
        session_id
    )


@router.delete("/history")
async def clear_history(
    session_id: str,
):
    """Clear chat history for a session."""

    runtime.clear_history(
        session_id
    )

    return {
        "success": True,
    }


@router.post("/sessions")
async def create_session():
    """Create a new chat session."""

    return {
        "session_id": runtime.create_session(),
    }


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
):
    """Delete a chat session."""

    deleted = runtime.delete_session(
        session_id
    )

    if not deleted:
        return {
            "success": False,
            "session_id": session_id,
        }

    return {
        "success": True,
        "session_id": session_id,
    }
