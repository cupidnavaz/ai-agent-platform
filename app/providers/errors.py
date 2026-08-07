"""Provider exceptions."""


class ProviderError(Exception):
    """Base provider exception."""


class ProviderAuthenticationError(ProviderError):
    """Authentication failed."""


class ProviderConnectionError(ProviderError):
    """Connection to provider failed."""


class ProviderRateLimitError(ProviderError):
    """Rate limit exceeded."""


class ProviderTimeoutError(ProviderError):
    """Request timed out."""


class ProviderResponseError(ProviderError):
    """Invalid provider response."""
