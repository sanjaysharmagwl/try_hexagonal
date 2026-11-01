# Write Implementation Plan Prompt

You are tasked with writing an implementation plan (plan.md) for a spec-approved Change Proposal.

## Context

The specification has been approved. Now you need to create a detailed implementation plan that an agent (or human) can follow to implement the specification.

## Instructions

1. Read the approved spec.md carefully
2. Write plan.md using the template in `harness/templates/plan.md`
3. Break down the work into small, manageable tasks
4. Ensure complete traceability (REQ -> Task -> Test)
5. Define verification steps

## Plan Sections

### Approach & Architecture Notes
Describe the technical approach:
- Architecture decisions (why this approach?)
- Implementation strategy (phases, ordering)
- Reference relevant architecture standards

### Files in Scope
List ALL files that will be:
- Created
- Modified
- Deleted

Be explicit. Don't guess.

### Task List
Break down the work into tasks. Each task must:
- Have a unique ID (T-001, T-002, etc.)
- Have a clear description
- List requirements covered (REQ-XXX)
- List dependencies (other task IDs)
- List files touched
- List tests to add
- Define "done when" criteria
- Be small enough for one PR (< ~200 lines changed)

Example:
```
## T-001: Create Idea Domain Entity

**Description**: Create the Idea domain entity with title validation.

**Requirements Covered**:
- REQ-001
- REQ-002

**Dependencies**: None

**Files Touched**:
- `app/ideas/models.py` (create)
- `tests/unit/test_models.py` (create)

**Tests to Add**:
- `test_idea_rejects_empty_title`
- `test_idea_trims_whitespace_from_title`
- `test_idea_accepts_valid_title`

**Done When**:
- [ ] Idea entity created with Pydantic model
- [ ] Title validation implemented
- [ ] All tests pass
- [ ] Code reviewed

**Size**: Small
```

### Traceability Matrix
Create a matrix mapping:
- REQ -> Task(s) -> Test(s)

Every REQ must map to at least one task and one test.

### Rollout / Migration / Rollback
Define:
- How to deploy (staging, canary, etc.)
- Data migration steps (if needed)
- Rollback procedure (if something goes wrong)

### Verification Steps
List exact commands to verify the implementation:
- Test commands
- Lint commands
- Manual testing steps

## Quality Checklist

Before submitting, verify:
- [ ] Approach is clear and justified
- [ ] Files in scope are complete
- [ ] Every task is small and focused
- [ ] Every task references at least one REQ
- [ ] Every REQ maps to at least one task
- [ ] Traceability matrix is complete
- [ ] Rollback plan exists (if applicable)
- [ ] Verification steps are defined
- [ ] Tasks are ordered by dependencies

## Output

Create the plan file at `proposals/XXXX-slug/plan.md`.

Run `cp lint <id>` to validate before submitting for approval.
