# Implement Task Prompt

You are tasked with implementing a specific task from an approved implementation plan.

## Pre-Task Checklist

Before starting, you MUST:
1. Read `AGENTS.md` (repository root)
2. Read `harness/README.md`
3. Read `harness/constitution.md`
4. Read relevant `harness/standards/` files
5. Read the CP's `proposal.md`, `spec.md`, and `plan.md`
6. Verify the CP status is `In-Progress`

STOP if any of these checks fail.

## Task Information

You are implementing:
- CP: CP-XXXX
- Task: T-YYY
- Requirements: REQ-ZZZ, REQ-AAA

Read the task description in plan.md for full details.

## Implementation Steps

1. **Understand the Requirements**
   - Read the relevant REQs in spec.md
   - Understand the acceptance criteria
   - Clarify any ambiguities (ask if needed)

2. **Write Tests First**
   - Write tests based on acceptance criteria
   - Ensure tests fail initially
   - Tests should be clear and descriptive

3. **Implement the Code**
   - Write the minimal code to pass tests
   - Follow coding standards (`harness/standards/coding.md`)
   - Follow architecture standards (`harness/standards/architecture.md`)
   - Stay within the task's "Files in scope"

4. **Verify**
   - Run all tests
   - Run linter (`ruff check .`)
   - Run formatter (`ruff format .`)
   - Run any harness checks

5. **Commit**
   - Commit with proper message format
   - Include CP, Task, and REQ IDs
   - Example: `feat: add idea validation (CP-0001, T-001, REQ-001)`

6. **Update log.md**
   - Add implementation notes
   - Document any decisions
   - Add verification results

## Rules

### DO
- Commit after each task
- Reference CP, Task, and REQ IDs in commits
- Write tests first
- Stay in scope
- Run all checks before declaring done
- Update log.md

### DON'T
- Work on multiple tasks at once
- Skip the pre-task checklist
- Edit approved proposal.md or spec.md
- Touch files outside scope without documenting
- Skip verification
- Fabricate test results

## If Spec is Ambiguous

If the spec is ambiguous, wrong, or impossible:
1. STOP immediately
2. Add to `log.md` under "Spec Amendment Request"
3. Ask a human for guidance
4. Do NOT proceed until resolved

## Verification Checklist

Before declaring the task done, verify:
- [ ] All REQs covered by tests
- [ ] All tests pass
- [ ] ruff check passes
- [ ] ruff format produces no changes
- [ ] Files in scope match plan
- [ ] log.md updated
- [ ] Commit message references CP, Task, REQ IDs

## Output

Complete the task and commit. Update log.md with verification results.
