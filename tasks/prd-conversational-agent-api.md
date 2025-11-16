# Product Requirements Document: Conversational AI Agent API with OpenAI Agent SDK and Gemini

## Introduction/Overview

This feature will integrate OpenAI Agent SDK with Google's Gemini model to create a conversational AI agent system accessible via REST API endpoints. The system will enable end users to interact with intelligent agents that maintain conversation context and memory across sessions. The primary goal is to provide a fast, responsive conversational AI experience through a FastAPI-based backend, using Gemini as the underlying language model while leveraging OpenAI Agent SDK's agent framework capabilities.

**Problem Statement:** Users need a way to interact with AI agents that can maintain context and memory across conversations, providing a more natural and coherent conversational experience through a simple REST API interface.

## Goals

1. Integrate OpenAI Agent SDK with Google Gemini API to enable conversational AI agent functionality
2. Implement REST API endpoints that allow end users to interact with AI agents
3. Provide memory and context management so agents can maintain conversation history within user sessions
4. Ensure low response latency for real-time conversational interactions
5. Implement user session management to track and manage individual user conversations

## User Stories

1. **As an end user**, I want to send a message to the AI agent via a REST API endpoint, so that I can get intelligent responses to my queries.

2. **As an end user**, I want the agent to remember our previous conversation within a session, so that I can have a coherent, context-aware dialogue.

3. **As an end user**, I want to start a new conversation session, so that I can begin fresh interactions without previous context interfering.

4. **As an end user**, I want to receive responses quickly, so that the conversation feels natural and responsive.

5. **As an end user**, I want to interact with the agent through simple HTTP requests, so that I can easily integrate it into my applications or use it directly.

## Functional Requirements

### Core Agent Functionality

1. The system must integrate OpenAI Agent SDK with Google Gemini API as the underlying language model.

2. The system must create and manage AI agent instances that can process user messages and generate appropriate responses.

3. The system must maintain conversation memory and context for each user session, allowing the agent to reference previous messages within the same session.

4. The system must support multiple concurrent user sessions, with each session maintaining its own isolated conversation context.

### API Endpoints

5. The system must provide a REST API endpoint (e.g., `POST /api/v1/chat`) that accepts user messages and returns agent responses.

6. The API endpoint must accept a request body containing:

   - User message text
   - Session identifier (or generate a new one if not provided)

7. The API endpoint must return a response containing:

   - Agent response text
   - Session identifier
   - Timestamp of the interaction

8. The system must provide an endpoint to create a new session (e.g., `POST /api/v1/sessions`) that returns a unique session identifier.

9. The system must provide an endpoint to retrieve session information (e.g., `GET /api/v1/sessions/{session_id}`) that returns the conversation history for that session.

### Session Management

10. The system must generate unique session identifiers for each new user session.

11. The system must store session data in memory (or a simple storage mechanism) to maintain conversation history.

12. The system must associate conversation messages with their respective session identifiers.

13. The system must allow retrieval of conversation history for a given session.

### Memory and Context Management

14. The system must maintain a conversation history for each session, including both user messages and agent responses.

15. The system must pass conversation history to the agent when processing new messages, enabling context-aware responses.

16. The system must limit the conversation history length to prevent excessive token usage (e.g., keep last N messages or implement a token-based limit).

### Error Handling

17. The system must handle cases where an invalid session identifier is provided and return an appropriate error response.

18. The system must handle API errors from the Gemini API and return meaningful error messages to the user.

19. The system must validate incoming request data and return validation errors when required fields are missing or invalid.

### Performance

20. The system must optimize for low response latency, with a target response time of under 3 seconds for typical queries.

21. The system must handle concurrent requests efficiently without blocking other user sessions.

## Non-Goals (Out of Scope)

1. **Authentication/Authorization:** User authentication and authorization are not included in this initial implementation. All sessions are accessible without authentication.

2. **Rate Limiting:** API rate limiting is not included in this initial version.

3. **Persistent Storage:** Long-term persistent storage (e.g., database) is not included. Session data may be stored in memory only.

4. **Advanced Agent Features:** Advanced features like tool calling, function execution, or multi-agent coordination are not included in this basic implementation.

5. **WebSocket Support:** Real-time streaming via WebSocket is not included. Only REST API endpoints are provided.

6. **Monitoring and Logging:** Comprehensive monitoring, logging, and analytics are not included in this basic implementation.

7. **Agent Configuration UI:** A user interface for configuring agent behavior is not included. Configuration will be done through code/environment variables.

8. **Multi-turn Planning:** Complex multi-step reasoning and planning capabilities are not included. The agent will respond to individual messages with context awareness.

## Design Considerations

### API Design

- Follow RESTful API conventions
- Use JSON for request/response bodies
- Include appropriate HTTP status codes (200, 400, 404, 500, etc.)
- Provide clear, consistent error message formats

### Request/Response Format

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
  "session_id": "generated-or-provided-session-id",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Session Management

- Sessions can be identified by UUIDs
- Session data structure should include:
  - Session ID
  - Creation timestamp
  - List of conversation messages (user and agent)
  - Last activity timestamp

## Technical Considerations

1. **Dependencies:**

   - OpenAI Agent SDK (Python package)
   - Google Gemini API client library
   - FastAPI framework (already in project)
   - Python 3.11+ (already configured)

2. **Environment Variables:**

   - Gemini API key (required)
   - Any OpenAI Agent SDK configuration (if needed)

3. **Project Structure:**

   - Create agent service module in `src/nov_fastapi/`
   - Create API route handlers in `src/nov_fastapi/routes/` or similar
   - Create session management module for handling session state

4. **Integration Points:**

   - Integrate with existing FastAPI application structure
   - Ensure compatibility with existing project dependencies

5. **Memory Management:**
   - Consider using in-memory dictionaries or simple data structures for session storage
   - Implement conversation history truncation to manage memory usage

## Success Metrics

1. **Response Latency:** Average API response time should be under 3 seconds for typical queries (measured at the 95th percentile).

2. **API Availability:** The API endpoints should be accessible and functional.

3. **Context Retention:** The agent should successfully reference previous messages within the same session in at least 90% of multi-turn conversations.

4. **Error Rate:** API error rate (excluding user input validation errors) should be less than 5%.

## Open Questions

1. What is the maximum conversation history length (number of messages or tokens) that should be maintained per session?

2. Should there be a session expiration mechanism (e.g., sessions expire after X minutes of inactivity)?

3. What is the preferred format for conversation history in session storage (e.g., list of message objects with role, content, timestamp)?

4. Are there any specific Gemini model parameters (temperature, max tokens, etc.) that should be configured?

5. Should the system support custom system prompts or agent instructions, or use default behavior?

6. What should happen when a session's conversation history exceeds the token limit for the Gemini API? (Truncate from beginning, summarize, etc.)
