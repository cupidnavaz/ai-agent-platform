"""Provider configuration."""

from dataclasses import dataclass
import os


@dataclass(slots=True)
class ProviderSettings:
    """Configuration for AI providers."""

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-5"

    # Anthropic
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4"

    # Google
    google_api_key: str = ""
    google_model: str = "gemini-2.5-pro"

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    # OpenRouter
    openrouter_api_key: str = ""
    openrouter_model: str = "openai/gpt-5"

    # Azure OpenAI
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = ""


def load_provider_settings() -> ProviderSettings:
    """Load provider settings from environment variables."""

    return ProviderSettings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-5"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        anthropic_model=os.getenv(
            "ANTHROPIC_MODEL",
            "claude-sonnet-4",
        ),
        google_api_key=os.getenv("GOOGLE_API_KEY", ""),
        google_model=os.getenv(
            "GOOGLE_MODEL",
            "gemini-2.5-pro",
        ),
        ollama_host=os.getenv(
            "OLLAMA_HOST",
            "http://localhost:11434",
        ),
        ollama_model=os.getenv(
            "OLLAMA_MODEL",
            "llama3",
        ),
        openrouter_api_key=os.getenv(
            "OPENROUTER_API_KEY",
            "",
        ),
        openrouter_model=os.getenv(
            "OPENROUTER_MODEL",
            "openai/gpt-5",
        ),
        azure_openai_api_key=os.getenv(
            "AZURE_OPENAI_API_KEY",
            "",
        ),
        azure_openai_endpoint=os.getenv(
            "AZURE_OPENAI_ENDPOINT",
            "",
        ),
        azure_openai_deployment=os.getenv(
            "AZURE_OPENAI_DEPLOYMENT",
            "",
        ),
    )


settings = load_provider_settings()

# ==========================================================
# FUTURE AI STUDIO FEATURES (Private Roadmap)
#
# - Provider quotas
# - Secret vault integration
# - API key rotation
# - Workspace-specific providers
# - Cost analytics
# - Multi-provider routing
# - Provider benchmarking
# - Region-aware routing
#
# Reserved for future implementation.
# ==========================================================
