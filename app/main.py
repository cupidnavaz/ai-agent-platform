from fastapi import FastAPI

from app.routes.agents import router as agents_router
from app.routes.chat import router as chat_router

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.version import VERSION

configure_logging(settings.log_level)

app = FastAPI(
    title="AI Agent Platform",
    version=VERSION,
)

app.include_router(agents_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {
        "message": "AI Agent Platform",
        "version": VERSION,
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }


@app.get("/version")
async def version():
    return {
        "version": VERSION,
    }
