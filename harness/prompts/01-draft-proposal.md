# Draft Proposal Prompt

You are tasked with drafting a Change Proposal (CP) for a requested change.

## Context

The user has requested a change to the system. Your job is to create a proposal.md file that clearly articulates the "why" of this change.

## Instructions

1. Read the user's request carefully
2. Ask clarifying questions if anything is unclear
3. Draft the proposal using the template in `harness/templates/proposal.md`
4. Ensure all sections are filled thoughtfully
5. Focus on the "why" and "what", not the "how"

## Proposal Sections

### Summary
Write 1-2 sentences that capture the essence of the proposal.

### Motivation / Problem
Explain:
- What problem are we solving?
- Why is this change needed now?
- What pain points does it address?
- What happens if we don't do this?

### Goals
List 3-5 specific, measurable goals. Each goal should be:
- Specific (not vague)
- Measurable (can we verify it's done?)
- Achievable (realistic given constraints)

### Non-Goals
Explicitly state what is NOT in scope. This prevents scope creep.

### Proposed Solution
High-level description of the solution. Do NOT include:
- Implementation details
- Code snippets
- Database schemas
- API endpoints

Focus on:
- The approach at a conceptual level
- Architectural changes (if any)
- User experience changes

### Alternatives Considered
List 2-3 alternative approaches and explain why they were rejected. This shows due diligence.

### Impact
Consider all dimensions:
- Users: How does this affect end users?
- Data: Migration, schema changes, retention?
- Security: New attack vectors, authentication needs?
- Performance: Will this slow things down?
- Cost: Infrastructure, third-party services?

### Risks & Mitigations
List 3-5 potential risks and how to mitigate them. Be realistic.

### Open Questions
List questions that need answers before implementation. Don't guess - ask.

### Success Metrics
How will we know this succeeded? Metrics should be:
- Quantitative if possible
- Observable
- Time-bound

## Quality Checklist

Before submitting, verify:
- [ ] Summary is clear and concise
- [ ] Motivation is compelling
- [ ] Goals are specific and measurable
- [ ] Non-goals are clearly defined
- [ ] Solution is high-level (no implementation details)
- [ ] Alternatives show due diligence
- [ ] Impact analysis is comprehensive
- [ ] Risks have mitigations
- [ ] Open questions are actual questions
- [ ] Success metrics are observable

## Output

Create the proposal file at `proposals/XXXX-slug/proposal.md` where XXXX is the next available number and slug is a short URL-friendly version of the title.
