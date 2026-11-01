---
id: CP-0002
spec: CP-0002
status: Approved
plan: CP-0002
---

# CP-0002 Plan: Align documentation with repository state

## Approach & Architecture Notes

Documentation-only edits, one task per document group, committed per task on branch `cp-0002-align-documentation` and merged by rebase-merge. File renames use `git mv` so history follows the file. No code, test, tooling, CI, or dependency file changes (REQ-008). Each task is verified by the `rg`/`ls` checks under "Verification Steps" plus the five repository checks.

## Files in Scope

- `README.md` (modify)
- `harness/standards/docs.md` (modify)
- `harness/standards/architecture.md` (modify)
- `harness/standards/testing.md` (modify)
- `harness/standards/git.md` (modify)
- `harness/stack.md` (modify)
- `harness/README.md` (modify)
- `knowledge/architecture/template/ard.md` (rename to `adr.md`)
- `knowledge/architecture/index/002_techincal_writing_framework.md` (rename to `002_technical_writing_framework.md` and modify)
- `knowledge/architecture/index/001_adopting_hexagonal_architecture.md` (modify)
- `knowledge/design/architecture.md` (delete)
- `knowledge/architecture/README.md` (delete)
- `proposals/0002-align-documentation-with-repository-state/*` (modify: plan status, log)
- `proposals/README.md` (modify: regenerated index)

## Task List

### T-001: README API docs, links, contributing

- **Status**: todo
- **Requirements**: REQ-001, REQ-002
- **Depends on**: none
- **Files**: README.md
- **Tests**: verify-readme (see Verification Steps)
- **Done when**: README has `## API Documentation` mentioning `/docs`; no `knowledge/design` reference; tree describes `knowledge/` as ADRs; Contributing links `proposals/README.md` and states `--by` for G1-G4; Development Checks names `--cov=app --cov=tools/cp`
- **Size**: S (<= 1 PR)
- **Description**: Finalize the uncommitted README rewrite against REQ-001 and REQ-002

### T-002: Docs standard and ADR template

- **Status**: todo
- **Requirements**: REQ-003
- **Depends on**: none
- **Files**: harness/standards/docs.md, knowledge/architecture/template/ard.md -> adr.md
- **Tests**: verify-docs-standard (see Verification Steps)
- **Done when**: no License in README structure; ADR statuses Proposed/Accepted/Deprecated/Superseded; template referenced and present as `adr.md`; numbering format `NNN_description.md` / `# NNNN. Title` stated
- **Size**: S (<= 1 PR)
- **Description**: Align docs.md with the ADR template and drop the License requirement

### T-003: Architecture and testing standards

- **Status**: todo
- **Requirements**: REQ-004
- **Depends on**: none
- **Files**: harness/standards/architecture.md, harness/standards/testing.md
- **Tests**: verify-arch-testing (see Verification Steps)
- **Done when**: `main.py` outside `app/` in the module tree; CI coverage command is `--cov=app --cov=tools/cp`; cited test IDs exist
- **Size**: S (<= 1 PR)
- **Description**: Correct the module tree, coverage commands, and example test IDs

### T-004: Git standard

- **Status**: todo
- **Requirements**: REQ-005
- **Depends on**: none
- **Files**: harness/standards/git.md
- **Tests**: verify-git-standard (see Verification Steps)
- **Done when**: History section prescribes rebase-merge (no merge commits, no squash) preserving per-task commits; PR template linked, not embedded; no Commit-msg section
- **Size**: S (<= 1 PR)
- **Description**: Resolve the linear-history contradiction and remove duplicated/unimplemented content

### T-005: Stack and harness README

- **Status**: todo
- **Requirements**: REQ-006
- **Depends on**: none
- **Files**: harness/stack.md, harness/README.md
- **Tests**: verify-stack-harness (see Verification Steps)
- **Done when**: resolved questions in past tense; no runtime version; CONTRIBUTING question removed; harness README links `proposals/README.md`
- **Size**: S (<= 1 PR)
- **Description**: Remove stale statements and point to the canonical command list

### T-006: Knowledge base

- **Status**: todo
- **Requirements**: REQ-007
- **Depends on**: T-002
- **Files**: knowledge/design/architecture.md, knowledge/architecture/README.md, knowledge/architecture/index/002_techincal_writing_framework.md -> 002_technical_writing_framework.md, knowledge/architecture/index/001_adopting_hexagonal_architecture.md
- **Tests**: verify-knowledge (see Verification Steps)
- **Done when**: empty files deleted; ADR 002 renamed, heading `# 0002.`, status Proposed, placeholders replaced per spec; ADR 001 Related line, ADR 0002 cross-reference, and follow-up fixed; ADR 001 Context/Decision/Alternatives prose otherwise unchanged
- **Size**: S (<= 1 PR)
- **Description**: Remove empty docs and make ADRs consistent with the numbering format from T-002

### T-007: Final verification

- **Status**: todo
- **Requirements**: REQ-008
- **Depends on**: T-001, T-002, T-003, T-004, T-005, T-006
- **Files**: proposals/0002-align-documentation-with-repository-state/log.md
- **Tests**: verify-scope plus the five repository checks
- **Done when**: no out-of-scope paths in the branch diff; all checks pass; results pasted in log.md
- **Size**: S (<= 1 PR)
- **Description**: Confirm scope and run all checks

## Traceability Matrix

| REQ | Task(s) | Test(s) |
|-----|---------|---------|
| REQ-001 | T-001 | verify-readme |
| REQ-002 | T-001 | verify-readme |
| REQ-003 | T-002 | verify-docs-standard |
| REQ-004 | T-003 | verify-arch-testing |
| REQ-005 | T-004 | verify-git-standard |
| REQ-006 | T-005 | verify-stack-harness |
| REQ-007 | T-006 | verify-knowledge |
| REQ-008 | T-007 | verify-scope, repository checks |

## Rollout / Migration / Rollback

Merge the branch by rebase-merge. No migration. Rollback: revert the CP-0002 commits; renames revert cleanly because they use `git mv`.

## Verification Steps

```bash
# verify-readme (REQ-001, REQ-002): first two must match, third must not
rg -n '^## API Documentation' README.md && rg -n '/docs' README.md
rg -n 'proposals/README.md|--by|--cov=app --cov=tools/cp' README.md
! rg -n 'knowledge/design' README.md

# verify-docs-standard (REQ-003)
ls knowledge/architecture/template/adr.md && ! ls knowledge/architecture/template/ard.md
! rg -n 'ard\.md|License' harness/standards/docs.md
rg -n 'Deprecated' harness/standards/docs.md

# verify-arch-testing (REQ-004)
# tree root must be the repository, not app/ (main.py is a sibling of app/)
! rg -n '^app/$' harness/standards/architecture.md && rg -n '^├── app/' harness/standards/architecture.md
rg -n 'cov=tools/cp' harness/standards/testing.md
uv run pytest --collect-only -q tests/unit/test_domain.py::test_review_then_approve

# verify-git-standard (REQ-005)
rg -n -i 'rebase' harness/standards/git.md && rg -n 'pull_request_template.md' harness/standards/git.md
! rg -n -i 'commit-msg|use merge commits' harness/standards/git.md

# verify-stack-harness (REQ-006)
! rg -n 'to be added|will be moved|to be configured|to be defined|3\.13\.5|No CONTRIBUTING' harness/stack.md
rg -n 'proposals/README.md' harness/README.md

# verify-knowledge (REQ-007)
! ls knowledge/design/architecture.md knowledge/architecture/README.md
ls knowledge/architecture/index/002_technical_writing_framework.md
! rg -n 'techincal|docs/hexagonal|ADR 0003|see ADR 0002|\[names|\[ADR index|\[to be filled' knowledge/ harness/ README.md
rg -n '^# 0002\.' knowledge/architecture/index/002_technical_writing_framework.md

# verify-scope (REQ-008): must print nothing
git diff --name-only main...HEAD | rg '^(app/|tests/|tools/|harness/checks/|\.github/|main\.py|pyproject\.toml|uv\.lock)'

# repository checks
uv run ruff format --check .
uv run ruff check .
uv run pytest
python3 tools/cp/cp lint
python3 harness/checks/run_all.py
```
