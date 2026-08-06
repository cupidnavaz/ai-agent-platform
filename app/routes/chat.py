from fastapi import APIRouter
from pydantic import BaseModel

from app.agents.assistant import Assistant
from app.providers.mock import MockProvider

router = APIRouter(prefix="/chat", tags=["Chat"])

assistant = Assistant(MockProvider())


class ChatRequest(BaseModel):
    message: str


@router.post("/")
async def chat(request: ChatRequest):
    return {
        "reply": assistant.chat(request.message)
    }


@router.get("/history")
async def history():
    return assistant.history()


@router.delete("/history")
async def clear_history():
    assistant.clear()
    return {"success": True}
