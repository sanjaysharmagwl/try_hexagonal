# Definition of Done

This document defines the checklist that must be satisfied before a CP can be closed.

## DoD Checklist

A CP is considered "done" only when ALL of the following are satisfied:

### Requirements Coverage
- [ ] Every REQ in spec.md has at least one corresponding test
- [ ] Every test can be traced back to a REQ ID
- [ ] Traceability matrix in plan.md is complete

### Code Quality
- [ ] All code passes ruff linting
- [ ] All code passes ruff formatting
- [ ] No new warnings introduced

### Testing
- [ ] All tests pass (`pytest`)
- [ ] Coverage does not decrease relative to `main` (80% overall target <!-- inferred: confirm -->)
- [ ] New code has corresponding tests
- [ ] Edge cases are tested

### Documentation
- [ ] README.md is updated if user-facing changes
- [ ] API documentation is updated if API changes
- [ ] Inline documentation (docstrings) follows Google format
- [ ] Architecture documentation updated if structural changes
- [ ] Migration guide included if breaking changes

### Harness Checks
- [ ] All checks in `harness/checks/` pass
- [ ] `cp lint <id>` passes without errors
- [ ] No new security vulnerabilities introduced

### Process Artifacts
- [ ] log.md is complete with:
  - All implementation decisions
  - Any deviations from spec (with amendments)
  - Verification results from each task
  - Rollback notes if applicable
- [ ] No TODOs without linked CP
- [ ] All open questions from proposal are resolved

### Verification
- [ ] Verification steps in plan.md all pass
- [ ] Manual testing (if required) is documented
- [ ] Reviewer has signed off

### Review
- [ ] At least one human reviewer has approved
- [ ] Reviewer confirms DoD is met
- [ ] All reviewer feedback addressed

## DoD Exceptions

Exceptions to DoD must be:
1. Documented in the CP's plan.md
2. Approved by the reviewer
3. Exceptionally rare

Common exceptions:
- Legacy code that cannot reach the coverage target
- Documentation for internal-only features
- Experimental features marked as such

## Sign-Off

When DoD is met, the reviewer adds to log.md:
```markdown
## DoD Sign-Off
**Date**: YYYY-MM-DD
**Reviewer**: [name]
**Status**: PASSED
**Notes**: [any notes]
```

The CP can then transition to Closed.
