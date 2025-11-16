"""Custom exception classes for error handling."""


class SessionNotFoundError(Exception):
    """Raised when a session is not found."""

    pass


class AgentServiceError(Exception):
    """Raised when there's an error in the agent service."""

    pass


class InvalidRequestError(Exception):
    """Raised when a request is invalid."""

    pass


class GeminiAPIError(Exception):
    """Raised when there's an error with the Gemini API."""

    pass

