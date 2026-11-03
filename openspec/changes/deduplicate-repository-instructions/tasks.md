# Tasks

## 1. Canonical instruction ownership

- [ ] 1.1 Consolidate AGENTS.md, docs/README.md, docs/constitution.md, agent-protocol.md and definition-of-done.md around the ownership table in design.md; preserve Core verbatim, retain all unique policies, link to owners, and verify the protocol accommodates the constitution's trivial-change exception and defines read order once.
- [ ] 1.2 Remove repeated architecture, dependency, tooling and command definitions from README.md and docs/stack.md; retain the runnable quick start/API example and verify relative links resolve to their canonical owners.

## 2. Concern-specific standards

- [ ] 2.1 Deduplicate coding, documentation, testing and Git standards internally and across documents; preserve unique requirements and existing merge policy, centralize provisional coverage targets in testing.md, and verify removed prescriptions remain available through owner links.
- [ ] 2.2 Deduplicate architecture and observability guidance without changing security.md or historical ADRs; replace stale Command examples and conflicting HTTP response guidance with references to current code/specs, and verify no new health/logging/API behavior is required.
- [ ] 2.3 Replace the PR template's copied checklist with evidence fields and a DoD attestation; keep the change/trivial distinction via a constitution link and verify every review requirement remains in the DoD owner.

## 3. Command consumers

- [ ] 3.1 Make just check run the existing coverage test recipe and have CI call just check; verify just --dry-run check retains lint, types, arch, tests with coverage, spec validation and local checks, without introducing a coverage threshold.
- [ ] 3.2 Delegate pre-commit OpenSpec validation to just spec while preserving filename filters and ruff hook semantics; reduce OpenSpec context to owner references, quote the malformed YAML task rule, and verify OpenSpec no longer warns about ignored task rules.

## 4. Integration verification

- [ ] 4.1 Validate relative Markdown links in changed live instruction files, review every removed rule against its canonical owner, run git diff --check and just check, and record actual verification results in this change's tasks.md.

## Workflow follow-up

- Review and archive the change after the repository's review requirements are satisfied.
