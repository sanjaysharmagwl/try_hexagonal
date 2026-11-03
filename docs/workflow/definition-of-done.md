# Definition of Done

This document defines the checklist that must be satisfied before an OpenSpec change can be considered complete.

## DoD Checklist

A change is considered "done" only when ALL of the following are satisfied:

### Tasks
- [ ] Every item in the change's `tasks.md` is checked off

### Requirements Coverage
- [ ] Every requirement/scenario in the change's spec deltas has at least one corresponding test
- [ ] Tests reference the requirement names they cover
- [ ] Edge cases are tested

### Code Quality
- [ ] `just lint` passes (ruff format check + ruff lint)
- [ ] `just types` passes (pyright)
- [ ] `just arch` passes (import-linter boundaries)
- [ ] No new warnings introduced

### Testing
- [ ] All tests pass (`just test`)
- [ ] Coverage does not decrease relative to `main` (80% overall target)
- [ ] New code has corresponding tests

### Documentation
- [ ] README.md is updated if user-facing changes
- [ ] API documentation is updated if API changes
- [ ] Inline documentation (docstrings) follows Google format
- [ ] Architecture documentation updated if structural changes
- [ ] Migration guide included if breaking changes

### Checks
- [ ] All checks in `docs/checks/` pass (`just harness`)
- [ ] `just spec` passes (`openspec validate --all --strict`)
- [ ] In short: `just check` is green
- [ ] No new security vulnerabilities introduced

### Process Artifacts
- [ ] No TODOs left without a linked change
- [ ] All open questions in the change's artifacts are resolved

### Review
- [ ] At least one human reviewer has approved the PR
- [ ] Reviewer confirms DoD is met
- [ ] All reviewer feedback addressed

### Archival
- [ ] When the change merges, it is archived so its delta specs are merged into `openspec/specs/` (`openspec archive <change>`)

## DoD Exceptions

Exceptions to DoD must be:
1. Documented in the change's artifacts
2. Approved by the reviewer
3. Exceptionally rare

Common exceptions:
- Legacy code that cannot reach the coverage target
- Documentation for internal-only features
- Experimental features marked as such
