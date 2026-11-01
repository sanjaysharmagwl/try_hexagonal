# Review Implementation Prompt

You are tasked with reviewing an implementation of a Change Proposal.

## Context

The implementation is complete. Your job is to verify that it meets the Definition of Done and the specification.

## Instructions

1. Read the CP's `proposal.md`, `spec.md`, `plan.md`, and `log.md`
2. Review the code changes
3. Verify against the Definition of Done
4. Provide feedback or approve

## Review Checklist

### Requirements Coverage
- [ ] Every REQ in spec.md has at least one corresponding test
- [ ] Every test can be traced back to a REQ ID
- [ ] Traceability matrix in plan.md is complete

### Code Quality
- [ ] All code passes ruff linting
- [ ] All code passes ruff formatting
- [ ] No new warnings introduced
- [ ] Code follows coding standards
- [ ] Code follows architecture standards

### Testing
- [ ] All tests pass (`pytest`)
- [ ] Coverage is at least 80% (or documented exception)
- [ ] New code has corresponding tests
- [ ] Edge cases are tested
- [ ] Tests follow testing standards

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

## Approval Criteria

You may approve if:
- All items in the checklist are satisfied
- Code quality is high
- Implementation matches spec
- No security issues
- No breaking changes without documentation

## Rejection Criteria

You must request changes if:
- Requirements are not fully implemented
- Tests are missing or inadequate
- Code quality issues exist
- Documentation is incomplete
- Security concerns present
- Deviations from spec without amendments

## Providing Feedback

When requesting changes:
- Be specific about what needs to change
- Reference specific files/lines
- Explain why the change is needed
- Provide suggestions if helpful

## Sign-Off

If approving, add to log.md:
```markdown
## DoD Sign-Off
**Date**: YYYY-MM-DD
**Reviewer**: [your name]
**Status**: PASSED
**Notes**: [any notes]
```

The CP can then transition to Closed.
