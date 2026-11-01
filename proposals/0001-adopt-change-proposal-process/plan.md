---
id: CP-0001
spec: CP-0001
status: Approved
---

# CP-0001 Plan: Adopt Change Proposal Process

## Approach & Architecture Notes

Docs-first bootstrap, then a stdlib-only CLI, then mechanical enforcement (checks + CI). The CP-0001 proposal documents the framework itself; gate approvals are recorded as bootstrap and pending human confirmation.

## Files in Scope

- `harness/` (create: constitution, stack, workflow/, standards/, templates/, prompts/, checks/)
- `proposals/` (create: README.md, 0000-template/, 0001-adopt-change-proposal-process/)
- `tools/cp/` (create: cp, cp.py, tests/test_cp.py)
- `tests/unit/test_domain.py` (moved from `test_domain.py`)
- `pyproject.toml`, `uv.lock`, `.gitignore` (modify)
- `README.md` (modify)
- `.github/workflows/ci.yml`, `.github/pull_request_template.md`, `.pre-commit-config.yaml` (create)
- `AGENTS.md`, `CLAUDE.md` (create)
- `app/`, `main.py` (style-only: ruff import sorting/formatting)

## Task List

### T-001: Harness docs and standards

- **Status**: done
- **Requirements**: REQ-001
- **Depends on**: none
- **Files**: harness/constitution.md, harness/stack.md, harness/README.md, harness/workflow/*, harness/standards/*, harness/prompts/*
- **Tests**: none (docs)
- **Done when**: docs reflect decided stack (ruff, GHA, pytest-cov, tests/, minimal pre-commit, no mypy)
- **Size**: M (<= 1 PR)
- **Description**: Author constitution, workflow, standards, prompts; fix lifecycle/agent-protocol; rewrite stale stack.md sections

### T-002: Parseable templates

- **Status**: done
- **Requirements**: REQ-002
- **Depends on**: T-001
- **Files**: harness/templates/*.md, proposals/0000-template/*
- **Tests**: test_templates_sync_ok, test_templates_sync_diverged
- **Done when**: templates carry front matter + required sections; 0000-template copies byte-identical plus log.md
- **Size**: S (<= 1 PR)
- **Description**: Restructure templates for machine parsing; create proposals/0000-template

### T-003: CP CLI

- **Status**: done
- **Requirements**: REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008
- **Depends on**: T-002
- **Files**: tools/cp/cp.py, tools/cp/cp, tools/cp/tests/test_cp.py, proposals/README.md
- **Tests**: test_new_creates_numbered_cp, test_gate_requires_by, test_closed_requires_dod_signoff, test_lint_duplicate_req, test_index_preserves_surrounding_text, test_next_respects_dependencies (and remaining cases in test_cp.py)
- **Done when**: all commands implemented and 29 CLI tests pass
- **Size**: M (<= 1 PR)
- **Description**: Rewrite the CLI with lifecycle enforcement, lint engine, index regeneration, and next-task selection

### T-004: Harness checks

- **Status**: done
- **Requirements**: REQ-009, REQ-011
- **Depends on**: T-002
- **Files**: harness/checks/*.py, harness/checks/tests/test_checks.py, harness/checks/README.md
- **Tests**: test_architecture_violation, test_banned_violations, test_secrets_violation, test_pr_reference_in_progress (and remaining cases in test_checks.py)
- **Done when**: all checks are AST/stdlib-based, importable, and green
- **Size**: M (<= 1 PR)
- **Description**: Rewrite checks with check(root) functions plus run_all.py

### T-005: Tooling and CI

- **Status**: done
- **Requirements**: REQ-010
- **Depends on**: T-003, T-004
- **Files**: pyproject.toml, uv.lock, .gitignore, tests/unit/test_domain.py, README.md, .github/workflows/ci.yml, .github/pull_request_template.md, .pre-commit-config.yaml
- **Tests**: full pytest suite (47 tests)
- **Done when**: ruff+pytest-cov configured, uv.lock committed, CI workflow and PR template defined
- **Size**: M (<= 1 PR)
- **Description**: Add ruff/pytest-cov config, move tests to tests/, wire GitHub Actions and pre-commit

### T-006: CP-0001 artifacts and entry point

- **Status**: done
- **Requirements**: REQ-001, REQ-012
- **Depends on**: T-005
- **Files**: proposals/0001-adopt-change-proposal-process/*, AGENTS.md, CLAUDE.md
- **Tests**: test_cannot_approve_without_review, test_review_then_approve (unchanged domain tests prove no behavior change)
- **Done when**: cp lint clean, index regenerated, AGENTS.md <60 lines, CLAUDE.md symlink
- **Size**: S (<= 1 PR)
- **Description**: Write the CP-0001 proposal/spec/plan/log and the AGENTS.md entry point

## Traceability Matrix

| REQ | Task(s) | Test(s) |
|-----|---------|---------|
| REQ-001 | T-001, T-006 | manual: harness tree exists |
| REQ-002 | T-002 | test_templates_sync_ok, test_templates_sync_diverged |
| REQ-003 | T-003 | test_new_creates_numbered_cp, test_new_second_cp_gets_0002 |
| REQ-004 | T-003 | test_gate_requires_by, test_invalid_transition_rejected, test_closed_requires_dod_signoff, test_deferred_reopen_and_superseded |
| REQ-005 | T-003 | test_spec_requires_accepted, test_spec_and_plan_scaffold |
| REQ-006 | T-003 | test_lint_duplicate_req, test_lint_req_missing_from_matrix, test_lint_task_without_req, test_lint_unknown_req_referenced, test_lint_broken_link, test_lint_bad_history_chain, test_lint_status_consistency |
| REQ-007 | T-003 | test_index_preserves_surrounding_text |
| REQ-008 | T-003 | test_next_respects_dependencies, test_next_all_done, test_next_warns_when_not_in_progress |
| REQ-009 | T-004 | test_architecture_ok, test_banned_ok, test_secrets_ok, test_templates_sync_ok |
| REQ-010 | T-005 | CI workflow definition (ci.yml) |
| REQ-011 | T-004 | test_pr_reference_in_progress, test_pr_reference_wrong_status, test_pr_reference_trivial_label |
| REQ-012 | T-006 | test_cannot_approve_without_review, test_review_then_approve |

## Rollout / Migration / Rollback

Documentation and tooling only; rollback = revert the commits. `test_domain.py` was moved to `tests/unit/` unchanged.

## Verification Steps

```bash
uv run ruff format --check .
uv run ruff check .
uv run pytest --cov=app --cov=tools/cp
python3 tools/cp/cp lint
python3 harness/checks/run_all.py
```
