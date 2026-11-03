# Idea Management System

AI-Native app easy for an agent to understand, run and verify.

A feature-sliced layered FastAPI app in a uv workspace: business logic in `packages/core`, HTTP in `apps/api`.

## Project Structure

```
try_hexagonal/
├── pyproject.toml              # uv workspace root (tooling config)
├── justfile                    # just check = the definition of done
├── apps/
│   └── api/
│       ├── src/api/
│       │   ├── main.py         # create_app() + app; includes routers
│       │   ├── deps.py         # Depends providers (wiring)
│       │   └── ideas/          # HTTP slice: router.py, schemas.py
│       └── tests/              # API tests (TestClient + dependency_overrides)
├── packages/
│   └── core/
│       ├── src/core/ideas/     # models.py, service.py, repository.py
│       └── tests/              # domain + service tests
├── docs/                       # standards, workflow, checks (was harness/)
└── openspec/                   # spec-driven workflow
```

## Setup

```bash
# Install just (task runner) once:
brew install just        # or: uv tool install rust-just

just setup               # uv sync --all-packages
```

## Run

```bash
just dev                 # fastapi dev server at http://127.0.0.1:8000
```

## Test

```bash
just test                # all tests
just test -k submission  # subset
just cov                 # with coverage
```

## Done

```bash
just check               # lint, types, arch boundaries, tests, spec, docs/checks
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

Feature-sliced layers; dependencies flow downward only:

- **router** (`apps/api`) — HTTP only: validation wiring, status codes, response shaping
- **schemas** (`apps/api`) — Pydantic request/response DTOs
- **service** (`packages/core`) — business rules; plain class, no FastAPI
- **repository** (`packages/core`) — persistence Protocol + implementation
- **models** (`packages/core`) — domain entities and errors

Boundaries are enforced by import-linter (`just arch`). See `docs/standards/architecture.md` and `docs/architecture.md` (ADR-001).
