# Design

## Context

See proposal.md for motivation and scope. The working tree was clean before this change. Review found repeated read orders, task/commit rules, architecture descriptions, check lists, dependency/tool settings and review requirements. The constitution allows trivial exceptions but the protocol's absolute tasks-only wording omits them. OpenSpec also reports that rules.tasks[1] in config.yaml is a mapping because of an unquoted colon.

## Goals / Non-Goals

Give each rule one normative owner and retain discoverability through relative Markdown links. DRY applies to maintained definitions, not to historical evidence or examples of using a command. Do not replace helpful links with an indiscriminate shared abstraction.

See proposal.md for non-goals. Historical ADRs and generated skills are not live policy copies to rewrite.

## Decisions

### Ownership

| Topic | Canonical owner |
| --- | --- |
| Core user preferences | AGENTS.md Core section, preserved verbatim |
| Governance, trivial exceptions, scope, spec authority and task/commit policy | docs/constitution.md |
| Read order and execution sequence | docs/workflow/agent-protocol.md |
| Completion, review and exception criteria | docs/workflow/definition-of-done.md |
| Architectural constraints | docs/standards/architecture.md |
| Historical architectural rationale | docs/architecture.md |
| Testing policy and provisional coverage targets | docs/standards/testing.md |
| Git mechanics and merge policy | docs/standards/git.md |
| Docstring format and documentation requirements | docs/standards/docs.md |
| Coding conventions | docs/standards/coding.md |
| Logging and metrics | docs/standards/observability.md |
| Security requirements | docs/standards/security.md, unchanged |
| Commands and gate composition | justfile |
| Dependency/tool settings | pyproject.toml files |
| Local check implementation contract/index | docs/checks/README.md |

AGENTS.md, docs/README.md and stack.md link to owners instead of restating their contents. Keep root README's runnable quick start and API example. The PR template captures evidence and attests to DoD rather than copying it. Prefer links over duplicated summaries because summaries drift independently.

### Workflow and conflicts

The protocol links to the constitution's change/trivial distinction and task policy rather than reproducing them. It retains only execution-specific steps and unique honesty/communication guidance not already owned by Core. DoD links to testing and documentation standards instead of repeating their rules. Keep human approval and completion criteria intact.

In Git guidance, rename the misleading Linear History heading to Merge Policy while preserving the existing merge-commit instruction. Do not choose a new merge strategy. Keep existing coverage targets explicitly provisional in their sole owner; do not add enforcement thresholds or remove the non-decrease review requirement.

Remove stale Command-based observability examples. For API response shapes, refer to the capability spec rather than prescribing a competing error envelope. Security rules and controls remain untouched; other documents link to them rather than duplicating sensitive-data policy.

### Executable definitions

Have check use the existing coverage test recipe instead of separately maintaining plain-test and coverage gates; retain test for focused runs. CI calls just check after its existing locked workspace installation. This preserves every check and coverage reporting without a second CI recipe list.

Pre-commit's filename-sensitive ruff hooks retain their existing semantics. Delegate only the filename-independent OpenSpec hook to just spec, preserving its openspec/ filter and pass_filenames: false. This removes the second pinned OpenSpec invocation, not a security control.

OpenSpec context points to authoritative docs rather than copying architecture details. Keep artifact-specific generation guidance there; quote the malformed task-rule scalar without altering its meaning.

### Verification

Use just's dry-run output to confirm coverage and every existing check remain reachable through check, and inspect CI/pre-commit wiring. Check relative Markdown links in changed live instruction files with a temporary local validation command. Review the diff against the ownership table to ensure each removed requirement remains available at its owner. Run just check, strict OpenSpec validation and git diff --check. No application test changes are needed because API behavior is unchanged.

## Risks / Trade-offs

- Links require readers to follow references: retain concise navigation at agent and human entry points.
- Removing a duplicate could remove a unique rule: inventory unique requirements before rewriting each file; retain them at the appropriate owner.
- Coverage runs are slightly slower than plain pytest: they already run in CI and avoid duplicating the verification definition.
- Existing provisional policies are unresolved: preserve their status instead of promoting guesses into requirements.
- Instruction policy cannot prove repository protection is configured: describe expected policy without claiming it is enforced remotely.

## Migration Plan

Update governance/navigation first, then standards, then command consumers. Run verification before completion. Rollback is a normal reviewable Git change, never a history rewrite. Baseline specs and archives remain untouched.
