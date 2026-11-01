# Architecture Standards

This document defines the architectural principles and layering rules for this repository.

## Architectural Style

This project uses **Hexagonal Architecture** (Ports and Adapters).

### Layers

```
┌─────────────────────────────────────────┐
│         Adapters (Inbound)             │
│      HTTP, CLI, Event Handlers         │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Application Layer               │
│         Use Cases / Services            │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│            Domain Layer                 │
│      Entities, Value Objects, Errors    │
└─────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│         Adapters (Outbound)              │
│    Database, External APIs, File System │
└─────────────────────────────────────────┘
```

## Dependency Rules

### Rule 1: Dependencies Point Inward
Inner layers must not depend on outer layers.

- Domain layer: No dependencies on other layers
- Application layer: Depends on Domain only
- Adapters: Depend on Application and Domain

### Rule 2: Use Interfaces for Outbound Dependencies
Application layer depends on interfaces (protocols), not implementations.

Example:
```python
# Good: Depends on protocol
class SubmitIdea:
    def __init__(self, ideas: IdeaRepository) -> None:
        self._ideas = ideas

# Bad: Depends on implementation
class SubmitIdea:
    def __init__(self, ideas: InMemoryIdeaRepository) -> None:
        self._ideas = ideas
```

### Rule 3: Domain is Pure
Domain layer contains:
- Entities (business objects)
- Value objects
- Domain errors
- Business rules

Domain layer does NOT contain:
- HTTP code
- Database code
- External API calls
- Framework-specific code

## Module Structure

```
app/
├── core/              # Shared application utilities
├── <feature>/         # Feature-specific modules
│   ├── models.py      # Domain entities
│   ├── service.py     # Use cases
│   ├── repository.py  # Repository interface + implementations
│   ├── router.py      # HTTP adapter (if applicable)
│   └── schemas.py     # DTOs for HTTP
└── main.py            # Composition root
```

## Composition Root

`main.py` is the composition root where:
- All dependencies are wired together
- Adapters are instantiated
- Application is assembled

No other file should instantiate adapters or use cases directly.

## Boundaries

### Cross-Feature Dependencies
Features should not depend on each other directly. Use:
- Shared domain entities in a common location
- Application services for coordination
- Events for loose coupling

### External Boundaries
All external dependencies must be wrapped in adapters:
- Database: Repository pattern
- HTTP clients: Adapter pattern
- File system: Adapter pattern

## Testing Architecture

### Unit Tests
- Test domain entities in isolation
- Test use cases with mock repositories
- No external dependencies

### Integration Tests
- Test adapters with real implementations
- Use test database/file system
- Not in domain layer

### End-to-End Tests
- Test through HTTP adapter
- Full stack
- Minimal, slow tests

## Anti-Patterns

### Forbidden
- Domain layer importing FastAPI/Flask/etc.
- Use cases directly calling database
- HTTP code in domain entities
- Circular dependencies between features
- Business logic in adapters

### Discouraged
- Large use cases (> 100 lines)
- Domain entities with many methods
- Tight coupling between features

## Review Checklist

When reviewing code, check:
- [ ] Dependencies point inward
- [ ] Domain layer has no external dependencies
- [ ] Interfaces used for outbound dependencies
- [ ] Composition root wires everything
- [ ] No cross-feature direct dependencies
- [ ] Adapters are thin (delegation only)
