"""Session API endpoints."""

from fastapi import APIRouter

from nov_fastapi.exceptions import AgentServiceError, SessionNotFoundError
from nov_fastapi.models.schemas import Message, SessionCreateResponse, SessionResponse
from nov_fastapi.services.session_manager import session_manager

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post(
    "",
    response_model=SessionCreateResponse,
    summary="Create a new conversation session",
    description="""
    Create a new conversation session for maintaining chat history.
    
    Sessions are stored in SQLAlchemy database and persist across server restarts.
    Each session maintains its own isolated conversation context.
    
    **Example Response:**
    ```json
    {
        "session_id": "session_abc123",
        "created_at": "2024-01-15T10:30:00Z"
    }
    ```
    """,
)
async def create_session() -> SessionCreateResponse:
    """
    Create a new session.

    Returns:
        SessionCreateResponse: Created session information.
    """
    try:
        session_id = await session_manager.create_session()
        session_info = await session_manager.get_session_info(session_id)
        return SessionCreateResponse(
            session_id=session_id,
            created_at=session_info.get("created_at") if session_info else None,
        )
    except Exception as e:
        raise AgentServiceError(f"Failed to create session: {str(e)}")


@router.get(
    "/{session_id}",
    response_model=SessionResponse,
    summary="Get session information and conversation history",
    description="""
    Retrieve session information and full conversation history for a given session ID.
    
    **Response includes:**
    - Session metadata (session_id, created_at, last_activity)
    - Complete conversation history with all messages
    
    **Example Response:**
    ```json
    {
        "session_id": "session_abc123",
        "created_at": "2024-01-15T10:30:00Z",
        "last_activity": "active",
        "message_count": 5,
        "messages": [
            {
                "role": "user",
                "content": "Hello"
            },
            {
                "role": "assistant",
                "content": "Hi there!"
            }
        ]
    }
    ```
    """,
)
async def get_session(session_id: str) -> SessionResponse:
    """
    Get session information and conversation history.

    Args:
        session_id: The session ID to retrieve.

    Returns:
        SessionResponse: Session information with conversation history.
    """
    session_info = await session_manager.get_session_info(session_id)
    if not session_info:
        raise SessionNotFoundError(f"Session {session_id} not found")

    conversation_history = await session_manager.get_conversation_history(session_id)
    messages = [
        Message(role=msg.get("role", ""), content=msg.get("content", ""))
        for msg in (conversation_history or [])
    ]

    return SessionResponse(
        session_id=session_id,
        created_at=session_info.get("created_at"),
        last_activity=session_info.get("last_activity"),
        messages=messages,
    )

