# Constitution

This document contains the non-negotiable principles that govern all development in this repository.

## Core Principles

### 1. Spec is the Source of Truth
The specification (spec.md) is the authoritative source for what should be built. Code must follow the spec, never the reverse. If code and spec conflict, the spec wins unless explicitly amended.

### 2. No Code Without an Accepted CP
No non-trivial code change may be made without an Accepted Change Proposal (CP). Trivial changes (see `workflow/lifecycle.md` for definition) may bypass this requirement.

### 3. Smallest Change That Satisfies the Spec
Implement the smallest change that satisfies the specification. Do not add unrequested refactors, optimizations, or "nice-to-haves" unless they are explicitly in the spec.

### 4. Every Requirement is Testable and Has a Unique ID
Every requirement in spec.md must be testable and must have a unique ID (e.g., REQ-001). Test coverage must trace back to specific requirement IDs.

### 5. Decisions Are Written Down
All significant decisions must be written down in the appropriate place:
- Proposal-level decisions in `proposal.md`
- Implementation decisions in `log.md`
- Architecture decisions in `knowledge/architecture/` (ADR format)
No decision should exist only in chat or conversation.

### 6. Humans Own Approvals
Humans must approve all transitions through gates (G1-G4 in lifecycle.md). Agents may prepare, review, and suggest, but never approve their own work.

### 7. Explicit Gates Must Be Passed
The CP lifecycle has explicit gates (G1-G4). Each gate must be explicitly passed before proceeding to the next state. See `workflow/lifecycle.md` for details.

### 8. One Plan Task at a Time
When implementing a plan, work on one task at a time. Commit after each task. Reference the CP ID, task ID, and requirement IDs in commit messages.

### 9. Never Silently Deviate
If the spec is ambiguous, wrong, or impossible, STOP. Document the issue in `log.md` under "Spec Amendment Request" and ask a human. Never silently deviate from the spec.

### 10. Never Edit Approved Documents
Never edit the content of an approved `proposal.md` or `spec.md`. Spec changes must go through an Amendment (new dated section + status bump) and require human approval.

## Violations

Violations of these principles are taken seriously. Repeated violations will result in loss of commit access. Agents that violate these principles should be reconfigured or replaced.

## Amendment Process

This constitution may only be amended by:
1. Creating a CP proposing the amendment
2. Following the full CP lifecycle
3. Explicit approval by the repository owner(s)

Last updated: 2026-11-02
