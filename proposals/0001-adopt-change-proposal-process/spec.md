---
id: CP-0001
proposal: CP-0001
status: Approved
version: 1.0
approved_by: sanjaysharmagwl (bootstrap via task brief — pending confirmation)
approved_on: 2026-11-02
---

# CP-0001 Spec: Adopt Change Proposal Process

## Overview

Specify the CP workflow framework: harness layout, parseable templates, the `tools/cp` CLI lifecycle enforcement, executable harness checks, CI pipeline, and the PR CP-reference rule — with zero application behavior change.

## Definitions

- **CP**: Change Proposal; a directory under `proposals/NNNN-slug/` containing proposal.md, spec.md, plan.md, log.md
- **Gate (G1-G4)**: A human-approved lifecycle transition enforced by the CLI
- **Harness**: `harness/` directory of standards, workflow docs, templates, prompts, and checks
- **Trivial change**: One of {doc/comment typo, dependency patch bump, comment-only change, formatter-only change} that changes no behavior

## Requirements

### REQ-001: Harness layout

The repository MUST contain `harness/` with `constitution.md`, `stack.md`, `workflow/` (lifecycle, roles, agent-protocol, definition-of-done), `standards/` (architecture, coding, docs, git, observability, security, testing), `templates/`, `prompts/`, and `checks/`.

**Acceptance Criteria**:
- Given the repository root
- When the harness directory is listed
- Then all of the above files and directories exist

### REQ-002: Parseable templates

`harness/templates/{proposal,spec,plan}.md` MUST start with YAML-like front matter (`key: value` lines between `---` fences) and contain the required `## ` sections; `proposals/0000-template/` MUST contain byte-identical copies plus `log.md`.

**Acceptance Criteria**:
- Given the template files
- When parsed by `tools/cp`
- Then front matter keys and required sections are present and the copies are byte-identical

### REQ-003: `cp new`

`cp new "<title>"` MUST create `proposals/NNNN-slug/` with the next available number (ignoring 0000), fill front matter (id, title, author, dates, status Draft), append the first status-history line, and regenerate the index.

**Acceptance Criteria**:
- Given a repository with `proposals/0000-template/`
- When `cp new "X"` runs
- Then the numbered CP directory exists with status Draft and a history line

### REQ-004: `cp status` transitions and gates

`cp status <id> <state>` MUST validate against the transition table, enforce artifact preconditions (spec.md before Specified, plan.md before Planned), require `--by` for gate transitions (G1-G4) and Rejected/Deferred/Superseded, update front matter, and append status-history lines.

**Acceptance Criteria**:
- Given a CP in a given state
- When an invalid transition or a gate without `--by` is attempted
- Then the CLI rejects it with a clear error and exit code 1

### REQ-005: `cp spec` and `cp plan` gating

`cp spec <id>` MUST scaffold spec.md only when status is Accepted; `cp plan <id>` only when status is Spec-Approved; both refuse to overwrite existing files.

**Acceptance Criteria**:
- Given a CP not in the required status
- When `cp spec`/`cp plan` is run
- Then the CLI refuses with an error

### REQ-006: `cp lint` rules

`cp lint [id]` MUST check front matter keys, known statuses, required sections, REQ uniqueness/MUST-SHOULD-MAY/Given-When-Then, task field completeness and reference validity, traceability matrix coverage, status-document consistency, status-history validity, and relative markdown links; it MUST exit 1 on any problem.

**Acceptance Criteria**:
- Given a CP violating any rule
- When `cp lint` runs
- Then each problem is printed as `path: message` and exit code is 1

### REQ-007: `cp index`

`cp index` MUST regenerate only the table between `<!-- cp-index:start -->` and `<!-- cp-index:end -->` in `proposals/README.md` (columns ID, Title, Status, Author), preserving surrounding content.

**Acceptance Criteria**:
- Given a README with text around the markers
- When `cp index` runs
- Then the table is refreshed and surrounding text is unchanged

### REQ-008: `cp next`

`cp next <id>` MUST print the first task with `Status: todo` whose dependencies are all `done`, or "All tasks done"; it SHOULD warn on stderr when the CP is not In-Progress.

**Acceptance Criteria**:
- Given a plan with interdependent tasks
- When `cp next` runs
- Then the first unblocked todo task is printed with its full block

### REQ-009: Harness checks

`harness/checks/` MUST provide executable, importable, stdlib-only checks (architecture boundaries, banned patterns, secrets, templates sync, PR reference) plus `run_all.py` which runs all but the CI-only check.

**Acceptance Criteria**:
- Given the repository
- When `python3 harness/checks/run_all.py` runs
- Then each check reports PASS/FAIL and the exit code reflects failures

### REQ-010: CI pipeline

GitHub Actions MUST run ruff format check, ruff lint, pytest with coverage, `cp lint`, and `run_all.py` on push to main and pull requests; a separate job MUST run the PR CP-reference check on pull requests.

**Acceptance Criteria**:
- Given `.github/workflows/ci.yml`
- When a push or PR occurs
- Then the `checks` job runs all commands and `cp-reference` runs on PRs

### REQ-011: PR CP-reference rule

For PRs touching `app/` or `main.py` without the `trivial` label, `check_pr_reference.py` MUST require the PR title/body to reference a CP-NNNN whose status is `In-Progress`.

**Acceptance Criteria**:
- Given a PR body/title/labels/changed-files via environment
- When the check runs
- Then it fails unless a referenced CP is In-Progress or the `trivial` label applies

### REQ-012: No application behavior change

This CP MUST NOT change application behavior; the pre-existing domain tests MUST pass unchanged.

**Acceptance Criteria**:
- Given `tests/unit/test_domain.py` (moved verbatim from the repo root)
- When `uv run pytest` runs
- Then all tests pass with no behavioral modifications to `app/` or `main.py` (style-only diff)

## Interfaces & Data Contracts

- CP front matter: simple `key: value` lines between `---` fences; lists as `[a, b]`
- Status history lines: `- YYYY-MM-DD From -> To by <name> [(Gn)]`
- Task fields: `- **Status|Requirements|Depends on|Files|Tests|Done when|Size|Description**: ...`
- Traceability matrix: `| REQ | Task(s) | Test(s) |`
- CLI signature: `main(argv, root) -> int`; exit 0 success, 1 error

## Error Handling & Edge Cases

- Unknown command/id/state: stderr message + exit 1
- `cp spec`/`plan` on existing file or wrong status: refused
- `cp next` with all tasks done: prints "All tasks done"
- Checks on non-git roots (tests): secret scan falls back to walking files

## Non-Functional Requirements

- `tools/cp` and all checks are Python stdlib-only
- Tests run against `tmp_path` fixtures, never the real repo state
- Root defaults to the repo containing the script, not the cwd

## Security & Privacy

- `--by` is an honor-system record of the human approver, not authentication
- Secret scan covers all tracked files; `uv.lock` skipped
- CI must never interpolate the PR body into shell code (passed via `env:`)

## Out of Scope

- Type checking (mypy)
- Branch protection / required-reviewers GitHub settings
- Any application feature or behavior change

## Amendments

None.
