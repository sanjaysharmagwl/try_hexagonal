# Checks

Executable enforcement of `docs/standards/`. Each check exposes `check(root) -> list[str]`, runs standalone (`python3 docs/checks/<file>.py`, exit 0/1), and is stdlib-only.

Architecture layering is **not** a check here — it is enforced by import-linter contracts in the root `pyproject.toml` (run `just arch`).

| Check | Enforces | What it checks |
|-------|----------|----------------|
| `check_banned_patterns.py` | `standards/coding.md` | Wildcard imports, bare `except:`, `print()`/`breakpoint()`/pdb in `apps/*/src` and `packages/*/src` |
| `check_secrets.py` | `standards/security.md` | Private keys, AWS key ids, hardcoded credential assignments in tracked files (skips `uv.lock`, binaries) |

## Run all local checks

```bash
python3 docs/checks/run_all.py   # or: just harness
```

`run_all.py` runs every `check_*.py`.

## Adding a check

1. Create `check_<name>.py` with a `check(root) -> list[str]` function and a standalone `main()`
2. Document it above
3. Add unit tests in `tests/test_checks.py`
