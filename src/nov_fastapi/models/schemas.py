"""Pydantic request/response models for API endpoints."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Message model for conversation history."""

    role: str = Field(..., description="Message role (user or assistant)")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., min_length=1, max_length=10000, description="User message")
    session_id: Optional[str] = Field(None, description="Optional session ID for continuing conversation")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str = Field(..., description="Agent response")
    session_id: str = Field(..., description="Session ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class SessionCreateResponse(BaseModel):
    """Response model for session creation endpoint."""

    session_id: str = Field(..., description="Created session ID")
    created_at: Optional[datetime] = Field(None, description="Session creation timestamp")


class SessionResponse(BaseModel):
    """Response model for session retrieval endpoint."""

    session_id: str = Field(..., description="Session ID")
    created_at: Optional[datetime] = Field(None, description="Session creation timestamp")
    last_activity: Optional[datetime] = Field(None, description="Last activity timestamp")
    messages: List[Message] = Field(default_factory=list, description="Conversation history")

