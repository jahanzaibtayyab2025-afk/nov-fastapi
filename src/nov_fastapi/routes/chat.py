"""Chat API endpoints."""

from datetime import datetime

from fastapi import APIRouter
from openai import APIError

from nov_fastapi.exceptions import AgentServiceError, GeminiAPIError, SessionNotFoundError

from nov_fastapi.models.schemas import ChatRequest, ChatResponse
from nov_fastapi.services.agent_service import agent_service
from nov_fastapi.services.session_manager import session_manager

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "",
    response_model=ChatResponse,
    summary="Send a message to the AI agent",
    description="""
    Send a message to the AI agent and receive an intelligent response.
    
    **Session Management:**
    - If `session_id` is provided, the conversation continues from that session
    - If `session_id` is not provided, a new session is automatically created
    - The agent maintains conversation context automatically using SQLAlchemy sessions
    
    **Example Request:**
    ```json
    {
        "message": "Hello, how are you?",
        "session_id": "optional-session-id"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "response": "I'm doing well, thank you! How can I help you today?",
        "session_id": "session_abc123",
        "timestamp": "2024-01-15T10:30:00Z"
    }
    ```
    """,
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Process a chat message and return agent response.

    Args:
        request: Chat request containing message and optional session_id.

    Returns:
        ChatResponse: Agent response with session_id and timestamp.
    """
    # Get or create session
    if request.session_id:
        session = await session_manager.get_session(request.session_id)
        if not session:
            raise SessionNotFoundError(f"Session {request.session_id} not found")
    else:
        session_id = await session_manager.create_session()
        session = await session_manager.get_session(session_id)
        if not session:
            raise AgentServiceError("Failed to create session")

    # Process message with agent
    try:
        response_text = await agent_service.process_message(request.message, session)
    except APIError as e:
        # Handle OpenAI API errors (which may be from Gemini if using proxy)
        raise GeminiAPIError(f"Gemini API error: {str(e)}")
    except Exception as e:
        raise AgentServiceError(f"Error processing message: {str(e)}")

    return ChatResponse(
        response=response_text,
        session_id=session.id,
        timestamp=datetime.utcnow(),
    )

