# Support AI — AI-Powered Customer Support Backend

A backend application built with **Python, FastAPI, PostgreSQL, SQLAlchemy, and Groq**, designed to explore production-oriented backend development and the integration of Large Language Models (LLMs) into customer support workflows.

Support AI provides REST APIs for managing support tickets, storing conversations, and generating AI-powered responses using conversation history.

This project is being developed incrementally as part of a hands-on AI engineering learning journey, with an emphasis on understanding backend architecture, database operations, LLM integration, and maintainable Python code.

> **Project Status:** Learning and development project. Core backend functionality, conversation persistence, and LLM integration have been implemented. Advanced AI capabilities are still being explored.

---

## Getting Started

### Prerequisites

Before running the application, make sure you have:

- Python 3.13 or later
- PostgreSQL
- [uv — Python Package Manager](https://docs.astral.sh/uv/)
- Git
- A Groq API key from the [Groq Console](https://console.groq.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/support_ai.git
cd support_ai
```

Replace `YOUR_USERNAME` with the repository owner's GitHub username.

### 2. Install Dependencies

The project uses **uv** for Python dependency and environment management.

```bash
uv sync
```

This creates or updates the project's virtual environment and installs the required dependencies.

### 3. Create a PostgreSQL Database

Make sure PostgreSQL is installed and running.

Create a database:

```sql
CREATE DATABASE sql_learning_test;
```

You can use a different database name if you prefer, provided your connection URL points to it.

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/sql_learning_test
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=openai/gpt-oss-120b
APP_NAME=Support API
```

Replace the following values:

- `YOUR_PASSWORD` — Your PostgreSQL password.
- `your_groq_api_key_here` — Your Groq API key.
- Database connection details — Update them if your PostgreSQL configuration differs.

The application uses **Pydantic Settings** to load configuration from environment variables.

`DATABASE_URL` uses the PostgreSQL `psycopg` driver.

`MODEL_NAME` should reference a model currently available through your Groq account.

**Security:** Never commit your actual `.env` file or API keys to GitHub.

Ensure your `.gitignore` includes:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

### 5. Apply Database Migrations

The project uses **Alembic** to manage database schema changes.

Run:

```bash
uv run alembic upgrade head
```

This applies the available database migrations to your configured PostgreSQL database.

### 6. Start the FastAPI Server

From the project root, run:

```bash
uv run uvicorn main:app --reload
```

The development server should start at:

http://127.0.0.1:8000

The `--reload` option automatically restarts the development server when Python files change.

### 7. Open the API Documentation

FastAPI automatically generates interactive API documentation.

**Swagger UI:**

http://127.0.0.1:8000/docs

**ReDoc:**

http://127.0.0.1:8000/redoc

**OpenAPI Schema:**

http://127.0.0.1:8000/openapi.json

These interfaces allow you to explore and test the application's endpoints.

---

## API Endpoints

### Conversation Endpoints

The conversation API includes the following routes:

| Method | Endpoint | Description |
|---|---|---|
| POST | `/conversations` | Create a conversation with an initial message |
| GET | `/conversations/{conversation_id}/messages` | Retrieve conversation history |
| POST | `/conversations/{conversation_id}/messages` | Add a user message to an existing conversation |
| POST | `/conversations/{conversation_id}/generate` | Generate and save an AI response |
| POST | `/conversations/{conversation_id}/chat` | Add a user message and generate an AI response |

### Support Ticket Endpoints

The application also includes REST endpoints for managing customer support tickets.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tickets/` | Create a new support ticket |
| GET | `/tickets/{ticket_id}` | Retrieve a support ticket by ID |

These endpoints use Pydantic schemas for request and response validation and SQLAlchemy for database operations.

### Example AI Conversation Workflow

A typical AI conversation follows these steps:

1. A client creates a conversation.
2. The application saves the conversation and its initial message in PostgreSQL.
3. The client sends a message to the chat endpoint.
4. The service stores the user's message.
5. Recent conversation history is retrieved from PostgreSQL.
6. The LLM service converts the history into Groq-compatible messages.
7. Groq generates an assistant response.
8. The application stores the generated response in PostgreSQL.
9. The API returns the response to the client.

This demonstrates how an LLM can be integrated into a **stateful backend application** rather than used as a standalone chatbot.

---

## Key Engineering Concepts

The project covers several foundational backend and AI engineering concepts.

### Backend Engineering

- REST API design
- HTTP methods and status codes
- Request and response validation
- Dependency injection
- Exception handling
- Layered application architecture
- Configuration management

### Database Engineering

- Relational data modeling
- SQLAlchemy ORM
- Database sessions and transactions
- Repository pattern
- PostgreSQL queries
- Schema migrations with Alembic

### LLM Engineering

- LLM API integration
- System and user messages
- Prompt engineering
- Few-shot prompting
- Conversation history
- Context management
- Token usage monitoring
- Structured output concepts

---

## Current Limitations

Support AI is an educational backend project and is not yet a production-ready customer support service.

Current limitations include:

- No implemented order-status tool-calling integration.
- No retrieval-augmented generation (RAG) pipeline.
- No complete user authentication and authorization system documented.
- No production deployment configuration.
- No comprehensive automated test suite.
- No frontend application.
- No integrated conversation summarization or structured ticket classification workflow.

The application should not be used with real customer data without additional security, privacy, reliability, and operational safeguards.

---

## Planned Improvements

Potential future enhancements include:

- LLM tool calling for verified backend operations
- Structured tool argument validation
- Streaming AI responses
- Retrieval-augmented generation (RAG)
- Semantic search using PostgreSQL and pgvector
- More advanced conversation context management
- AI evaluation and response-quality measurement
- Authentication and authorization
- Docker-based development and deployment
- Observability and inference cost monitoring

These are planned learning directions, not currently implemented features.

---

## Features

### 1. Support Ticket Management

A REST API for managing customer support tickets using a PostgreSQL database.

The application demonstrates:

- FastAPI route handlers
- Request and response validation using Pydantic
- SQLAlchemy ORM models
- Repository and service layers
- Database dependency injection
- Application-level exception handling

### 2. Conversation Management

Support for persistent customer support conversations.

Implemented concepts include:

- Creating conversations
- Storing user and assistant messages
- Retrieving conversation history
- Associating messages with conversations
- Maintaining chronological message order
- Persisting conversation data in PostgreSQL

### 3. LLM Integration with Groq

Integration with the Groq API for generating customer support responses.

Capabilities include:

- Sending messages to an LLM
- Configurable model selection
- System prompts for assistant behavior
- Few-shot prompting examples
- Conversation-aware response generation
- Basic token usage and completion metadata logging

The assistant is instructed not to fabricate order statuses, refund approvals, or other information that has not been verified.

### 4. Conversation Context Management

The application implements a basic conversation-history window to limit the number of messages sent to the LLM.

This demonstrates:

- Context-window management
- Retrieving recent messages efficiently
- Chronological ordering of retrieved messages
- Reducing unnecessary prompt tokens
- Understanding token usage and API costs

The current implementation uses a recent-message limit rather than a token-based context budget.

### 5. Additional AI Engineering Exercises

The project has also been used to explore standalone implementations of:

- Conversation summarization
- Structured LLM outputs
- Pydantic validation of generated JSON
- Ticket classification by category and priority
- Python generators and LLM streaming concepts

These exercises are not necessarily integrated into the main application endpoints.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Primary programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy 2.x | ORM and database interaction |
| Alembic | Database schema migrations |
| Pydantic v2 | Data validation and serialization |
| Pydantic Settings | Environment-based configuration |
| Groq API | LLM inference |
| Uvicorn | ASGI server |
| uv | Python dependency and environment management |

---

## Project Structure

```text
support_ai/
│
├── alembic/                    # Database migrations
├── alembic.ini                 # Alembic configuration
│
├── main.py                     # FastAPI application entry point
├── config.py                   # Application settings
├── database.py                 # Database engine and sessions
├── dependencies.py             # FastAPI dependencies
├── exceptions.py               # Exception handling
│
├── models.py                   # Support ticket ORM models
├── schemas.py                  # Pydantic schemas
├── repository.py               # Ticket database operations
├── service.py                  # Ticket business logic
├── routes.py                   # Ticket API routes
│
├── conversation_models.py      # Conversation and message models
├── conversation_repository.py  # Conversation database operations
├── conversation_service.py     # Conversation business logic
├── conversation_routes.py      # Conversation API routes
│
├── llm_service.py              # Groq integration and LLM utilities
│
├── test_llm_manual.py          # Manual LLM experimentation
│
├── .env                        # Local environment variables (not committed)
├── .gitignore
├── .python-version
├── pyproject.toml              # Project dependencies
└── README.md
```

---

## Architecture

The application follows a layered backend architecture to separate HTTP handling, business logic, and database access.

```text
                  Client / Swagger UI
                           |
                           v
                    FastAPI Routes
                           |
                           v
                      Services
                      /      \
                     v        v
               Repositories  LLM Service
                     |        |
                     v        v
                SQLAlchemy   Groq API
                     |
                     v
                 PostgreSQL
```

**Routes:** Receive HTTP requests, validate input through Pydantic schemas, and return responses.

**Services:** Coordinate business logic, including database operations and AI response generation.

**Repositories:** Encapsulate database queries and persistence operations using SQLAlchemy.

**LLM Service:** Handles prompts, conversation formatting, Groq API calls, and response generation.

**Database Models:** Define relational data structures and relationships.

This separation makes the application easier to maintain and extend.

---

## Learning Objectives

This project is intended to develop practical experience in building backend systems that integrate LLM capabilities.

Rather than relying only on prompt engineering or simple API calls, the focus is on understanding how the complete system works:

- How requests flow through application layers
- How data is validated and persisted
- How conversations are represented in a relational database
- How LLM context is constructed
- How generated responses are stored
- How backend architecture supports future AI capabilities

The project will continue evolving as new AI engineering concepts are learned and implemented.

---

## License

No license has been specified yet. Unless a license is added, standard copyright restrictions apply.