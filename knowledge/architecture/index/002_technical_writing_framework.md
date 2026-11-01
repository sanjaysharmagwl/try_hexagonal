# 0002. Use ASD-STE100 writing rules for knowledge management documents

- **Status:** Proposed
- **Date:** 2026-11-01
- **Deciders:** Engineering team
- **Related:** ADR 0001, `harness/standards/docs.md`

## Context

We write knowledge management documents such as ADRs, runbooks, design notes, and onboarding guides. Both humans and AI agents read and act on these documents. Today, writing style varies by author, terms drift between documents (for example, "service", "component", and "module" refer to the same thing), and sentences often contain several instructions. Agents and non-native English readers both misread this kind of text.

Forces in favour of a controlled standard:
- Short sentences with one instruction each are easier for humans and agents to parse reliably.
- A fixed, approved vocabulary reduces term drift across documents and authors.
- The standard is designed for readers who are not native English speakers, which matches our team.
- ASD-STE100 has a published rule set and an official, freely available copy, so we do not have to invent our own rules.

Facts that cut against this decision:
- The ASD-STE100 general dictionary (about 900 words) was built for aircraft maintenance. Many software terms, such as "repository", "deploy", "cache", and "pipeline", are not in it and must be added as project terms.
- Some rules, such as limits on "-ing" forms, clash with ordinary software vocabulary such as "logging" or "caching" and need project-specific handling.
- ADRs and design notes need to explain trade-offs and reasoning, and a strict vocabulary can make that prose stilted.
- Contributors need training, and the standard alone does not check documents. Enforcement needs a tool, and we have not yet selected one.

## Decision

We will write procedural knowledge management documents, such as runbooks and how-to guides, in ASD-STE100 Issue 9 style. We will use the standard's writing rules and its general dictionary, plus a project dictionary of approved technical terms that we maintain. We will write ADRs and design notes with the same writing rules, but we may relax the dictionary restriction for rationale and background sections. We will check documents against these rules with an automated checker in CI, and we will record the chosen checker in a follow-up ADR.

## Consequences

Easier:
- Terms are consistent across documents, which helps both human readers and agents retrieve and act on content.
- Short, single-instruction sentences are simpler to translate and review.
- New contributors have a clear, published rule set to follow.

Harder:
- First drafts take longer, and reviewers spend time on style as well as content.
- We must create and maintain a project dictionary, and every new technical term needs an approval step.
- Rationale sections may read more formally than authors want.
- We must pick, configure, and maintain a checker.

Follow-up work:
- Create the project dictionary, with a term-approval process and an owner.
- Write a short style guide that states which rules apply to which document types.
- Select and configure the CI checker, then record the choice in an ADR.
- Pilot the approach on three documents (one runbook, one ADR, one onboarding guide) and review it after six months.

## Alternatives considered

- **Plain-English style guide (for example, a major tech company's developer documentation style):** lighter and cheaper to adopt, but it gives weaker control over vocabulary, so agents and readers get less consistency.
- **Diátaxis structure with markdown linting:** organizes documents by purpose and catches formatting errors, but sets no rules on sentence structure or vocabulary.
- **Full ASD-STE100 for every document, including ADRs:** rejected because it is too restrictive for reasoning and trade-off text.
- **No standard, keep the current practice:** rejected because term drift and inconsistent structure already reduce clarity for both humans and agents.