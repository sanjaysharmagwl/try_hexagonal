# Harness

This directory contains the standards, workflows, and templates that govern the Change Proposal (CP) process for this repository.

## Overview

The harness defines:
- **Constitution**: Non-negotiable principles
- **Standards**: Coding, architecture, testing, security, git, docs, observability
- **Workflow**: CP lifecycle, roles, agent protocol, definition of done
- **Templates**: Proposal, spec, and plan templates
- **Prompts**: Reusable agent prompts for each phase
- **Checks**: Executable enforcement of standards

## Usage

For humans:
1. Read `constitution.md` to understand the principles
2. Review relevant `standards/` files before making changes
3. Follow the workflow in `workflow/lifecycle.md` for all non-trivial changes

For agents:
1. Always read `AGENTS.md` (root) first
2. Then read this `README.md`
3. Then read `constitution.md`
4. Then read relevant `standards/` files
5. Follow `workflow/agent-protocol.md` for all tasks

## Quick Start

To create a new Change Proposal:
```bash
tools/cp/cp new "Your proposal title"
```

To lint a proposal:
```bash
tools/cp/cp lint <id>
```

To see the next task in a plan:
```bash
tools/cp/cp next <id>
```

## File Structure

```
harness/
├── README.md              # This file
├── constitution.md        # Non-negotiable principles
├── stack.md              # Technology stack documentation
├── workflow/
│   ├── lifecycle.md      # CP states and transitions
│   ├── roles.md          # Author, Reviewer, Approver, Implementer
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
├── templates/
│   ├── proposal.md       # Proposal template
│   ├── spec.md           # Specification template
│   └── plan.md           # Implementation plan template
├── prompts/
│   ├── 01-draft-proposal.md
│   ├── 02-write-spec.md
│   ├── 03-write-plan.md
│   ├── 04-implement-task.md
│   └── 05-review-implementation.md
└── checks/
    ├── README.md         # Index of available checks
    └── [executable scripts]
```
