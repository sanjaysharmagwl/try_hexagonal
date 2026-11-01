# Stack Overview

This document captures the technical stack and conventions for the Idea Management System.

## Language & Runtime

- **Language**: Python 3.12+ (`requires-python = ">=3.12"`; CI uses 3.12)
- **Package Manager**: uv (modern Python package installer)
- **Virtual Environment**: .venv (managed by uv)

## Dependencies

### Core Dependencies
- **FastAPI**: Web framework for building APIs
- **Pydantic**: Data validation and domain modeling
- **Uvicorn**: ASGI server for running FastAPI

### Development Dependencies
- **pytest**: Test runner
- **pytest-cov**: Coverage plugin
- **ruff**: Linter and formatter

## Project Structure

```
try_hexagonal/
├── main.py                 # Composition root and app entry point
├── pyproject.toml          # Project configuration (uv-based)
├── uv.lock                 # Dependency lock file
├── app/                    # Application code
│   ├── core/               # Core dependencies (FastAPI dependency injection)
│   └── ideas/              # Ideas feature
│       ├── models.py       # Domain entities and errors
│       ├── service.py      # Use cases (application layer)
│       ├── repository.py   # Repository interface and in-memory implementation
│       ├── router.py       # HTTP adapter (FastAPI routes)
│       └── schemas.py      # API request/response DTOs
├── tests/                  # Test directory
│   └── unit/               # Unit tests (domain tests live here)
├── tools/cp/               # CP workflow CLI
├── harness/                # Standards, workflow, templates, checks
├── proposals/              # Change Proposals
└── knowledge/              # Architecture documentation
```

## Architecture Pattern

**Hexagonal Architecture** (Ports and Adapters):
- **Domain Layer**: Pure business logic with no external dependencies (app/ideas/models.py)
- **Application Layer**: Use cases orchestrate domain objects (app/ideas/service.py)
- **Adapters**: HTTP routes (inbound), repository implementations (outbound)
- **Composition Root**: main.py wires dependencies together

Key principles observed:
- Domain entities are plain Pydantic models with business rules
- Use cases depend on repository interfaces (protocol-based)
- HTTP layer only handles FastAPI concerns, delegates to use cases
- Repository is currently in-memory (no persistence layer)

## Testing

- **Test Runner**: pytest
- **Test Location**: `tests/unit/` for domain/unit tests; `tools/cp/tests/` and `harness/checks/tests/` for tooling tests
- **Test Style**: pytest with plain assertions
- **Coverage**: pytest-cov, reported in CI (`--cov=app --cov=tools/cp`); must not decrease
- **Current Tests**: Domain entity behavior tests (status transitions)

## Code Quality Tools

- **ruff**: Linter and formatter (selected rules: E, F, I, B, UP; B008 ignored for FastAPI `Depends`; line-length 100; target py312)
- **pytest-cov**: Coverage reporting (`--cov=app --cov=tools/cp`)
- **pre-commit**: Minimal local hooks (ruff format, ruff check, `cp lint` on proposals); install via `uvx pre-commit install`
- Type checking (mypy) is not adopted — candidate for a future CP

## CI/CD

- **GitHub Actions** (`.github/workflows/ci.yml`):
  - `checks` job: ruff format check, ruff lint, pytest with coverage, `cp lint`, `harness/checks/run_all.py`
  - `cp-reference` job (PRs only): verifies a non-trivial PR references an In-Progress CP
- Coverage must not decrease; 80% overall target <!-- inferred: confirm -->

## Documentation

- **README.md**: Project overview, quick start, API usage, checks, and contributing
- **knowledge/**: Architecture decision records (ADRs)
- **Contributing**: covered by the README Contributing section

## Build & Run Commands

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn main:app --reload

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=app --cov=tools/cp

# Lint and format
uv run ruff check .
uv run ruff format --check .

# CP tooling
python3 tools/cp/cp lint
python3 harness/checks/run_all.py
```

## Git

- Repository initialized; `main` is the default branch
- `uv.lock` is committed (reproducible installs and audits)
- Branch naming: `cp-XXXX-short-description`; commit format: `<type>: <subject> (CP-XXXX, T-YYY, REQ-ZZZ)`
- See `harness/standards/git.md` for the full conventions

## Conventions Inferred

### Code Style
- **Naming**: PascalCase for classes (Idea, SubmitIdea), snake_case for functions/variables
- **Type Hints**: Extensive use of type hints (Python 3.12+ style)
- **Domain Errors**: Custom exception hierarchy (DomainError -> specific errors)
- **Validation**: Pydantic validators for domain rules

### Error Handling
- Domain errors raised as exceptions
- HTTP adapter catches DomainError and returns 422 Unprocessable Entity
- Status transitions validated at domain level

### Dependency Injection
- FastAPI dependency injection for use cases
- Use cases depend on repository interfaces
- Composition root wires everything in main.py

## Resolved Questions

1. **Linting/Formatting**: ruff (confirmed)
2. **CI/CD**: GitHub Actions (confirmed)
3. **Git**: Repository initialized; branching and merge strategy defined in `standards/git.md`
4. **Coverage**: pytest-cov added; CI reports coverage
5. **Test Organization**: Tests moved to `tests/`
6. **Pre-commit**: Minimal local hooks configured in `.pre-commit-config.yaml`
7. **Documentation Standards**: Google docstring format (most popular)

## Assumptions

- CP-0001 bootstrap gate approvals are pending human confirmation
- ruff rule set chosen (E, F, I, B, UP); B008 ignored for FastAPI `Depends`
- `cp status --by` is an honor-system human-gate record, not authentication
- Type checking (mypy) is not adopted — candidate for a future CP
- Open questions will be answered by humans during the CP-0001 approval process

## Remaining Open Questions

- Coverage threshold (80% is provisional) <!-- inferred: confirm -->
- Branch protection for `main` must be configured in the GitHub UI (cannot be done from the repo)
- The `cp-reference` CI rule relies on the PR body/title/labels — it is advisory for edge cases it cannot see
