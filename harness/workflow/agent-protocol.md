# Agent Protocol

This document defines the rules of engagement for coding agents working in this repository.

## Mandatory Pre-Task Checklist

Before starting ANY task, an agent MUST:

1. Read `AGENTS.md` (at repository root)
2. Read `harness/README.md`
3. Read `harness/constitution.md`
4. Read relevant `harness/standards/` files for the task
5. Read the CP's `proposal.md`, `spec.md`, and `plan.md`
6. Verify the CP status is `In-Progress`

If any of these checks fail, the agent MUST STOP and ask for clarification.

## Implementation Rules

### 1. Read Before Acting
Read order: `AGENTS.md` (root) -> `harness/README.md` -> `harness/constitution.md` -> the `harness/standards/` files relevant to the task. Then read the CP's `proposal.md`, `spec.md`, and `plan.md`.

### 2. Only Implement from Approved Plans
Only implement tasks from a plan whose CP status is `In-Progress`. Never implement from a Draft, Proposed, Specified, Spec-Approved, or Planned CP.

### 3. One Task at a Time, Commit Per Task
Work on one plan task at a time. Complete it fully (including tests) before moving on. Commit after each task; commit messages must reference the CP ID, task ID, and requirement IDs (e.g. `feat: add approval flow (CP-0001, T-003, REQ-002)`). The full commit format is defined in `harness/standards/git.md` — it is the single source of truth.

### 4. Spec Ambiguity Protocol
If the spec is ambiguous, wrong, or impossible: STOP, append a "Spec Amendment Request" entry to the CP's `log.md` (under `## Spec Amendment Requests`), and ask a human. Do NOT proceed until resolved.

### 5. Never Edit Approved Documents
Never edit the content of an approved `proposal.md` or `spec.md`. Amendments happen only as a new dated section plus a status bump, and require human approval.

### 6. Run All Checks Before Declaring Done
Before declaring a task complete, run all harness checks (`python3 harness/checks/run_all.py`), tests, and ruff, and paste the results in `log.md` under "Verification Results".

### 7. Stay in Scope
Only touch files listed in the plan's "Files in Scope". If you must touch other files, log the reason in `log.md` first.

### 8. Never Fabricate
Never fabricate test results, dependencies, APIs, documentation, or anything else. All work must be based on reality.

### Gate Approvals
Agents never pass `--by` for a gate transition (G1-G4) on their own work — gate approval is human-only (see `tools/cp` and `workflow/lifecycle.md`).

## Communication

### When to Ask a Human
Ask a human when:
- Spec is ambiguous or impossible
- Plan seems contradictory
- You need to touch files outside scope
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
- [ ] All REQs covered by the task have corresponding tests
- [ ] All tests pass
- [ ] All harness checks pass
- [ ] log.md is updated with implementation notes
- [ ] Commit message references CP, Task, and REQ IDs
- [ ] Files in scope match the plan

## Common Mistakes to Avoid

1. **Skipping the pre-task checklist** - This is the most common error. Always read the constitution and standards first.

2. **Working on multiple tasks at once** - Complete one task fully before starting the next.

3. **Not committing per task** - Commit after each task, not at the end.

4. **Silently deviating from spec** - If the spec is wrong, document it and ask. Don't just "fix it."

5. **Editing approved docs** - Never edit proposal.md or spec.md. Use the amendment process.

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
