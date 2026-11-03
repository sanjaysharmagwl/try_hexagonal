# Architecture Decisions

## ADR-001: Feature-sliced layered architecture over hexagonal

**Status**: Accepted

**Context**: The project started with hexagonal architecture (ports and adapters):
use-case classes (`SubmitIdeaCommand`/`SubmitIdea`), an `app/core` wiring module,
and `app.state` composition in `main.py`. For a single-entry-point FastAPI app
with one feature, the ceremony cost more than it bought — Command objects wrapped
what is really a function call, and the ports/adapters vocabulary implied a
generality nobody needed yet.

**Decision**: Adopt feature-sliced layered architecture in a uv workspace.
Business logic lives in `packages/core` (models, service, repository — no web
framework); HTTP lives in `apps/api` (routers, schemas, deps, main). Each feature
is a slice whose layers flow downward: router -> service -> repository -> models.
Wiring uses FastAPI `Depends` providers in `deps.py`; tests override them via
`app.dependency_overrides`. Boundaries are enforced by import-linter contracts.

**Consequences**: Simpler code (a service class instead of use-case/Command
pairs), a real package boundary (`core` cannot import `fastapi` — checked in CI),
and room to add entry points later. Repositories and Protocols are retained only
where they pay for themselves: persistence and genuine external systems. If the
app grows multiple entry points or many swappable integrations, revisiting a
fuller ports/adapters split is a new decision, not a revert.
