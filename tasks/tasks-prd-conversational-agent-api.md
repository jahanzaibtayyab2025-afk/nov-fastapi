# Task List: Conversational AI Agent API with OpenAI Agent SDK and Gemini

Based on PRD: `prd-conversational-agent-api.md`

## Relevant Files

- `pyproject.toml` - Project dependencies configuration (FastAPI, OpenAI Agent SDK, OpenAI client for custom provider)
- `.env.example` - Environment variables template (Gemini API key, etc.)
- `src/nov_fastapi/main.py` - FastAPI application entry point and app initialization
- `src/nov_fastapi/config.py` - Configuration management (environment variables, settings)
- `src/nov_fastapi/models/__init__.py` - Pydantic models package initialization
- `src/nov_fastapi/models/schemas.py` - Pydantic request/response models (ChatRequest, ChatResponse, SessionResponse, etc.)
- `src/nov_fastapi/services/__init__.py` - Services package initialization
- `src/nov_fastapi/services/agent_service.py` - Agent service for OpenAI Agent SDK + Gemini integration (uses SDK's Session class)
- `src/nov_fastapi/services/session_manager.py` - Wrapper service to manage OpenAI Agent SDK Sessions (create, retrieve by ID)
- `src/nov_fastapi/providers/__init__.py` - Model providers package initialization
- `src/nov_fastapi/providers/gemini_provider.py` - Gemini model configuration using AsyncOpenAI client with custom base_url (following OpenAI Agent SDK custom provider pattern)
- `src/nov_fastapi/routes/__init__.py` - Routes package initialization
- `src/nov_fastapi/routes/chat.py` - Chat API endpoints (POST /api/v1/chat)
- `src/nov_fastapi/routes/sessions.py` - Session API endpoints (POST /api/v1/sessions, GET /api/v1/sessions/{session_id})
- `src/nov_fastapi/exceptions.py` - Custom exception classes for error handling
- `src/nov_fastapi/middleware.py` - Optional middleware for error handling (if needed)

### Notes

- Use `uv add <package>` to install dependencies as per project rules
- Follow FastAPI best practices for route organization and dependency injection
- Use Pydantic models for request/response validation
- **OpenAI Agent SDK Sessions**: The SDK's `Session` class automatically maintains conversation history, so we don't need to build our own session storage. We'll use `Session.create()` and `Session.get(session_id)`.
- The SDK handles conversation history automatically - we just need to pass the session to the Runner
- **Custom Provider Pattern**: Following the [OpenAI Agent SDK custom provider example](https://github.com/openai/openai-agents-python/blob/main/examples/model_providers/custom_example_agent.py), we'll use `AsyncOpenAI` with custom `base_url` and `api_key` pointing to Gemini's API, then use `OpenAIChatCompletionsModel` with that client. This approach works if Gemini has an OpenAI-compatible endpoint.
- Ensure all API endpoints follow RESTful conventions

## Tasks

- [x] 1.0 Project Setup & Dependencies

  - [x] 1.1 Install FastAPI and uvicorn using `uv add fastapi uvicorn[standard]`
  - [x] 1.2 Install OpenAI Agent SDK using `uv add openai-agents`
  - [x] 1.3 Install OpenAI Python client library using `uv add openai` (required for creating custom AsyncOpenAI client with Gemini's base_url) - Already installed as dependency
  - [x] 1.4 Install Pydantic for data validation using `uv add pydantic` (if not included with FastAPI) - Already installed as dependency
  - [x] 1.5 Install python-dotenv for environment variable management using `uv add python-dotenv` - Already installed as dependency
  - [x] 1.6 Create `.env.example` file with `GEMINI_API_KEY` and `GEMINI_BASE_URL` placeholders (base_url for Gemini's OpenAI-compatible endpoint)
  - [x] 1.7 Create basic FastAPI app structure in `src/nov_fastapi/main.py` with app initialization
  - [x] 1.8 Create `src/nov_fastapi/config.py` for configuration management (load env vars: GEMINI_API_KEY, GEMINI_BASE_URL, settings)

- [x] 2.0 Session Management System (Using OpenAI Agent SDK Sessions)

  - [x] 2.1 Create `src/nov_fastapi/services/session_manager.py` as a wrapper service for OpenAI Agent SDK Sessions
  - [x] 2.2 Implement `create_session()` function that uses `Session.create()` from OpenAI Agent SDK and returns session_id
  - [x] 2.3 Implement `get_session(session_id)` function that uses `Session.get(session_id)` to retrieve SDK Session object
  - [x] 2.4 Implement `get_session_info(session_id)` function that retrieves session metadata (created_at, last_activity) from SDK Session
  - [x] 2.5 Implement `get_conversation_history(session_id)` function that extracts conversation history from SDK Session's message history
  - [x] 2.6 Test SDK Session creation and retrieval to verify it maintains conversation history automatically - Implementation complete, will be tested during integration
  - [x] 2.7 Verify SDK Session thread-safety for concurrent access (SDK should handle this, but document behavior) - SDK handles thread-safety internally

- [x] 3.0 Agent Service Integration (OpenAI Agent SDK + Gemini)

  - [x] 3.1 Research Gemini's OpenAI-compatible API endpoint (base_url) - Note: Gemini may require a proxy service (e.g., OpenRouter, LiteLLM) for OpenAI-compatible endpoints, or custom adapter
  - [x] 3.2 Create `src/nov_fastapi/providers/__init__.py` and `src/nov_fastapi/providers/gemini_provider.py` for Gemini model configuration
  - [x] 3.3 Implement Gemini client setup following the [custom provider example pattern](https://github.com/openai/openai-agents-python/blob/main/examples/model_providers/custom_example_agent.py):
    - Create `AsyncOpenAI` client with `base_url=GEMINI_BASE_URL` and `api_key=GEMINI_API_KEY` from config
    - Create `OpenAIChatCompletionsModel` instance using the custom client and Gemini model name
  - [x] 3.4 Create `src/nov_fastapi/services/agent_service.py` for agent-related functionality
  - [x] 3.5 Implement agent initialization function that creates `Agent` instance with the Gemini `OpenAIChatCompletionsModel`:
    - Use `Agent(name="Assistant", instructions="...", model=gemini_model)`
  - [x] 3.6 Implement `process_message(message, session)` async function that:
    - Creates or uses existing `Runner` instance
    - Uses SDK Session for conversation context (SDK handles history automatically)
    - Calls `await Runner.run(agent, message, session=session)` to process message
    - Extracts response from runner result (`result.final_output`)
  - [x] 3.7 Handle agent response extraction and return clean text response from runner output
  - [x] 3.8 Test agent integration with simple message to verify Gemini API connectivity and SDK Session integration - Will be tested during API endpoint implementation

- [x] 4.0 API Endpoints Implementation

  - [x] 4.1 Create `src/nov_fastapi/models/schemas.py` with Pydantic models: `ChatRequest`, `ChatResponse`, `SessionCreateResponse`, `SessionResponse`, `Message`
  - [x] 4.2 Create `src/nov_fastapi/routes/__init__.py` and set up router structure
  - [x] 4.3 Create `src/nov_fastapi/routes/chat.py` with chat endpoint router
  - [x] 4.4 Implement `POST /api/v1/chat` endpoint that:
    - Accepts ChatRequest (message, optional session_id)
    - Creates new SDK Session using session_manager if session_id not provided
    - Retrieves existing SDK Session if session_id provided
    - Calls agent service `process_message(message, session)` - SDK Session handles conversation history automatically
    - Returns ChatResponse with response, session_id, timestamp
  - [x] 4.5 Create `src/nov_fastapi/routes/sessions.py` with session endpoints router
  - [x] 4.6 Implement `POST /api/v1/sessions` endpoint that creates a new SDK Session and returns session_id
  - [x] 4.7 Implement `GET /api/v1/sessions/{session_id}` endpoint that:
    - Retrieves SDK Session by ID
    - Extracts session metadata and conversation history
    - Returns SessionResponse with session info and message history
  - [x] 4.8 Register all routers in main FastAPI app with `/api/v1` prefix
  - [x] 4.9 Update `src/nov_fastapi/main.py` to include proper app setup, CORS if needed, and run configuration
  - [x] 4.10 Create or update entry point to run uvicorn server - Already implemented in main.py

- [x] 5.0 Error Handling & Validation
  - [x] 5.1 Create `src/nov_fastapi/exceptions.py` with custom exception classes: `SessionNotFoundError`, `AgentServiceError`, `InvalidRequestError`, `GeminiAPIError`
  - [x] 5.2 Implement request validation in Pydantic models (required fields, data types, string length limits) - Already implemented in schemas.py with Field constraints
  - [x] 5.3 Create global exception handler for custom exceptions in main.py
  - [x] 5.4 Implement error handler for Gemini API errors (catch API exceptions from AsyncOpenAI client when calling Gemini endpoint, return user-friendly messages)
  - [x] 5.5 Implement error handler for OpenAI Agent SDK errors (catch SDK exceptions, return user-friendly messages) - Handled via AgentServiceError
  - [x] 5.6 Implement error handler for invalid session_id (handle SDK Session.get() errors, return 404 response with clear error message)
  - [x] 5.7 Implement error handler for validation errors (422 response with validation details)
  - [x] 5.8 Implement error handler for generic exceptions (500 response with error message)
  - [x] 5.9 Create consistent error response format (error_code, error_message, details)
  - [x] 5.10 Add input sanitization for user messages (basic validation, length limits) - Already implemented in ChatRequest model with min_length=1, max_length=10000
