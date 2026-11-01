---
id: CP-0001
---

# CP-0001 Log

## Status History

- 2026-11-02 created as Draft by sanjaysharmagwl
- 2026-11-02 Draft -> Proposed by sanjaysharmagwl
- 2026-11-02 Proposed -> Accepted by sanjaysharmagwl (bootstrap via task brief — pending confirmation) (G1)
- 2026-11-02 Accepted -> Specified by sanjaysharmagwl
- 2026-11-02 Specified -> Spec-Approved by sanjaysharmagwl (bootstrap via task brief — pending confirmation) (G2)
- 2026-11-02 Spec-Approved -> Planned by sanjaysharmagwl
- 2026-11-02 Planned -> In-Progress by sanjaysharmagwl (bootstrap via task brief — pending confirmation) (G3)
- 2026-11-02 In-Progress -> Implemented by sanjaysharmagwl

## Decisions

- Linter/formatter: ruff (rules E, F, I, B, UP; B008 ignored for FastAPI Depends)
- CI: GitHub Actions
- Coverage: pytest-cov; CI reports coverage, coverage must not decrease, 80% target provisional
- Tests moved into tests/ (testpaths: tests, tools/cp/tests, harness/checks/tests)
- Pre-commit: minimal local hooks only; installed via `uvx pre-commit install`
- Docstrings: Google style
- mypy NOT adopted — candidate for a future CP
- `cp status --by` is an honor-system human-gate record, not authentication
- ruff per-file-ignores for UP042 (StrEnum) and B904 (raise-from) in app/ to keep the no-behavior-change rule

## Deviations

- Added `[tool.ruff.lint.per-file-ignores]` for `app/ideas/models.py` (UP042) and `app/ideas/router.py` (B904): applying those ruff fixes would change application code beyond style, which the brief forbids.
- README.md corrected beyond the test command: project tree (`idea_system/` -> `app/` + `main.py`), run command (`uvicorn main:app`), removed stale editable-install line.
- Secret-scan check skips `harness/checks/tests/` (the check's own test files contain fixture secrets).

## Spec Amendment Requests

None.

## Verification Results

```
$ uv run ruff format --check .
59 files already formatted

$ uv run ruff check .
All checks passed!

$ uv run pytest --cov=app --cov=tools/cp -q
...............................................                          [100%]
================================ tests coverage ================================
______________ coverage: platform darwin, python 3.12.11-final-0 _______________

Name                        Stmts   Miss  Cover
-----------------------------------------------
app/__init__.py                 0      0   100%
app/core/__init__.py            0      0   100%
app/core/deps.py                4      4     0%
app/ideas/__init__.py           0      0   100%
app/ideas/models.py            35      2    94%
app/ideas/repository.py        11     11     0%
app/ideas/router.py            13     13     0%
app/ideas/schemas.py           14     14     0%
app/ideas/service.py           14     14     0%
tools/cp/cp.py                506     70    86%
tools/cp/tests/test_cp.py     266      0   100%
-----------------------------------------------
TOTAL                         863    128    85%
47 passed in 0.50s

$ python3 tools/cp/cp lint
0 problem(s)

$ python3 harness/checks/run_all.py
[PASS] check_architecture.py
[PASS] check_banned_patterns.py
[PASS] check_secrets.py
[PASS] check_templates_sync.py
all checks passed
```

## DoD Sign-Off

Status: PENDING
