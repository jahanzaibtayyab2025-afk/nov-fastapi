"""Agent service for processing messages with OpenAI Agent SDK and Gemini."""

from agents import Agent, Runner
from agents import Session

from nov_fastapi.providers.gemini_provider import create_gemini_model


class AgentService:
    """Service for managing AI agents and processing messages."""

    def __init__(self, model_name: str = "gemini-pro"):
        """
        Initialize the agent service.

        Args:
            model_name: The Gemini model name to use.
        """
        self.model = create_gemini_model(model_name)
        self.agent = Agent(
            name="Assistant",
            instructions="You are a helpful, friendly, and knowledgeable AI assistant. "
            "You provide clear, concise, and accurate responses to user questions.",
            model=self.model,
        )

    async def process_message(self, message: str, session: Session) -> str:
        """
        Process a user message with the agent using the provided session.

        Args:
            message: The user's message to process.
            session: The SDK Session object for maintaining conversation context.

        Returns:
            str: The agent's response text.
        """
        result = await Runner.run(self.agent, message, session=session)
        return result.final_output


# Create a global instance for easy access
agent_service = AgentService()

