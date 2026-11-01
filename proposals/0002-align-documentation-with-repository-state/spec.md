---
id: CP-0002
proposal: CP-0002
status: Approved
version: 1.0
approved_by: sanjaysharmagwl
approved_on: 2026-11-02
---

# CP-0002 Spec: Align documentation with repository state

## Overview

Specify the documentation edits that make `README.md`, `harness/` docs, and `knowledge/` ADRs consistent with each other and with the current code, CI (`.github/workflows/ci.yml`), and tooling (`tools/cp`, `harness/checks/`). Documentation only.

## Definitions

- **Canonical command list**: the `cp` command table in `proposals/README.md` ("Quick Reference"), which lists every `cp` subcommand
- **Broken reference**: a backticked repository path, ADR number, or test ID in a touched document that does not exist in the repository
- **Touched docs**: `README.md`, `harness/README.md`, `harness/stack.md`, `harness/standards/{docs,architecture,testing,git}.md`, and files under `knowledge/`

## Requirements

### REQ-001: README API documentation and links

`README.md` MUST contain an `## API Documentation` section that points to the interactive docs at `/docs`. `README.md` MUST NOT reference `knowledge/design/architecture.md`, and its project tree MUST describe `knowledge/` as architecture decision records only.

**Acceptance Criteria**:
- Given the updated `README.md`
- When it is searched for `## API Documentation` and `knowledge/design`
- Then the section exists, mentions `/docs`, and there is no `knowledge/design` reference

### REQ-002: README contributing and checks accuracy

The README `## Contributing` section MUST link to `proposals/README.md` as the canonical command list and MUST state that gate transitions (G1-G4) require `--by <name>`. The `## Development Checks` section MUST state that CI runs pytest with `--cov=app --cov=tools/cp`.

**Acceptance Criteria**:
- Given the updated `README.md`
- When the Contributing and Development Checks sections are read
- Then they reference `proposals/README.md`, `--by`, and `--cov=app --cov=tools/cp`

### REQ-003: Docs standard alignment

`harness/standards/docs.md` MUST NOT require a License section in the README structure. Its ADR status list MUST equal the template's (Proposed, Accepted, Deprecated, Superseded). It MUST reference the ADR template as `knowledge/architecture/template/adr.md`, and that file MUST exist (renamed from `ard.md`). It MUST state the numbering format: filenames `NNN_description.md`, headings `# NNNN. Title`.

**Acceptance Criteria**:
- Given the updated `docs.md` and `knowledge/architecture/template/`
- When `docs.md` is searched for `License`, `Rejected`, and `ard.md`, and the template directory is listed
- Then none of the three strings appears in the README-structure/ADR sections, `adr.md` exists, and `ard.md` does not

### REQ-004: Architecture and testing standards accuracy

`harness/standards/architecture.md` MUST show `main.py` at the repository root, outside `app/`, in its module tree. `harness/standards/testing.md` MUST use `--cov=app --cov=tools/cp` wherever it describes the CI coverage command, and every test ID it cites MUST exist.

**Acceptance Criteria**:
- Given the updated `architecture.md` and `testing.md`
- When the module tree and test IDs are compared with the repository
- Then `main.py` is outside `app/` and each cited test ID resolves (e.g. `tests/unit/test_domain.py::test_review_then_approve`)

### REQ-005: Git standard alignment

`harness/standards/git.md` MUST prescribe linear history via rebase-merge (no merge commits, no squash) and state that this preserves per-task commits. It MUST link to `.github/pull_request_template.md` instead of embedding a divergent PR template. It MUST NOT describe a commit-msg hook.

**Acceptance Criteria**:
- Given the updated `git.md`
- When it is searched for `merge commits`, `rebase`, `pull_request_template.md`, and `Commit-msg`
- Then it prescribes rebase-merge, links the PR template, contains no embedded PR description template, and has no Commit-msg section

### REQ-006: Stack and harness README accuracy

`harness/stack.md` MUST state resolved questions in past tense, MUST NOT state a specific local runtime version, and MUST NOT list CONTRIBUTING.md as an open question (the README Contributing section covers it). `harness/README.md` MUST link to `proposals/README.md` for the full `cp` command list.

**Acceptance Criteria**:
- Given the updated `stack.md` and `harness/README.md`
- When they are searched for `to be added`, `will be moved`, `to be configured`, `to be defined`, `3.13.5`, and `No CONTRIBUTING.md`
- Then none appear, and `harness/README.md` references `proposals/README.md`

### REQ-007: Knowledge base consistency

`knowledge/design/architecture.md` and `knowledge/architecture/README.md` MUST be removed. ADR 002 MUST be renamed to `knowledge/architecture/index/002_technical_writing_framework.md`, MUST have heading `# 0002. ...`, MUST keep status Proposed, and MUST contain no `[...]` placeholders. ADR 001 MUST NOT reference `docs/hexagonal-architecture-team-guide.md` or ADR 0003, MUST NOT attribute CRUD layering to ADR 0002, and MUST record that the import-linter follow-up is covered by `harness/checks/check_architecture.py`.

**Acceptance Criteria**:
- Given the updated `knowledge/` tree
- When it is listed and the ADRs are searched for `techincal`, `docs/hexagonal`, `ADR 0003`, `see ADR 0002`, and `[`-placeholders
- Then the empty files are gone, ADR 002 has the new name and `0002.` heading, and none of the strings appear

### REQ-008: No non-documentation change

This CP MUST NOT modify files under `app/`, `tests/`, `tools/`, `harness/checks/`, `.github/`, or `main.py`, `pyproject.toml`, `uv.lock`. All repository checks MUST pass.

**Acceptance Criteria**:
- Given the CP-0002 commits
- When `git diff --name-only main...HEAD` is run and the five checks from `AGENTS.md` are executed
- Then no listed path appears and every check passes

## Interfaces & Data Contracts

- ADR filename: `knowledge/architecture/index/NNN_description.md`; ADR heading: `# NNNN. Title`
- ADR status values: `Proposed | Accepted | Deprecated | Superseded by NNNN`
- Canonical `cp` command list: `proposals/README.md` "Quick Reference"

## Error Handling & Edge Cases

- Renamed files (ADR 002, ADR template): every inbound reference in the repository MUST be updated in the same task; verified by searching for the old names
- ADR 001 is Accepted: edits are limited to the `Related` line, the wrong ADR 0002 cross-reference, and the follow-up list; the Context, Decision, and Alternatives prose otherwise stays unchanged
- ADR 002 placeholders: `Deciders` becomes `Engineering team` (matching ADR 001); `Related` becomes `ADR 0001, harness/standards/docs.md`; the "[to be filled in]" fact is removed
- `knowledge/design/` becomes empty after the deletion and is removed with it

## Non-Functional Requirements

- Edits are minimal: only text needed to satisfy each REQ changes
- Markdown renders correctly (headings, code fences, tables intact)

## Security & Privacy

None. No secrets, inputs, or runtime behavior affected.

## Out of Scope

- LICENSE file
- Whether docs-only changes require a CP (constitution change)
- Code smells: port and adapter co-located in `repository.py`, missing HTTP tests/httpx, missing docstrings, unimplemented observability standards, empty `# uv` section in `.gitignore`
- `git.md` "Direct commits to `main` are forbidden" versus bootstrap history
- GitHub branch protection merge settings (configured in the GitHub UI)

## Amendments

None.
