# Stack Overview

This document captures the technical stack and conventions for the Idea Management System.

## Language & Runtime

- **Language**: Python 3.12+ (project requires >=3.12, local runtime is 3.13.5)
- **Package Manager**: uv workspace (root is a virtual project)
- **Virtual Environment**: .venv (managed by uv)
- **Task Runner**: just (`just --list` for recipes)

## Dependencies

### Workspace Members
- **api** (`apps/api`): `fastapi[standard]`, `core` (workspace)
- **core** (`packages/core`): `pydantic` only — no web framework

### Development Dependencies (root dev group)
- **pytest**: Test runner
- **pytest-cov**: Coverage plugin
- **ruff**: Linter and formatter
- **pyright**: Type checker
- **import-linter**: Architecture boundary enforcement

## Project Structure

```
try_hexagonal/
├── pyproject.toml              # Workspace root + tooling config (ruff, pytest, pyright, importlinter)
├── justfile                    # just check = definition of done
├── apps/api/                   # HTTP entry point package
│   ├── src/api/
│   │   ├── main.py             # create_app() + app; includes routers
│   │   ├── deps.py             # Depends providers (composition via DI)
│   │   └── ideas/              # router.py, schemas.py
│   └── tests/test_ideas_api.py
├── packages/core/              # Business logic package (no fastapi)
│   ├── src/core/ideas/         # models.py, service.py, repository.py
│   └── tests/                  # test_domain.py, test_service.py
├── docs/                       # Standards, workflow, checks
│   ├── standards/, workflow/
│   ├── checks/                 # run_all.py, check_*.py
│   └── architecture.md         # ADRs
└── openspec/                   # Specs and changes
```

## Architecture Pattern

**Feature-sliced layered architecture** (see `docs/standards/architecture.md`, ADR-001 in `docs/architecture.md`):

- Layers: router -> schemas -> service -> repository -> models
- `core` may never import `api`, fastapi, or starlette — enforced by import-linter contracts (`just arch`)
- Wiring via FastAPI `Depends` providers in `apps/api/src/api/deps.py`; tests use `app.dependency_overrides`
- No use-case/Command classes; services are plain classes with plain arguments
- Repository is currently in-memory (no persistence layer)

## Testing

- **Test Runner**: pytest with `--import-mode=importlib`
- **Test Locations**: `packages/core/tests/` (domain/service), `apps/api/tests/` (HTTP), `docs/checks/tests/` (tooling)
- **Coverage**: `just cov` (`--cov=core --cov=api`); must not decrease

## Code Quality Tools

- **ruff**: Linter and formatter (E, F, I, B, UP; B008 ignored for FastAPI `Depends`; line-length 100; target py312)
- **pyright**: Type checker, `typeCheckingMode = "standard"`, includes `apps` and `packages`
- **import-linter**: Boundary contracts in root `pyproject.toml`
- **pre-commit**: Minimal local hooks (ruff format, ruff check, `openspec validate` on `openspec/` changes); install via `just hooks`

## CI/CD

- **GitHub Actions** (`.github/workflows/ci.yml`):
  - `checks` job: `uv sync --all-packages --locked`, then `just lint types arch cov spec harness`
- Coverage must not decrease; 80% overall target <!-- inferred: confirm -->

## Documentation

- **README.md**: Project overview, setup instructions, API usage
- **docs/architecture.md**: Architecture decision records (ADRs)
- **No CONTRIBUTING.md**: Open Question - should be added

## Build & Run Commands

```bash
just setup       # uv sync --all-packages
just dev         # dev server
just test        # pytest
just cov         # pytest with coverage
just lint        # ruff format --check + ruff check
just types       # pyright
just arch        # lint-imports
just spec        # openspec validate --all --strict
just harness     # docs/checks/run_all.py
just check       # all of the above = "done"
```

## Git

- Repository initialized; `main` is the default branch
- `uv.lock` is committed (reproducible installs and audits)
- Branch naming: `<change-name>` (kebab-case, matching `openspec/changes/<change-name>`); commit format: `<type>: <subject> (<change-name>)`
- See `docs/standards/git.md` for the full conventions

## Conventions Inferred

### Code Style
- **Naming**: PascalCase for classes (Idea, IdeaService), snake_case for functions/variables
- **Type Hints**: Extensive use of type hints (Python 3.12+ style), checked by pyright
- **Domain Errors**: Custom exception hierarchy (DomainError -> specific errors)
- **Validation**: Pydantic validators for domain rules

### Error Handling
- Domain errors raised as exceptions; pydantic `field_validator` exceptions that are not `ValueError` propagate unwrapped
- HTTP layer catches DomainError and returns 422 Unprocessable Entity
- Status transitions validated at domain level

### Dependency Injection
- FastAPI `Depends` providers in `deps.py` (lru_cached repository)
- Services depend on repository Protocols
- Tests override providers via `app.dependency_overrides`

## Resolved Questions

1. **Linting/Formatting**: ruff (confirmed)
2. **Type checking**: pyright, standard mode (adopted)
3. **CI/CD**: GitHub Actions (confirmed)
4. **Git**: Repository initialized, branching strategy to be defined in git.md
5. **Coverage**: pytest-cov via `just cov`
6. **Test Organization**: Tests live next to their package (`packages/core/tests`, `apps/api/tests`)
7. **Pre-commit**: Minimum pre-commit hooks configured
8. **Documentation Standards**: Google docstring format (most popular)

## Assumptions

- ruff rule set chosen (E, F, I, B, UP); B008 ignored for FastAPI `Depends`

## Remaining Open Questions

- Coverage threshold (80% is provisional) <!-- inferred: confirm -->
- Branch protection for `main` must be configured in the GitHub UI (cannot be done from the repo)
