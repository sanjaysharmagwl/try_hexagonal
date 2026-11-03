# Docs

This directory contains the standards and workflows that govern development for this repository, alongside the OpenSpec spec-driven workflow in `openspec/`.

## Overview

The docs define:
- **Constitution**: Non-negotiable principles
- **Standards**: Coding, architecture, testing, security, git, docs, observability
- **Workflow**: Agent protocol, definition of done
- **Checks**: Executable enforcement of standards
- **Architecture**: ADRs in `architecture.md`

## Usage

For humans:
1. Read `constitution.md` to understand the principles
2. Review relevant `standards/` files before making changes
3. Non-trivial changes go through an OpenSpec change under `openspec/changes/`

For agents:
1. Always read `AGENTS.md` (root) first
2. Then read this `README.md`
3. Then read `constitution.md`
4. Then read relevant `standards/` files
5. Follow `workflow/agent-protocol.md` for all tasks

## Quick Start

To propose a new change, use the `openspec-propose` skill (`.agents/skills/`) — it writes `proposal.md`, `design.md`, spec deltas, and `tasks.md` under `openspec/changes/<name>/`.

To inspect OpenSpec state:

```bash
openspec list                 # active changes
openspec list --specs         # specs
openspec show <change>        # a change's artifacts
openspec validate --all --strict --no-interactive
```

To archive a completed change (merges its delta specs into `openspec/specs/`):

```bash
openspec archive <change>
```

The justfile runs the CLI via pinned `npx -y @fission-ai/openspec@1.15.0`; a global install is optional.

## Checks

Executable standards enforcement lives in `docs/checks/`:

- `check_banned_patterns.py` — wildcard imports, bare except, print/breakpoint
- `check_secrets.py` — committed-secret scan

Architecture boundaries are enforced separately by import-linter contracts in the root `pyproject.toml` (`just arch`).

Run all local checks:
```bash
just harness
# or: uv run python docs/checks/run_all.py
```

## File Structure

```
docs/
├── README.md             # This file
├── constitution.md       # Non-negotiable principles
├── architecture.md       # Architecture decision records (ADRs)
├── stack.md              # Technology stack documentation
├── workflow/
│   ├── agent-protocol.md # Rules for coding agents
│   └── definition-of-done.md
├── standards/
│   ├── coding.md         # Style, naming, structure
│   ├── architecture.md   # Layering, boundaries
│   ├── testing.md        # Test pyramid, coverage
│   ├── security.md       # Secrets, validation, auth
│   ├── git.md            # Branching, commits, PRs
│   ├── docs.md           # Documentation standards
│   └── observability.md  # Logging, metrics
└── checks/
    ├── README.md         # Index of available checks
    └── [executable scripts]
```
