# Checks

Executable enforcement of `harness/standards/`. Each check exposes `check(root) -> list[str]`, runs standalone (`python3 harness/checks/<file>.py`, exit 0/1), and is stdlib-only.

| Check | Enforces | What it checks |
|-------|----------|----------------|
| `check_architecture.py` | `standards/architecture.md` | Layering under `app/<feature>/`: models.py only stdlib/pydantic/self; service.py no fastapi/starlette or app.*.router/schemas/core; repository.py no fastapi/starlette; router.py no app.*.repository; nothing imports `main` |
| `check_banned_patterns.py` | `standards/coding.md` | Wildcard imports, bare `except:`, `print()`/`breakpoint()`/pdb in `app/` and `main.py` |
| `check_secrets.py` | `standards/security.md` | Private keys, AWS key ids, hardcoded credential assignments in tracked files (skips `uv.lock`, binaries) |

## Run all local checks

```bash
python3 harness/checks/run_all.py
```

`run_all.py` runs every `check_*.py`.

## Adding a check

1. Create `check_<name>.py` with a `check(root) -> list[str]` function and a standalone `main()`
2. Document it above
3. Add unit tests in `tests/test_checks.py`
