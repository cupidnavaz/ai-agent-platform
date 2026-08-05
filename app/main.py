from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.version import VERSION

configure_logging(settings.log_level)

app = FastAPI(
    title="AI Agent Platform",
    version=VERSION,
)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "AI Agent Platform",
        "version": VERSION,
    }


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }


@app.get("/version")
async def version() -> dict[str, str]:
    return {
        "version": VERSION,
    }
