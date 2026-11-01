---
id: CP-0001
title: Adopt Change Proposal Process
author: sanjaysharmagwl
status: Implemented
created: 2026-11-02
updated: 2026-11-02
supersedes:
superseded_by:
tags: [process, tooling]
---

# CP-0001: Adopt Change Proposal Process

## Summary

Adopt a Change Proposal (CP) workflow for this repository: a `harness/` of standards and templates, a `tools/cp` CLI that mechanically enforces the lifecycle, executable checks, and CI wiring — with no change to application behavior.

## Motivation / Problem

The repository had no change-management process, no lint/format/CI tooling, no test layout, and no guardrails for agent-authored changes. Decisions lived only in conversation.

## Goals

- Define the CP lifecycle (Draft -> ... -> Closed) with explicit gates G1-G4
- Provide parseable templates and a CLI that enforces transitions, preconditions, and `--by` human gates
- Enforce standards mechanically via `harness/checks/` and GitHub Actions
- Require non-trivial PRs to reference an In-Progress CP
- Make zero application-behavior changes

## Non-Goals

- Changing any application code behavior
- Adopting a type checker (mypy) — candidate for a future CP
- Branch protection configuration (must be done in the GitHub UI)

## Proposed Solution

A documentation-plus-tooling framework:

- `harness/`: constitution, workflow (lifecycle, roles, agent protocol, DoD), standards, templates, prompts, checks, stack doc
- `proposals/`: CP directories based on `0000-template`, auto-generated index
- `tools/cp`: stdlib-only CLI (`new`, `status`, `spec`, `plan`, `lint`, `index`, `next`) enforcing the lifecycle
- `.github/workflows/ci.yml`: ruff, pytest+coverage, `cp lint`, harness checks, PR CP-reference rule
- `AGENTS.md` entry point (with `CLAUDE.md` symlink)

## Alternatives Considered

- Ad-hoc review without artifacts: rejected, no traceability
- Heavier external tools (e.g. a bespoke service): rejected, over-engineered for one repo

## Impact

### Users
Contributors and agents must follow the CP workflow for non-trivial changes.

### Data
None — markdown artifacts only.

### Security
New secret-scan check reduces risk of committed credentials.

### Performance
None at runtime; CI adds a few minutes per PR.

### Cost
GitHub Actions minutes (public-repo scale, negligible).

## Risks & Mitigations

- Process friction discourages contributions: `trivial` escape hatch defined in lifecycle
- `--by` is honor-system, not authentication: documented as such; human gates still required
- Bootstrap CP approves itself: all gate lines recorded as pending human confirmation

## Open Questions

- Final coverage threshold (80% is provisional)
- Whether to adopt mypy later

## Success Metrics

- `cp lint` and `run_all.py` green on the repo
- CI pipeline defined and passing
- Existing domain tests pass unchanged (no behavior change)
