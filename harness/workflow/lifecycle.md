# CP Lifecycle

This document defines the states, transitions, and gates for Change Proposals.

## State Diagram

```
                    Draft
                      |
                [Author proposes]
                      v
                   Proposed
                      |
              +-------+-------+
              |               |
          [Review]         [Withdraw]
              |               |
         +----+----+          v
         |         |      Withdrawn
    [Approved]  [Rejected]
         |         |
         v         v
    Accepted   Rejected
         |
    [Spec written]
         v
    Specified
         |
    [Review + Approver sign-off]
         v
    Spec-Approved
         |
    [Plan written]
         v
      Planned
         |
    [Plan lint + Human OK]
         v
    In-Progress
         |
    [Implementation complete]
         v
    Implemented
         |
    [DoD met + Reviewer sign-off]
         v
      Closed

    (Any state) -> Superseded (by a new CP)
```

## States

| State | Description | Who Can Transition To |
|-------|-------------|----------------------|
| Draft | Initial state, author is drafting | Author |
| Proposed | Ready for review | Author |
| Accepted | Proposal approved, ready for spec | Reviewer (via G1) |
| Specified | Spec written, ready for review | Author |
| Spec-Approved | Spec approved, ready for plan | Reviewer + Approver (via G2) |
| Planned | Plan written, ready for implementation | Author |
| In-Progress | Implementation in progress | Human (via G3) |
| Implemented | Implementation complete, ready for verification | Implementer |
| Closed | CP completed and verified | Reviewer (via G4) |
| Rejected | Proposal rejected | Reviewer |
| Deferred | Proposal deferred for later | Reviewer |
| Withdrawn | Author withdrew proposal | Author |
| Superseded | Replaced by a newer CP | Reviewer |

## Gates

### G1: Proposed -> Accepted
**Requirement**: Reviewer approval; all open questions resolved

**Before approval, reviewer must verify**:
- Motivation is clear and justified
- Goals are specific and achievable
- Non-goals are clearly defined
- Proposed solution is high-level (not implementation details)
- Alternatives considered
- Impact analysis is complete
- Risks have mitigations
- Open questions are resolved or documented as acceptable

### G2: Specified -> Spec-Approved
**Requirement**: Every REQ is testable; reviewer + approver sign-off

**Before approval, reviewer and approver must verify**:
- Every requirement has a unique ID (REQ-XXX)
- Every requirement uses MUST/SHOULD/MAY language
- Every requirement has acceptance criteria in Given/When/Then format
- Interfaces and data contracts are complete
- Error handling and edge cases are specified
- Non-functional requirements are documented
- Security implications are addressed
- Out-of-scope items are clearly listed

### G3: Planned -> In-Progress
**Requirement**: Plan lint passes; traceability complete; human OK

**Before approval, human must verify**:
- `cp lint <id>` passes without errors
- Every REQ maps to at least one task
- Every task references at least one REQ
- Traceability matrix is complete
- Files in scope are explicitly listed
- Rollback plan exists if applicable
- Verification steps are defined

### G4: Implemented -> Closed
**Requirement**: DoD met; checks green; reviewer sign-off

**Before approval, reviewer must verify**:
- All REQs are covered by tests
- All harness checks pass (see `checks/README.md`)
- Documentation is updated
- `log.md` is complete
- No TODOs without linked CP
- Verification steps in plan.md pass

## Valid Transitions

```
Draft -> Proposed
Draft -> Withdrawn
Proposed -> Accepted (via G1)
Proposed -> Rejected
Proposed -> Deferred
Proposed -> Withdrawn
Accepted -> Specified
Specified -> Spec-Approved (via G2)
Spec-Approved -> Planned
Planned -> In-Progress (via G3)
In-Progress -> Implemented
Implemented -> Closed (via G4)
Deferred -> Proposed (re-open)
Any state -> Superseded
```

## Trivial Changes

Trivial changes may bypass the CP process. A change is considered trivial if it is **one of**:
- A typo fix in documentation or comments
- A dependency patch-version bump (not minor or major)
- A comment-only change (no code logic changes)
- A formatter/import-order-only change produced by the configured tools (ruff)

**and** it changes no application behavior.

Trivial changes must:
- Carry the `trivial` label on the pull request
- Still pass all checks (lint, tests)
- Be reviewed by at least one human

If unsure whether a change is trivial, create a CP.

## Status Command

Use the CLI to check or change status:
```bash
python3 tools/cp/cp status <id> <state> --by <name>
```

## CLI Enforcement

`tools/cp/cp` enforces the lifecycle mechanically:

- **Transitions** are validated against the table above; invalid transitions are rejected.
- **Artifact preconditions**:
  - `-> Specified` requires `spec.md` to exist in the CP directory
  - `-> Spec-Approved` (G2) requires `cp lint` clean for the spec and spec front matter `approved_by`/`approved_on` set; the CLI sets spec `status: Approved`
  - `-> Planned` requires `plan.md` to exist
  - `-> In-Progress` (G3) requires a fully clean `cp lint`; the CLI sets plan `status: Approved`
  - `-> Implemented` requires every plan task `Status: done`
  - `-> Closed` (G4) requires a `## DoD Sign-Off` section in `log.md` containing `Status: PASSED`
- **`--by <name>` is required** for gate transitions (G1-G4) and for `Rejected`, `Deferred`, and `Superseded`. It records who authorized the transition; it is an honor-system record, not authentication. Agents must never pass `--by` for a gate on their own work.
- **Status history**: every transition appends a line `- <date> <from> -> <to> by <name> (Gn)` to `## Status History` in `log.md`.
- `status: Superseded` is allowed from any state; `--superseded-by CP-XXXX` sets `superseded_by` in the front matter.
