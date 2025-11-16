"""Session management service using OpenAI Agent SDK SQLAlchemy Sessions."""

from typing import Optional

from agents.extensions.memory import SQLAlchemySession

from nov_fastapi.config import settings


class SessionManager:
    """Wrapper service for managing OpenAI Agent SDK SQLAlchemy Sessions."""

    _initialized = False

    @classmethod
    def _initialize(cls):
        """Initialize SQLAlchemy session factory."""
        if cls._initialized:
            return

        # Test database connection by creating a temporary session
        try:
            test_session = SQLAlchemySession.from_url(
                session_id="__init__",
                url=settings.DATABASE_URL,
                create_tables=True,
            )
            cls._initialized = True
        except Exception as e:
            raise RuntimeError(f"Failed to initialize database: {str(e)}")

    @classmethod
    async def create_session(cls, session_id: Optional[str] = None) -> str:
        """
        Create a new session using OpenAI Agent SDK SQLAlchemy Session.

        Args:
            session_id: Optional custom session ID. If not provided, a UUID will be generated.

        Returns:
            str: The session ID of the newly created session.
        """
        cls._initialize()

        import uuid

        if not session_id:
            session_id = f"session_{uuid.uuid4().hex[:12]}"

        # Create a new SQLAlchemy session to verify it works
        session = SQLAlchemySession.from_url(
            session_id=session_id,
            url=settings.DATABASE_URL,
            create_tables=True,
        )

        # Verify session by getting items (empty list for new session)
        await session.get_items(limit=1)

        return session_id

    @classmethod
    async def get_session(cls, session_id: str) -> Optional[SQLAlchemySession]:
        """
        Retrieve a session by ID using OpenAI Agent SDK SQLAlchemy Session.

        Args:
            session_id: The ID of the session to retrieve.

        Returns:
            Optional[SQLAlchemySession]: The Session object if found, None otherwise.
        """
        cls._initialize()

        try:
            session = SQLAlchemySession.from_url(
                session_id=session_id,
                url=settings.DATABASE_URL,
                create_tables=True,
            )
            # Verify session exists by trying to get items
            # This will succeed even for empty sessions
            await session.get_items(limit=1)
            return session
        except Exception:
            return None

    @classmethod
    async def get_session_info(cls, session_id: str) -> Optional[dict]:
        """
        Get session metadata from SQLAlchemy Session.

        Args:
            session_id: The ID of the session.

        Returns:
            Optional[dict]: Dictionary with session metadata if found, None otherwise.
        """
        session = await cls.get_session(session_id)
        if not session:
            return None

        # Get items to determine session activity
        items = await session.get_items()
        message_count = len(items) if items else 0

        return {
            "session_id": session_id,
            "created_at": None,  # SQLAlchemy sessions don't expose created_at directly
            "last_activity": "active" if message_count > 0 else None,
            "message_count": message_count,
        }

    @classmethod
    async def get_conversation_history(cls, session_id: str) -> Optional[list]:
        """
        Extract conversation history from SQLAlchemy Session's message history.

        Args:
            session_id: The ID of the session.

        Returns:
            Optional[list]: List of messages if session found, None otherwise.
        """
        session = await cls.get_session(session_id)
        if not session:
            return None

        # Get all items from the session
        items = await session.get_items()

        # Convert items to message format
        messages = []
        for item in items:
            # Items are TResponseInputItem objects
            if hasattr(item, "role") and hasattr(item, "content"):
                messages.append({
                    "role": getattr(item, "role", "unknown"),
                    "content": str(getattr(item, "content", "")),
                })
            elif isinstance(item, dict):
                messages.append({
                    "role": item.get("role", "unknown"),
                    "content": str(item.get("content", "")),
                })
            else:
                # Try to extract role and content from item attributes
                role = getattr(item, "role", None) or (item.get("role") if isinstance(item, dict) else "unknown")
                content = getattr(item, "content", None) or (item.get("content") if isinstance(item, dict) else "")
                if role and content:
                    messages.append({
                        "role": str(role),
                        "content": str(content),
                    })

        return messages


# Create a global instance for easy access
session_manager = SessionManager()
