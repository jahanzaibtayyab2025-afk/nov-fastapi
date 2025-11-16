"""Configuration management for the application."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Gemini API Configuration
    gemini_api_key: str
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta"

    # Optional: OpenAI API Key (for tracing or other features)
    openai_api_key: Optional[str] = None

    # Database Configuration
    database_url: str = "sqlite+aiosqlite:///./sessions.db"

    # Application Settings
    app_name: str = "Conversational AI Agent API 2"
    app_version: str = "0.1.0"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def GEMINI_API_KEY(self) -> str:
        """Get Gemini API key."""
        return self.gemini_api_key

    @property
    def GEMINI_BASE_URL(self) -> str:
        """Get Gemini base URL."""
        return self.gemini_base_url

    @property
    def OPENAI_API_KEY(self) -> Optional[str]:
        """Get OpenAI API key if available."""
        return self.openai_api_key

    @property
    def DATABASE_URL(self) -> str:
        """Get database URL."""
        return self.database_url


# Create a global settings instance
settings = Settings()

