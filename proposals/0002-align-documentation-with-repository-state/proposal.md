---
id: CP-0002
title: Align documentation with repository state
author: sanjaysharmagwl
status: Implemented
created: 2026-11-02
updated: 2026-11-02
supersedes:
superseded_by:
tags: [docs]
---

# CP-0002: Align documentation with repository state

## Summary

Bring `README.md`, `harness/` docs, and `knowledge/` ADRs in line with each other and with the actual code, CI, and tooling. Documentation only; no application behavior change.

## Motivation / Problem

After the README rewrite, a holistic review found documents that contradict the code, CI, or each other:

- `README.md` lacks the API Documentation section required by `harness/standards/docs.md`, links to an empty `knowledge/design/architecture.md`, and lists a different subset of `cp` commands than `harness/README.md` and `proposals/README.md`.
- `harness/standards/docs.md` requires a License section that the project does not use; its ADR status list disagrees with the ADR template; the template file is named `ard.md`.
- `harness/standards/architecture.md` places `main.py` inside `app/`; it lives at the repository root.
- `harness/standards/testing.md` shows `--cov=app` while CI uses `--cov=app --cov=tools/cp`, and cites a test ID that does not exist.
- `harness/standards/git.md` says "Linear History" but prescribes merge commits, duplicates (and diverges from) `.github/pull_request_template.md`, and describes a commit-msg hook that is not configured.
- `harness/stack.md` keeps completed items in future tense, misstates the runtime version, and lists CONTRIBUTING.md as an open question that the README now answers.
- `knowledge/architecture/index/002_techincal_writing_framework.md` has a filename typo, a duplicate "0001." heading, and unfilled placeholders. ADR 001 references a non-existent team guide and ADR 0003, misattributes CRUD layering to ADR 0002, and lists an import-linter follow-up already covered by `harness/checks/check_architecture.py`. File and heading numbering formats are inconsistent.
- `knowledge/design/architecture.md` and `knowledge/architecture/README.md` are empty.

Stale docs mislead both humans and agents, who treat `harness/` as authoritative.

## Goals

- Every statement in the touched docs matches the current code, CI, and tooling
- One canonical list of `cp` commands (`proposals/README.md`), linked from elsewhere
- Linear history via rebase-merge documented in `git.md`, preserving per-task commits
- ADRs consistently numbered and free of broken references
- No empty placeholder docs linked from the README

## Non-Goals

- Any change to `app/`, `main.py`, tests, CI, or tooling behavior
- Adding a LICENSE file
- Clarifying whether docs-only changes require a CP (constitution change; separate CP)
- Addressing code smells found during review (port and adapter co-located in `repository.py`, missing HTTP tests/httpx, missing docstrings, unimplemented observability standards, empty `# uv` section in `.gitignore`)

## Proposed Solution

Documentation edits across `README.md`, `harness/standards/{docs,architecture,testing,git}.md`, `harness/stack.md`, `harness/README.md`, and `knowledge/`:

- README: add API Documentation section, remove the design-notes link, point Contributing to `proposals/README.md`, note `--by` for gates and CI coverage flags
- `docs.md`: drop the License requirement, align ADR statuses with the template, rename the template to `adr.md`, and state one numbering format (`NNN_` filenames, `NNNN.` headings)
- `architecture.md`, `testing.md`: correct module tree, coverage command, and example test
- `git.md`: rebase-merge linear history, link the PR template instead of duplicating it, remove the commit-msg hook claim
- `stack.md`, `harness/README.md`: past tense for resolved items, correct runtime note, close the CONTRIBUTING question, link the canonical command list
- `knowledge/`: delete the two empty files, rename and renumber ADR 002 (status stays Proposed), fix ADR 001 references and follow-up

## Alternatives Considered

- Treat as a trivial change: rejected, the edits exceed the trivial definition in `harness/workflow/lifecycle.md`
- Amend CP-0001: rejected, CP-0001 is Implemented and its spec is approved
- Fill the empty knowledge docs instead of deleting them: rejected for now, no content owner; can return via a future CP
- Squash merges for linear history: rejected, would collapse the per-task commits required by `harness/workflow/agent-protocol.md`

## Impact

### Users
Contributors and agents get accurate guidance. Merge style changes from merge commits to rebase-merge.

### Data
None.

### Security
None.

### Performance
None.

### Cost
None.

## Risks & Mitigations

- Renaming ADR 002 and the ADR template breaks inbound links: grep for references and update them in the same task; `cp lint` checks relative links in CP docs
- Deleting empty files removes intended future locations: documented here; recreate via a future CP when content exists
- Branch protection merge setting must match rebase-merge: configured in the GitHub UI by a human (out of repo scope)

## Open Questions

None.

## Success Metrics

- All five repository checks pass (ruff format, ruff check, pytest, `cp lint`, `run_all.py`)
- No reference in touched docs points to a non-existent file, command, or test
- `git diff` shows no changes under `app/`, `main.py`, `tests/`, `tools/`, or `.github/`
