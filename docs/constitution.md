# Constitution

This document contains the non-negotiable principles that govern all development in this repository.

## Core Principles

### 1. Spec is the Source of Truth
The specifications under `openspec/specs/`, together with the delta specs of the active change under `openspec/changes/<name>/`, are the authoritative source for what should be built. Code must follow the spec, never the reverse. If code and spec conflict, the spec wins unless explicitly changed through an OpenSpec change.

### 2. No Code Without an OpenSpec Change
No non-trivial code change may be made without an OpenSpec change under `openspec/changes/`. Trivial changes may bypass this requirement. A change is trivial only if it is one of the following AND changes no behavior:
- Typo fix in documentation or comments
- Dependency patch-version bump
- Comment-only change
- `ruff format` / import-order-only change

Trivial changes must still pass all checks.

### 3. Smallest Change That Satisfies the Spec
Implement the smallest change that satisfies the specification. Do not add unrequested refactors, optimizations, or "nice-to-haves" unless they are explicitly in the spec.

### 4. Every Requirement is Testable and Has a Scenario
Every requirement in a spec must be testable and must have at least one WHEN/THEN scenario. Tests must reference the requirement name they cover.

### 5. Decisions Are Written Down
All significant decisions must be written down in the appropriate place:
- Proposal-level decisions in the change's `proposal.md`
- Implementation decisions in the change's artifacts (`design.md`, `tasks.md`)
- Architecture decisions in `docs/architecture.md` (ADR format)
No decision should exist only in chat or conversation.

### 6. One Task at a Time
When implementing a change, work on one `tasks.md` item at a time. Check it off when done. Commit after each task.

### 7. Never Silently Deviate
If the spec is ambiguous, wrong, or impossible, STOP and ask a human. Spec fixes go into the change's own artifacts — never silently deviate from the spec.

### 8. Specs Change Only Through Changes
Archived changes are immutable. Main specs under `openspec/specs/` change only by archiving a change's delta specs (`openspec archive`), never by direct edit.

## Violations

Violations of these principles are taken seriously. Repeated violations will result in loss of commit access. Agents that violate these principles should be reconfigured or replaced.

## Amendment Process

This constitution may only be amended through an OpenSpec change proposing the amendment, merged with the approval of the repository owner(s).

Last updated: 2026-11-02
