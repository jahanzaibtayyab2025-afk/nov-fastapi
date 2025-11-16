"""Gemini model provider for OpenAI Agent SDK."""

from openai import AsyncOpenAI

from agents import OpenAIChatCompletionsModel

from nov_fastapi.config import settings


def create_gemini_client() -> AsyncOpenAI:
    """
    Create an AsyncOpenAI client configured for Gemini API.

    Note: This assumes Gemini has an OpenAI-compatible endpoint.
    If Gemini doesn't support OpenAI-compatible API directly, you may need to:
    1. Use a proxy service (e.g., OpenRouter, LiteLLM) that provides OpenAI-compatible endpoints
    2. Or implement a custom adapter that translates OpenAI format to Gemini format

    Returns:
        AsyncOpenAI: Configured client for Gemini API.
    """
    return AsyncOpenAI(
        base_url=settings.GEMINI_BASE_URL,
        api_key=settings.GEMINI_API_KEY,
    )


def create_gemini_model(model_name: str = "gemini-pro") -> OpenAIChatCompletionsModel:
    """
    Create an OpenAIChatCompletionsModel instance for Gemini.

    Args:
        model_name: The Gemini model name to use (e.g., "gemini-pro", "gemini-1.5-pro").

    Returns:
        OpenAIChatCompletionsModel: Configured model instance for Gemini.
    """
    client = create_gemini_client()
    return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

