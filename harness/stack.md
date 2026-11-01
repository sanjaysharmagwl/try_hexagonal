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
├── tests/                  # Test directory (currently empty)
├── test_domain.py          # Domain tests at root (to be moved to tests/)
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
- **Test Location**: Currently tests are at root (test_domain.py), tests/ directory exists but empty
- **Test Style**: pytest with plain assertions
- **Coverage**: No coverage tool configured
- **Current Tests**: Domain entity behavior tests (status transitions)

## Code Quality Tools

**Open Question**: No linting or formatting tools configured. Consider adding:
- **ruff**: Fast Python linter and formatter (recommended for modern Python projects)
- **mypy**: Static type checking (aligns with Pydantic/TypeScript-style development)
- **pre-commit**: Git hooks for automation

## CI/CD

**Open Question**: No CI/CD configured. Repository is not yet a git repository.
Consider:
- GitHub Actions (if using GitHub)
- GitLab CI (if using GitLab)
- Need to initialize git repository

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

# Run specific test file
uv run pytest test_domain.py
```

## Git

**Open Question**: Repository is not initialized as a git repository.
- No .gitignore at project root
- No branching strategy defined
- No commit conventions defined

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

- Repository will be initialized as a git repository during this CP workflow setup
- CI will be GitHub Actions (most common for GitHub-hosted repos, adjust if different)
- ruff will be adopted as the linter/formatter (modern, fast, all-in-one)
- mypy will be added for type checking (aligns with existing type hinting)
- Tests will be organized under tests/ directory following pytest conventions
- Open questions will be answered by humans during the CP-0001 approval process
