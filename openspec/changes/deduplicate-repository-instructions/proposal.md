# Proposal

## Why

Repository instructions repeat workflow, architecture, tooling and review rules in multiple files, allowing guidance to drift. Agents need one authoritative definition of each rule and links from every other entry point.

## What Changes

- Assign each instruction topic a canonical owner and replace duplicate prescriptions with links.
- Keep AGENTS.md as the entry point, the constitution as governance authority, the agent protocol as execution workflow, and the definition of done as completion/review criteria.
- Keep architecture rules in their standard and historical rationale in ADRs; make README and docs/README.md navigation/quick-start documents and stack.md a non-normative overview.
- Centralize command composition in justfile and make CI consume its check recipe while retaining coverage reporting and all existing checks.
- Replace repeated policy checklists in the PR template and standards with references to their owners.
- Correct the malformed YAML task rule in openspec/config.yaml, which OpenSpec currently ignores.
- Preserve established policy; explicitly label existing provisional targets and remove contradictory summaries rather than introducing new requirements.

## Capabilities

### New Capabilities

None. This is instruction and tooling deduplication, not a new application capability.

### Modified Capabilities

None. The ideas API behavior remains unchanged. This change sets skip_specs: true.

## Impact

AGENTS.md, README.md, docs/** instruction documents, openspec/config.yaml, justfile, .github/workflows/ci.yml, .github/pull_request_template.md and potentially pre-commit command wiring. No dependency additions or application changes.

## Non-goals

- Changing security/compliance controls, branch protections, coverage thresholds or merge policy.
- Editing generated skills, archived changes or baseline capability specs.
- Refactoring application code, adding a health endpoint, introducing logging infrastructure or changing HTTP error responses.
- Committing, pushing or archiving without following the established workflow and authorization.
