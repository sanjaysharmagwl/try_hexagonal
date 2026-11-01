# Roles

This document defines the roles in the CP workflow and their responsibilities.

## Roles

### Author
**Who**: Any human or agent proposing a change

**Responsibilities**:
- Draft the proposal (proposal.md)
- Write the specification (spec.md) after proposal is Accepted
- Write the implementation plan (plan.md) after spec is Spec-Approved
- Implement the plan (as Implementer) or delegate to an agent
- Maintain log.md with implementation notes and decisions
- Respond to reviewer feedback
- Withdraw proposal if needed

**Can transition states**:
- Draft -> Proposed
- Accepted -> Specified
- Spec-Approved -> Planned
- Any state -> Withdrawn

### Reviewer
**Who**: Human reviewer with domain knowledge

**Responsibilities**:
- Review proposals for completeness and quality
- Verify gate conditions (G1, G2, G4)
- Provide constructive feedback
- Approve or reject proposals
- Review implementation for adherence to spec
- Sign off on Definition of Done

**Can transition states**:
- Proposed -> Accepted (via G1)
- Proposed -> Rejected
- Proposed -> Deferred
- Specified -> Spec-Approved (via G2, with Approver)
- Implemented -> Closed (via G4)
- Any state -> Superseded

### Approver
**Who**: Human with authority to approve specs

**Responsibilities**:
- Review specifications for technical soundness
- Verify that all requirements are testable
- Sign off on spec approval (G2)
- Ensure architectural alignment

**Can transition states**:
- Specified -> Spec-Approved (via G2, with Reviewer)

### Implementer
**Who**: Human or agent writing code

**Responsibilities**:
- Read and understand the plan
- Implement tasks one at a time
- Commit after each task with proper references
- Run harness checks before declaring task done
- Update log.md with implementation notes
- Raise spec issues immediately via log.md
- Stay within "Files in scope" unless documented otherwise

**Can transition states**:
- In-Progress -> Implemented

## Role Assignment

- Author is always the person or agent creating the CP
- Reviewer is assigned when proposal is Proposed
- Approver is assigned when spec is Specified
- Implementer may be the Author or a different agent/human

## Agents in Roles

Agents may fulfill any role EXCEPT:
- Agents cannot approve their own work (no self-approval)
- Agents cannot approve a CP they authored
- Agents cannot sign off on G2 or G4 gates

For critical approvals (G2, G4), a human must always be involved.
