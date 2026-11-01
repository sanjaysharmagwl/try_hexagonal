# 0001. Adopt hexagonal architecture for domain applications

- **Status:** Accepted
- **Date:** 2026-11-01
- **Deciders:** Engineering team
- **Related:** docs/hexagonal-architecture-team-guide.md, ADR 0002, ADR 0003

## Context

Our domain applications, starting with the idea management system, contain
non-trivial business rules: idea status transitions, voting eligibility, and
approval permissions. FastAPI is our delivery mechanism, but we expect additional
entry points (CLI tools, message consumers) and possible changes to persistence.

Coupling rules to FastAPI and the ORM makes them slow to test, hard to reuse, and
tangled with infrastructure changes. Conversely, the team is new to this style,
and a fully layered approach adds files and indirection to simple CRUD parts.

## Decision

We will structure domain applications using hexagonal architecture:

- Domain code (entities, value objects, domain errors) has no framework imports.
- Use cases in the application layer depend only on the domain and on ports.
- Inbound adapters (HTTP, CLI) and outbound adapters (persistence, external services)
  implement or call those ports.
- Ports are created where there is real volatility or a need for test fakes, not for
  every class.
- Concrete adapters are wired in one composition root per application.

The terminology in code and documentation follows the team guide. Equivalent
FastAPI-common names are documented for external readers.

## Consequences

Easier:
- Business rules are testable without HTTP or a database.
- Infrastructure can be replaced without rewriting rules.
- New entry points reuse existing use cases.

Harder:
- More files and mapping code, especially for simple features.
- The team needs onboarding (the team guide and the FAQ) before productive use.
- Developers must resist putting logic in routes or leaking ORM models into the domain.

Follow-up:
- Add an import-linter rule enforcing the dependency direction.
- Review the adoption after two months; record changes as new ADRs.

## Alternatives considered

- **Layered architecture (routers, services, repositories):** simpler, but rules
  end up in services and entities become data holders. Rejected for long-lived
  domain logic, but still suitable for simple CRUD parts (see ADR 0002).
- **Framework-driven structure (plain FastAPI conventions only):** fastest to start,
  but ties business rules to HTTP and the ORM. Rejected because testability and
  reuse were priorities.