# Conversational AI Agent API 2

REST API for conversational AI agents using OpenAI Agent SDK with Google Gemini.

## Features

- 🤖 AI-powered conversational agents using OpenAI Agent SDK
- 🧠 Automatic conversation history management with SDK Sessions
- 🔌 Gemini model integration via custom provider pattern
- 🚀 FastAPI-based REST API
- 📝 Comprehensive error handling and validation
- 🔒 Type-safe configuration with Pydantic

## Installation

1. Install dependencies using `uv`:

```bash
uv sync
```

2. Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

3. Add your Gemini API credentials to `.env`:

```
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```

**Note:** If Gemini doesn't have a direct OpenAI-compatible endpoint, you may need to use a proxy service (e.g., OpenRouter, LiteLLM) that provides OpenAI-compatible endpoints for Gemini.

## Running the Application

### Development Mode (with auto-reload)

```bash
nov-fastapi
```

Or using Python directly:

```bash
python -m nov_fastapi.main
```

Or using uvicorn:

```bash
uvicorn nov_fastapi.main:app --reload
```

### Production Mode (no auto-reload)

```bash
nov-fastapi-prod
```

Or using uvicorn:

```bash
uvicorn nov_fastapi.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Chat Endpoint

- **POST** `/api/v1/chat`
- **Request Body:**
  ```json
  {
    "message": "Hello, how are you?",
    "session_id": "optional-session-id"
  }
  ```
- **Response:**
  ```json
  {
    "response": "I'm doing well, thank you!",
    "session_id": "session-id",
    "timestamp": "2024-01-15T10:30:00Z"
  }
  ```

### Session Management

- **POST** `/api/v1/sessions` - Create a new session
- **GET** `/api/v1/sessions/{session_id}` - Get session info and conversation history

### Health Check

- **GET** `/health` - Health check endpoint

## Project Structure

```
src/nov_fastapi/
├── __init__.py
├── main.py              # FastAPI app and entry point
├── config.py            # Configuration management
├── exceptions.py        # Custom exceptions
├── models/
│   ├── __init__.py
│   └── schemas.py       # Pydantic request/response models
├── providers/
│   ├── __init__.py
│   └── gemini_provider.py  # Gemini model provider
├── routes/
│   ├── __init__.py
│   ├── chat.py          # Chat endpoints
│   └── sessions.py       # Session endpoints
└── services/
    ├── __init__.py
    ├── agent_service.py      # Agent service
    └── session_manager.py    # Session management
```

## Development

Install development dependencies:

```bash
uv sync --extra dev
```

## License

MIT
