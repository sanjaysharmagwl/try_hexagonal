# Agent Protocol

This document defines the rules of engagement for coding agents working in this repository.

## Mandatory Pre-Task Checklist

Before starting ANY task, an agent MUST:

1. Read `AGENTS.md` (at repository root)
2. Read `harness/README.md`
3. Read `harness/constitution.md`
4. Read relevant `harness/standards/` files for the task
5. Read the OpenSpec change's `proposal.md`, `design.md` (if present), spec deltas, and `tasks.md`

If any of these checks fail, the agent MUST STOP and ask for clarification.

## Implementation Rules

### 1. Read Before Acting
Read order: `AGENTS.md` (root) -> `harness/README.md` -> `harness/constitution.md` -> the `harness/standards/` files relevant to the task. Then read the change's `proposal.md`, `design.md`, spec deltas, and `tasks.md` under `openspec/changes/<name>/`.

### 2. Only Implement from a Change's tasks.md
Only implement tasks listed in an OpenSpec change's `tasks.md`. Never implement behavior that has no change artifacts.

### 3. One Task at a Time, Commit Per Task
Work on one `tasks.md` item at a time. Complete it fully (including tests) before moving on, and check it off (`- [x]`). Commit after each task; commit messages reference the change name (e.g. `feat: add approval flow (add-idea-approval)`). The full commit format is defined in `harness/standards/git.md` — it is the single source of truth.

### 4. Spec Ambiguity Protocol
If the spec is ambiguous, wrong, or impossible: STOP and ask a human. Record the resolution in the change's own artifacts. Do NOT proceed until resolved.

### 5. Stay in Scope
Only touch files the change covers. If you must touch other files, note the reason and ask first.

### 6. Run All Checks Before Declaring Done
Before declaring a task complete, run all repo checks: ruff format check, ruff lint, pytest, `openspec validate --all --strict`, and `python3 harness/checks/run_all.py`.

### 7. Never Fabricate
Never fabricate test results, dependencies, APIs, documentation, or anything else. All work must be based on reality.

## Communication

### When to Ask a Human
Ask a human when:
- Spec is ambiguous or impossible
- The change's artifacts seem contradictory
- You need to touch files outside the change's scope
- Tests fail and you're unsure why
- You encounter unexpected complexity
- You're not sure how to proceed

### When to Proceed Independently
Proceed independently when:
- Task is clear
- Spec is unambiguous
- Implementation path is straightforward
- You can verify your work with tests

## Verification

After completing a task, verify:
- [ ] Every requirement/scenario covered by the task has a corresponding test
- [ ] All tests pass
- [ ] All harness checks pass
- [ ] `tasks.md` item is checked off
- [ ] Commit message references the change name
- [ ] Files touched are within the change's scope

## Common Mistakes to Avoid

1. **Skipping the pre-task checklist** - This is the most common error. Always read the constitution and standards first.

2. **Working on multiple tasks at once** - Complete one task fully before starting the next.

3. **Not committing per task** - Commit after each task, not at the end.

4. **Silently deviating from spec** - If the spec is wrong, document it in the change and ask. Don't just "fix it."

5. **Editing main specs directly** - Specs under `openspec/specs/` only change via `openspec archive`. Update the change's delta specs instead.

6. **Forgetting checks** - Run all checks before declaring done.

7. **Fabricating results** - Never fake test results or anything else.

## Agent Quality Signals

Good agents:
- Read instructions before acting
- Ask when unsure
- Commit frequently with clear messages
- Update documentation
- Run verification steps
- Stay in scope

Poor agents:
- Skip reading
- Guess when unsure
- Commit at the end
- Leave TODOs
- Skip verification
- Wander out of scope
