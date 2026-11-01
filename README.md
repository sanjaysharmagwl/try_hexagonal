# Idea Management System - Hexagonal Architecture

A FastAPI + Pydantic service for submitting ideas, built with hexagonal architecture and governed by a Change Proposal (CP) workflow.

## Quick Start

```bash
uv sync
uv run uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive docs are at `http://127.0.0.1:8000/docs`.

## Installation

Prerequisites: Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
# Install runtime and dev dependencies
uv sync

# Optional: install local pre-commit hooks (ruff format, ruff check, cp lint)
uvx pre-commit install
```

## Usage

Submit an idea:

```bash
curl -X POST http://127.0.0.1:8000/ideas \
  -H "Content-Type: application/json" \
  -d '{"title": "Dark mode", "description": "Add a dark theme", "author_id": "user-42"}'
```

Response (`201 Created`):

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

Request validation: `title` 1-200 chars, `description` up to 5000 chars (optional), `author_id` required. A domain rule violation (for example, a whitespace-only title) returns `422`.

Storage is in-memory, so data is lost on restart.

## API Documentation

FastAPI generates interactive API docs from the OpenAPI schema while the server runs: Swagger UI at `http://127.0.0.1:8000/docs` and ReDoc at `http://127.0.0.1:8000/redoc`.

## Project Structure

```
try_hexagonal/
├── main.py                 # Composition root: wires adapters to use cases
├── app/
│   ├── core/deps.py        # FastAPI dependency providers
│   └── ideas/
│       ├── models.py       # Domain: Idea entity, IdeaStatus, domain errors
│       ├── service.py      # Application: SubmitIdea use case
│       ├── repository.py   # Port (IdeaRepository) + in-memory adapter
│       ├── router.py       # HTTP adapter (POST /ideas)
│       └── schemas.py      # HTTP request/response models
├── tests/unit/             # Domain tests
├── harness/                # Constitution, standards, workflow, templates, prompts, checks
├── proposals/              # Change Proposals (CP-NNNN) and the CP template
├── tools/cp/               # `cp` CLI for the CP lifecycle
├── knowledge/              # Architecture decision records (ADRs)
└── .github/                # CI workflow and PR template
```

## Architecture

- **Domain** (`models.py`): `Idea` entity and business rules (title validation, status transitions)
- **Application** (`service.py`): use cases that depend only on ports
- **Adapters** (`router.py`, `repository.py`): HTTP routes and persistence implementations
- **Composition Root** (`main.py`): the only place where adapters are wired to use cases

Layering rules are enforced by `harness/checks/check_architecture.py`. See:

- `harness/standards/architecture.md` - layering and boundary rules
- `knowledge/architecture/index/` - architecture decision records (ADRs)

## Development Checks

Run all checks before opening a PR. CI runs the same checks, with pytest invoked as `uv run pytest --cov=app --cov=tools/cp --cov-report=term-missing`:

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
python3 tools/cp/cp lint
python3 harness/checks/run_all.py
```

## Contributing

Non-trivial changes go through the Change Proposal workflow:

```bash
python3 tools/cp/cp new "<title>"           # create a CP
python3 tools/cp/cp status <id> [<state>]   # check or change status
python3 tools/cp/cp lint [<id>]             # validate CP structure
python3 tools/cp/cp next <id>               # next unfinished task
```

Full command list: `proposals/README.md`. Gate transitions (G1-G4) require `--by <name>` and are run by a human approver, for example `python3 tools/cp/cp status <id> Accepted --by <name>`.

Lifecycle: Draft -> Proposed -> Accepted -> Specified -> Spec-Approved -> Planned -> In-Progress -> Implemented -> Closed. Gates G1-G4 require human approval.

Trivial changes (see `harness/workflow/lifecycle.md`) skip the CP but must carry the `trivial` PR label.

Start here:

- `AGENTS.md` - entry point for humans and coding agents
- `harness/README.md` - harness overview and read order
- `proposals/README.md` - CP index
- `proposals/0001-adopt-change-proposal-process/` - worked example
