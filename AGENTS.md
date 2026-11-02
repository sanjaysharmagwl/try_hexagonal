# Core
1. Ask, don't assume. If something is unclear, ask before writing a single line. Never make silent assumptions about intent, architecture, or requirements. When running unattended, pick the most reasonable interpretation, proceed, and record the assumption rather than blocking.

2. Implement the simplest solution for simple problems, better solutions for harder problems. Do not over-engineer or add flexibility that isn't needed yet. 

3. Don't touch unrelated code but please do surface bad code or design smells you discover with me so we can address them as a separate issue.

4. Flag uncertainty explicitly. If you're unsure about something, see point 1 above. If it makes sense to do so, conduct a small, localised and low-risk experiment and bring the hypothesis and results to me to discuss. Confidence without certainty causes more damage than admitting a gap.

# Usage

A hexagonal-architecture FastAPI + Pydantic app (`app/`, `main.py`) governed by an OpenSpec spec-driven workflow.

## OpenSpec workflow in 5 lines

1. Non-trivial changes need an OpenSpec change: propose via the `openspec-propose` skill (`.agents/skills/`), which writes `proposal.md`, `design.md`, spec deltas, and `tasks.md` under `openspec/changes/<name>/`
2. Implement via the `openspec-apply-change` skill: one `tasks.md` item at a time, check off `- [x]`, commit per task
3. Archive via the `openspec-archive-change` skill (`openspec archive <change>`), which merges delta specs into `openspec/specs/`
4. Trivial changes (see harness/constitution.md) skip the OpenSpec change but must still pass all checks
5. Baseline spec: `openspec/specs/ideas/spec.md`

## OpenSpec CLI

Install: `npm i -g @fission-ai/openspec@1.15.0` — the skills invoke `openspec` from PATH.

Key commands:

```bash
openspec list                 # list changes
openspec list --specs         # list specs
openspec show <change>        # inspect a change
openspec validate --all --strict --no-interactive
openspec archive <change>     # archive a completed change, merging its spec deltas
```

## Read order

Read `harness/README.md` first, then `harness/constitution.md`, then the `harness/standards/` files relevant to the task, then the change's `proposal.md`/`design.md`/spec deltas/`tasks.md`.

## Agent protocol (summary — full rules in harness/workflow/agent-protocol.md)

1. Follow the read order above before any task
2. Implement only tasks listed in a change's `tasks.md`
3. One task at a time; check it off; commit per task referencing the change name (format: harness/standards/git.md)
4. Ambiguity -> STOP, ask a human; record the resolution in the change's artifacts
5. Never edit `openspec/specs/` or archived changes directly — specs change only via `openspec archive`
6. Run all checks before done
7. Stay within the change's scope
8. Never fabricate results

## Checks

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest
openspec validate --all --strict --no-interactive
python3 harness/checks/run_all.py
```
