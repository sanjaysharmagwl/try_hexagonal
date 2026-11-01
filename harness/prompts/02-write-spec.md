# Write Specification Prompt

You are tasked with writing a specification (spec.md) for an accepted Change Proposal.

## Context

The proposal has been accepted. Now you need to write the detailed specification that defines exactly what will be built.

## Instructions

1. Read the accepted proposal.md carefully
2. Write spec.md using the template in `harness/templates/spec.md`
3. Ensure every requirement is testable
4. Use MUST/SHOULD/MAY language per RFC 2119
5. Define all interfaces and data contracts
6. Specify error handling and edge cases

## Specification Sections

### Overview
Provide a detailed overview of what is being specified. This should be more detailed than the proposal but still high-level.

### Definitions
Define all key terms, concepts, and entities. This creates a shared vocabulary.

### Requirements
This is the core of the spec. Each requirement must:
- Have a unique ID (REQ-001, REQ-002, etc.)
- Use MUST/SHOULD/MAY language
- Have acceptance criteria in Given/When/Then format
- Be testable

Example:
```
## REQ-001: Idea Title Validation

**MUST**: The system must reject ideas with empty titles.

**Acceptance Criteria**:
- Given: A user submits an idea with an empty title
- When: The submission is processed
- Then: The system returns a 422 error with message "Title cannot be empty"
```

### Interfaces & Data Contracts
Define all external interfaces:
- API endpoints (request/response schemas)
- Database schemas (tables, columns, constraints)
- Events (event types, payloads)
- Any other external contracts

Be precise. Use JSON schemas or similar for clarity.

### Error Handling & Edge Cases
Define:
- All error conditions
- HTTP status codes for each error
- Error response formats
- How to recover from errors
- Edge cases and how to handle them

### Non-Functional Requirements
Define quality attributes:
- Performance (response times, throughput)
- Scalability (how much load can it handle?)
- Reliability (uptime, durability)
- Maintainability (coverage, documentation)

### Security & Privacy
Define:
- Authentication requirements
- Authorization requirements
- Data privacy (encryption, logging)
- Input validation requirements

### Out of Scope
Explicitly list what is NOT included. This prevents scope creep.

## Quality Checklist

Before submitting, verify:
- [ ] Every requirement has a unique ID
- [ ] Every requirement uses MUST/SHOULD/MAY
- [ ] Every requirement has acceptance criteria
- [ ] All acceptance criteria are in Given/When/Then format
- [ ] All requirements are testable
- [ ] Interfaces are fully specified
- [ ] Error conditions are defined
- [ ] Edge cases are addressed
- [ ] Non-functional requirements are specified
- [ ] Security implications are addressed
- [ ] Out of scope is clearly defined

## Output

Create the spec file at `proposals/XXXX-slug/spec.md`.

Run `cp lint <id>` to validate before submitting for review.
