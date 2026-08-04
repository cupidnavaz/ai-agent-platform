from app.core.settings import get_settings


def test_default_settings() -> None:
    settings = get_settings()

    assert settings.app_name == "AI Agent Platform"
    assert settings.port == 8000
