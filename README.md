# Idea Management System - Hexagonal Architecture

A clean hexagonal architecture implementation using uv workspace pattern and Pydantic for domain modeling.

## Project Structure

```
try_hexagonal/
├── pyproject.toml              # Project configuration
├── main.py                     # Composition root (app entry point)
├── app/
│   ├── core/                   # Shared dependencies
│   └── ideas/                  # Ideas feature (models, service, repository, router, schemas)
└── tests/
    └── unit/                   # Domain tests
```

## Setup with uv

```bash
# Install dependencies
uv sync

```

## Running the Application

```bash
# Start the FastAPI server
uv run uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## Testing

```bash
# Run domain tests
uv run pytest
```

## API Usage

Submit an idea:

```bash
curl -X POST http://127.0.0.1:8000/ideas \
  -H "Content-Type: application/json" \
  -d '{"title": "Dark mode", "description": "Add a dark theme", "author_id": "user-42"}'
```

Response:

```json
{
  "id": "2690e2ce-f089-4018-9eda-2aa502dbb2d0",
  "title": "Dark mode",
  "description": "Add a dark theme",
  "author_id": "user-42",
  "status": "submitted",
  "created_at": "2026-11-01T03:46:50.494641Z"
}
```

## Architecture

- **Domain**: Core business logic (Idea entity, errors)
- **Application**: Use cases and ports (protocols)
- **Adapters**: HTTP routes, persistence implementations
- **Composition Root**: main.py wires everything together
