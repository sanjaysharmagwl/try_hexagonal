---
id: CP-0002
---

# CP-0002 Log

## Status History
- 2026-11-02 created as Draft by sanjaysharmagwl
- 2026-11-02 Draft -> Proposed
- 2026-11-02 Proposed -> Accepted by sanjaysharmagwl (G1)
- 2026-11-02 Accepted -> Specified
- 2026-11-02 Specified -> Spec-Approved by sanjaysharmagwl (G2)
- 2026-11-02 Spec-Approved -> Planned
- 2026-11-02 Planned -> In-Progress by sanjaysharmagwl (G3)


## Decisions

- Linear history via rebase-merge (preserves per-task commits)
- ADR 002 Deciders set to "Engineering team" per spec edge cases

## Deviations

None.

## Spec Amendment Requests

None.

## Verification Results

### T-001

```
$ rg -n '^## API Documentation' README.md && rg -n '/docs' README.md
53:## API Documentation
12:... `http://127.0.0.1:8000`. Interactive docs are at `http://127.0.0.1:8000/docs`.
16:... Python 3.12+ and [uv](https://docs.astral.sh/uv/).
55:... Swagger UI at `http://127.0.0.1:8000/docs` and ReDoc at `http://127.0.0.1:8000/redoc`.

$ rg -n 'proposals/README.md|--by|--cov=app --cov=tools/cp' README.md
92, 113, 123 matched (CI coverage command, --by note, CP index link)

$ ! rg -n 'knowledge/design' README.md
no match

$ uv run ruff format --check .   -> 65 files already formatted
$ uv run ruff check .          -> All checks passed!
$ uv run pytest -q             -> 47 passed in 0.28s
$ python3 tools/cp/cp lint     -> 0 problem(s)
$ python3 harness/checks/run_all.py -> all checks passed
```

### T-002

```
$ ls knowledge/architecture/template/adr.md && ! ls knowledge/architecture/template/ard.md
knowledge/architecture/template/adr.md
ls: knowledge/architecture/template/ard.md: No such file or directory

$ ! rg -n 'ard\.md|License' harness/standards/docs.md
no match

$ rg -n 'Deprecated' harness/standards/docs.md
168:- Status (Proposed, Accepted, Deprecated, Superseded by NNNN)

$ uv run ruff format --check .   -> 65 files already formatted
$ uv run ruff check .          -> All checks passed!
$ uv run pytest -q             -> 47 passed in 0.31s
$ python3 tools/cp/cp lint     -> 0 problem(s)
$ python3 harness/checks/run_all.py -> all checks passed
```

### T-003

```
$ ! rg -n '^app/$' harness/standards/architecture.md && rg -n '^├── app/' harness/standards/architecture.md
76:├── app/

$ rg -n 'cov=tools/cp' harness/standards/testing.md
95, 106, 143 matched

$ uv run pytest --collect-only -q tests/unit/test_domain.py::test_review_then_approve
1 test collected in 0.06s

$ uv run ruff format --check .   -> 65 files already formatted
$ uv run ruff check .          -> All checks passed!
$ uv run pytest -q             -> 47 passed in 0.28s
$ python3 tools/cp/cp lint     -> 0 problem(s)
$ python3 harness/checks/run_all.py -> all checks passed
```

### T-004

```
$ rg -n -i 'rebase' harness/standards/git.md && rg -n 'pull_request_template.md' harness/standards/git.md
117, 118, 119 (Linear History bullets), 159-160 (rebase alias) matched
80:Use `.github/pull_request_template.md`; GitHub applies it automatically ...

$ ! rg -n -i 'commit-msg|use merge commits' harness/standards/git.md
no match

$ uv run ruff format --check .   -> 65 files already formatted
$ uv run ruff check .          -> All checks passed!
$ uv run pytest -q             -> 47 passed in 0.31s
$ python3 tools/cp/cp lint     -> 0 problem(s)
$ python3 harness/checks/run_all.py -> all checks passed
```

## DoD Sign-Off

Status: PENDING
