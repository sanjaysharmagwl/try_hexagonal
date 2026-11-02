## OpenSpec Change

Change name: `<change-name>` (from `openspec/changes/<change-name>/`)

## Trivial?

- [ ] This is a trivial change (no OpenSpec change required — see `harness/constitution.md`)

## Definition of Done

- [ ] Every requirement/scenario in the change's spec deltas has a corresponding test
- [ ] All `tasks.md` items are checked off
- [ ] All tests pass (`uv run pytest`)
- [ ] `ruff format --check .` and `ruff check .` pass
- [ ] Coverage does not decrease
- [ ] `openspec validate --all --strict --no-interactive` passes
- [ ] `python3 harness/checks/run_all.py` passes
- [ ] Documentation updated where needed
