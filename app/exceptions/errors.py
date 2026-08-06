"""Project exceptions."""


class AIPlatformError(Exception):
    """Base project exception."""


class AgentError(AIPlatformError):
    """Agent-related error."""


class AgentNotFoundError(AgentError):
    """Agent does not exist."""


class ProviderError(AIPlatformError):
    """Provider error."""


class SessionError(AIPlatformError):
    """Session error."""


class SessionNotFoundError(SessionError):
    """Session does not exist."""


class ToolError(AIPlatformError):
    """Tool error."""


class ToolNotFoundError(ToolError):
    """Tool not found."""
