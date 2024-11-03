"""Configuration settings for the Math Assistant."""

import os
from typing import List


class Config:
    """Configuration settings."""

    # API settings
    ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")

    # Image settings
    MAX_IMAGE_SIZE: int = 2048
    SUPPORTED_FORMATS: List[str] = [".jpg", ".jpeg", ".png"]

    # Model settings
    DEFAULT_MODEL: str = "claude-3-5-sonnet-20241022"
    DEFAULT_MAX_TOKENS: int = 1500

    # Output settings
    DEFAULT_FORMAT_STYLE: str = "rich"

    @classmethod
    def initialize(cls) -> None:
        """Initialize configuration."""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
