# Architecture Standards

This document defines the architectural principles and layering rules for this repository.

## Architectural Style

This project uses **feature-sliced layered architecture**. Each feature is a vertical slice (`ideas`) whose code is organized into layers. Dependencies flow downward only:

```
router -> schemas -> service -> repository -> models
```

## Packages

| Package | Location | Contents | May import |
|---------|----------|----------|------------|
| `core` | `packages/core` | models, service, repository — all business logic | stdlib + pydantic only. **Never** `api`, fastapi, starlette |
| `api` | `apps/api` | routers, schemas, deps, main — the HTTP entry point | `core`, fastapi |

## Layer Rules

| Layer | File | Responsibility |
|-------|------|----------------|
| router | `apps/api/src/api/<feature>/router.py` | HTTP only: request validation wiring, auth deps, status codes, response shaping. Delegates all logic to the service. Never imports `core.<feature>.repository`. |
| schemas | `apps/api/src/api/<feature>/schemas.py` | Pydantic request/response DTOs. Separate from domain models — API shape can drift from domain shape. |
| service | `packages/core/src/core/<feature>/service.py` | Business rules and orchestration. Plain class, plain args in / domain objects out. No FastAPI imports. |
| repository | `packages/core/src/core/<feature>/repository.py` | Persistence. A `Protocol` plus implementation(s); returns domain models. **Always present for every feature** — services never touch storage directly. |
| models | `packages/core/src/core/<feature>/models.py` | Domain entities, value objects, domain errors. stdlib + pydantic only. |

Dependencies point downward only: a layer may import the layers below it, never above.

## Wiring

Composition happens via FastAPI `Depends` providers in `apps/api/src/api/deps.py` — there is no app-state wiring and no separate composition root module:

```python
@lru_cache
def get_idea_repository() -> IdeaRepository:
    return InMemoryIdeaRepository()


def get_idea_service(repo: IdeaRepository = Depends(get_idea_repository)) -> IdeaService:
    return IdeaService(repo)
```

Tests swap implementations via `app.dependency_overrides` (see `apps/api/tests/test_ideas_api.py`).

## Simplicity Rules

- `Protocol` + `Depends` only for real external systems (payment, email, LLM, storage) and for repositories. No abstract ports/adapters hierarchy.
- No use-case/Command classes — a service method takes plain arguments.
- Services return domain models, never schemas or HTTP types.

## When to Go Further

Stay with this style until a real need appears. Consider richer architecture (separate ports/adapters modules, multiple apps, events) only when you have:

- Multiple entry points (HTTP + CLI + workers) sharing the same core
- Many swappable external integrations
- A complex domain that outgrows per-feature service classes

## Enforcement

Boundaries are enforced by import-linter contracts in the root `pyproject.toml` (`[tool.importlinter]`), run by `just arch` and as part of `just check`.

## How to Add a Feature/Endpoint

Copy `ideas` as the reference. For a feature named `widgets`:

1. `packages/core/src/core/widgets/models.py` — entities and domain errors
2. `packages/core/src/core/widgets/repository.py` — `WidgetRepository` Protocol + `InMemoryWidgetRepository`
3. `packages/core/src/core/widgets/service.py` — `WidgetService`
4. `apps/api/src/api/widgets/schemas.py` — request/response DTOs
5. `apps/api/src/api/widgets/router.py` — routes calling the service, catching `DomainError`
6. `apps/api/src/api/deps.py` — add `get_widget_repository` / `get_widget_service` providers
7. `apps/api/src/api/main.py` — `include_router`
8. Tests: `packages/core/tests/test_<thing>.py` for domain/service, `apps/api/tests/test_widgets_api.py` for HTTP

## Review Checklist

- [ ] Dependencies flow downward only (`just arch` passes)
- [ ] Router contains no business logic — only HTTP concerns
- [ ] Service has no FastAPI/starlette imports
- [ ] Every feature has a repository; services never touch storage directly
- [ ] Schemas are separate from domain models
- [ ] New providers live in `deps.py`; tests use `dependency_overrides`
