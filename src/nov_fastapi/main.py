"""FastAPI application entry point."""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from nov_fastapi.exceptions import (
    AgentServiceError,
    GeminiAPIError,
    InvalidRequestError,
    SessionNotFoundError,
)
from nov_fastapi.routes import chat, sessions

# Create FastAPI app instance
app = FastAPI(
    title="Conversational AI Agent API",
    description="""
    REST API for conversational AI agents using OpenAI Agent SDK with Google Gemini.
    
    ## Features
    
    * 🤖 **AI-Powered Conversations**: Chat with AI agents powered by Google Gemini
    * 🧠 **Session Memory**: Automatic conversation history management using SQLAlchemy
    * 🔄 **Multi-turn Conversations**: Maintain context across multiple interactions
    * 📝 **Comprehensive API**: Full REST API with Swagger documentation
    
    ## Endpoints
    
    ### Chat
    * `POST /api/v1/chat` - Send a message to the AI agent and get a response
    
    ### Sessions
    * `POST /api/v1/sessions` - Create a new conversation session
    * `GET /api/v1/sessions/{session_id}` - Retrieve session information and conversation history
    
    ## Session Management
    
    Sessions are managed using SQLAlchemy, providing persistent storage for conversation history.
    Each session maintains its own isolated conversation context.
    
    ## Authentication
    
    Currently, no authentication is required. In production, implement proper authentication.
    """,
    version="0.1.0",
    contact={
        "name": "API Support",
        "email": "jtayyab204@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    tags_metadata=[
        {
            "name": "chat",
            "description": "Chat with AI agents. Send messages and receive intelligent responses with automatic conversation context management.",
        },
        {
            "name": "sessions",
            "description": "Manage conversation sessions. Create new sessions and retrieve conversation history stored in SQLAlchemy database.",
        },
    ],
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")


# Exception handlers
@app.exception_handler(SessionNotFoundError)
async def session_not_found_handler(request: Request, exc: SessionNotFoundError):
    """Handle session not found errors."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_code": "SESSION_NOT_FOUND",
            "error_message": "Session not found",
            "details": str(exc),
        },
    )


@app.exception_handler(AgentServiceError)
async def agent_service_error_handler(request: Request, exc: AgentServiceError):
    """Handle agent service errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "AGENT_SERVICE_ERROR",
            "error_message": "Error processing agent request",
            "details": str(exc),
        },
    )


@app.exception_handler(GeminiAPIError)
async def gemini_api_error_handler(request: Request, exc: GeminiAPIError):
    """Handle Gemini API errors."""
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={
            "error_code": "GEMINI_API_ERROR",
            "error_message": "Error communicating with Gemini API",
            "details": str(exc),
        },
    )


@app.exception_handler(InvalidRequestError)
async def invalid_request_error_handler(request: Request, exc: InvalidRequestError):
    """Handle invalid request errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_code": "INVALID_REQUEST",
            "error_message": "Invalid request",
            "details": str(exc),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error_code": "VALIDATION_ERROR",
            "error_message": "Request validation failed",
            "details": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle generic exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error_code": "INTERNAL_SERVER_ERROR",
            "error_message": "An unexpected error occurred",
            "details": str(exc),
        },
    )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Conversational AI Agent API",
        "version": "0.1.0",
        "description": "REST API for conversational AI agents",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


def main(reload: bool = True, host: str = "0.0.0.0", port: int = 8000) -> None:
    """
    Entry point for running the application.

    Args:
        reload: Enable auto-reload on code changes (default: True for development).
        host: Host to bind to (default: "0.0.0.0").
        port: Port to bind to (default: 8000).
    """
    import uvicorn

    uvicorn.run(
        "nov_fastapi.main:app",
        host=host,
        port=port,
        reload=reload,
    )


def main_prod() -> None:
    """Entry point for running the application in production mode (no reload)."""
    main(reload=False)


if __name__ == "__main__":
    main()

