"""Custom exceptions for the Math Assistant."""


class MathAssistantError(Exception):
    """Base exception for Math Assistant."""

    pass


class ImageProcessingError(MathAssistantError):
    """Raised when there's an error processing an image."""

    pass


class APIError(MathAssistantError):
    """Raised when there's an error with the API."""

    pass


class ConfigurationError(MathAssistantError):
    """Raised when there's a configuration error."""

    pass
