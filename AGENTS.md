# Core
1. Ask, don't assume. If something is unclear, ask before writing a single line. Never make silent assumptions about intent, architecture, or requirements. When running unattended, pick the most reasonable interpretation, proceed, and record the assumption rather than blocking.

2. Implement the simplest solution for simple problems, better solutions for harder problems. Do not over-engineer or add flexibility that isn't needed yet. 

3. Don't touch unrelated code but please do surface bad code or design smells you discover with me so we can address them as a separate issue.

4. Flag uncertainty explicitly. If you're unsure about something, see point 1 above. If it makes sense to do so, conduct a small, localised and low-risk experiment and bring the hypothesis and results to me to discuss. Confidence without certainty causes more damage than admitting a gap.

# Usage

A hexagonal-architecture FastAPI + Pydantic app (`app/`, `main.py`) governed by a Change Proposal (CP) workflow.

## CP workflow in 5 lines

1. Non-trivial changes need a CP: `python3 tools/cp/cp new "<title>"`
2. Lifecycle: Draft -> Proposed -> Accepted -> Specified -> Spec-Approved -> Planned -> In-Progress -> Implemented -> Closed
3. Gates G1-G4 are human approvals recorded via `cp status <id> <state> --by <name>`
4. Trivial changes (see harness/workflow/lifecycle.md) skip the CP but carry the `trivial` PR label
5. Worked example: `proposals/0001-adopt-change-proposal-process/`

## Read order

Read `harness/README.md` first, then `harness/constitution.md`, then the `harness/standards/` files relevant to the task.

## Agent protocol (summary — full rules in harness/workflow/agent-protocol.md)

1. Follow the read order above before any task
2. Implement only tasks whose CP status is `In-Progress`
3. One task at a time; commit per task referencing CP-XXXX, T-YYY, REQ-ZZZ (format: harness/standards/git.md)
4. Ambiguity -> STOP, log a Spec Amendment Request in log.md, ask a human
5. Never edit approved proposal.md/spec.md — amendments only, human-approved
6. Run all harness checks before done; paste results in log.md
7. Stay within the plan's "Files in Scope" or log why
8. Never fabricate results; never pass `--by` for a gate on your own work

## Checks

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
python3 tools/cp/cp lint
python3 harness/checks/run_all.py
```
