# Stack Overview

This document captures the technical stack and conventions for the Idea Management System.

## Language & Runtime

- **Language**: Python 3.12+ (project requires >=3.12, local runtime is 3.13.5)
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
├── openspec/               # OpenSpec specs and changes
│   ├── specs/              # Baseline capability specs
│   └── changes/            # Active and archived changes
├── harness/                # Standards, workflow, checks
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
- **Test Location**: `tests/unit/` for domain/unit tests; `harness/checks/tests/` for tooling tests
- **Test Style**: pytest with plain assertions
- **Coverage**: pytest-cov, reported in CI (`--cov=app`); must not decrease
- **Current Tests**: Domain entity behavior tests (status transitions)

## Code Quality Tools

- **ruff**: Linter and formatter (selected rules: E, F, I, B, UP; B008 ignored for FastAPI `Depends`; line-length 100; target py312)
- **pytest-cov**: Coverage reporting (`--cov=app`)
- **pre-commit**: Minimal local hooks (ruff format, ruff check, `openspec validate` on `openspec/` changes); install via `uvx pre-commit install`
- Type checking (mypy) is not adopted — candidate for a future change

## CI/CD

- **GitHub Actions** (`.github/workflows/ci.yml`):
  - `checks` job: ruff format check, ruff lint, pytest with coverage, `openspec validate --all --strict`, `harness/checks/run_all.py`
- Coverage must not decrease; 80% overall target <!-- inferred: confirm -->

## Documentation

- **README.md**: Project overview, setup instructions, API usage
- **knowledge/**: Architecture documentation (mostly empty placeholders)
- **No CONTRIBUTING.md**: Open Question - should be added

## Build & Run Commands

```bash
# Install dependencies
uv sync

# Run development server
uv run uvicorn main:app --reload

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=app

# Lint and format
uv run ruff check .
uv run ruff format --check .

# OpenSpec and harness checks
openspec validate --all --strict --no-interactive
python3 harness/checks/run_all.py
```

## Git

- Repository initialized; `main` is the default branch
- `uv.lock` is committed (reproducible installs and audits)
- Branch naming: `<change-name>` (kebab-case, matching `openspec/changes/<change-name>`); commit format: `<type>: <subject> (<change-name>)`
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
3. **Git**: Repository initialized, branching strategy to be defined in git.md
4. **Coverage**: pytest-cov to be added
5. **Test Organization**: Tests will be moved to tests/ directory
6. **Pre-commit**: Minimum pre-commit hooks to be configured
7. **Documentation Standards**: Google docstring format (most popular)

## Assumptions

- ruff rule set chosen (E, F, I, B, UP); B008 ignored for FastAPI `Depends`
- Type checking (mypy) is not adopted — candidate for a future change

## Remaining Open Questions

- Coverage threshold (80% is provisional) <!-- inferred: confirm -->
- Branch protection for `main` must be configured in the GitHub UI (cannot be done from the repo)
