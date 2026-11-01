# Git Standards

This document defines git workflow and conventions for this repository.

## Branching Strategy

### Main Branch
- `main` is the protected default branch
- All PRs merge into `main`
- Direct commits to `main` are forbidden

### Feature Branches
- Create a branch for each CP: `cp-0001-description`
- Branch from `main`
- Merge back via PR
- Delete branch after merge

### Branch Naming
- Format: `cp-XXXX-short-description`
- Example: `cp-0001-add-user-authentication`
- Use lowercase, hyphens only

## Commit Messages

### Format
```
<type>: <subject> (CP-XXXX, T-YYY, REQ-ZZZ)

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring (no behavior change)
- `test`: Adding tests
- `docs`: Documentation changes
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Subject
- Imperative mood ("add" not "added")
- 50 characters or less
- No period at end
- Reference CP ID, Task ID, and REQ IDs

### Body
- Explain "why", not "what"
- Wrap at 72 characters
- Use present tense

### Footer
- Breaking changes: "BREAKING CHANGE: ..."
- References to issues: "Closes #123"

### Example
```
feat: add idea approval workflow (CP-0001, T-003, REQ-002)

Implement the approval workflow as specified in REQ-002.
Adds status transitions and validation.

BREAKING CHANGE: Idea.status now includes "approved" state.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>
```

## Pull Requests

### PR Title
- Follow commit message format
- Include CP ID
- Example: `feat: add idea approval workflow (CP-0001)`

### PR Description Template
Use `.github/pull_request_template.md`; GitHub applies it automatically and it is the single source of truth for PR descriptions.

### PR Requirements
- Must reference a CP in `In-Progress` state
- Must pass all CI checks
- Must have at least one reviewer approval
- Must resolve all review comments

### PR Labels
- `trivial`: For trivial changes (bypasses CP requirement)
- `bugfix`: For bug fixes
- `feature`: For new features
- `breaking`: For breaking changes

## Code Review

### Reviewer Responsibilities
- Check code adheres to standards
- Verify implementation matches spec
- Ensure tests are adequate
- Check documentation is updated
- Approve or request changes

### Author Responsibilities
- Address all review comments
- Update code/tests/docs as needed
- Respond to reviewer feedback
- Keep PR updated

### Review Turnaround
- Aim for review within 24 hours <!-- inferred: confirm -->
- If busy, leave a comment with ETA
- Use GitHub's "Request changes" appropriately

## History

### Linear History
- Merge PRs with rebase-merge (GitHub "Rebase and merge"); no merge commits and no squash merges
- Rebase-merge keeps every per-task commit (CP-XXXX, T-YYY, REQ-ZZZ) on `main`, preserving traceability
- Rebase your branch onto `main` before merging; force-push only your own feature branch (`--force-with-lease`), never `main`

### Reverting
- If a commit needs to be reverted, create a revert commit
- Don't delete history
- Document why in commit message

## CI Integration

### Required Checks
- All tests pass
- Linting passes
- Formatting passes
- Coverage reported (must not decrease)

### Blocking
PRs will be blocked if:
- CI checks fail
- No CP reference (unless `trivial` label)
- No reviewer approval
- Merge conflicts not resolved

## Git Hooks

### Pre-commit
A minimal `.pre-commit-config.yaml` (local hooks only) runs ruff format, ruff check, and `cp lint` on proposal changes. Install it with:
```bash
uvx pre-commit install
```

## Commands

### Useful Aliases
```bash
# View commit history
git log --oneline --graph

# View changed files
git diff --stat

# Interactive rebase (careful!)
git rebase -i HEAD~3
```

## Troubleshooting

### Merge Conflicts
1. Pull latest from main
2. Resolve conflicts locally
3. Test resolution
4. Commit and push

### Force Push
Never force push to `main` or shared branches without team consensus.

### Large Files
Git is not for large files. Use:
- Git LFS for large binary files
- External storage for data
- `.gitignore` to exclude
