# Git Standards

This document defines git workflow and conventions for this repository.

## Branching Strategy

### Main Branch
- `main` is the protected default branch
- All PRs merge into `main`
- Direct commits to `main` are forbidden

### Feature Branches
- Create a branch for each OpenSpec change
- Branch from `main`
- Merge back via PR
- Delete branch after merge

### Branch Naming
- Format: `<change-name>` — kebab-case matching `openspec/changes/<change-name>`
- Example: `add-user-authentication`
- Use lowercase, hyphens only

## Commit Messages

### Format
```
<type>: <subject> (<change-name>)

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
- Reference the OpenSpec change name

### Body
- Explain "why", not "what"
- Wrap at 72 characters
- Use present tense

### Footer
- Breaking changes: "BREAKING CHANGE: ..."
- References to issues: "Closes #123"

### Example
```
feat: add idea approval workflow (add-idea-approval)

Implement the approval workflow from the change's spec deltas.
Adds status transitions and validation.

BREAKING CHANGE: Idea.status now includes "approved" state.

Generated with [Devin](https://devin.ai)

Co-Authored-By: Devin <158243242+devin-ai-integration[bot]@users.noreply.github.com>
```

## Pull Requests

### PR Title
- Follow commit message format
- Include the change name
- Example: `feat: add idea approval workflow (add-idea-approval)`

### PR Description
Use `.github/pull_request_template.md` — it records the OpenSpec change name (or a trivial-change tick) and the Definition of Done checklist.

### PR Requirements
- Non-trivial changes must reference an OpenSpec change under `openspec/changes/`
- Must pass all CI checks
- Must have at least one reviewer approval
- Must resolve all review comments

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
- Use merge commits (not rebase)
- Keep history clean
- Avoid force pushing

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
- No reviewer approval
- Merge conflicts not resolved

## Git Hooks

### Pre-commit
A minimal `.pre-commit-config.yaml` (local hooks only) runs ruff format, ruff check, and `openspec validate` on `openspec/` changes. Install it with:
```bash
uvx pre-commit install
```

### Commit-msg
Validate commit message format.

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
