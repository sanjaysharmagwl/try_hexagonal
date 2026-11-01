# Checks

This directory contains executable scripts that mechanically enforce the standards defined in `harness/standards/`.

## Available Checks

### Architecture Boundary Check
**File**: `check_architecture.py`
**Enforces**: `harness/standards/architecture.md`
**What it checks**:
- Domain layer has no external dependencies
- Application layer depends only on Domain
- Adapters depend on Application and Domain
- No circular dependencies

**Run**: `python harness/checks/check_architecture.py`

### Banned Patterns Check
**File**: `check_banned_patterns.py`
**Enforces**: `harness/standards/coding.md`
**What it checks**:
- No wildcard imports
- No bare except clauses
- No print statements in production code
- No commented-out code

**Run**: `python harness/checks/check_banned_patterns.py`

### Secret Scan
**File**: `check_secrets.py`
**Enforces**: `harness/standards/security.md`
**What it checks**:
- No API keys in code
- No passwords in code
- No tokens in code
- No private keys in code

**Run**: `python harness/checks/check_secrets.py`

## Adding New Checks

To add a new check:

1. Create a Python script in this directory
2. Name it `check_<name>.py`
3. Implement the check logic
4. Return exit code 0 on success, 1 on failure
5. Document it in this README
6. Add it to CI workflow

## Check Standards

All checks must:
- Be executable as standalone scripts
- Return 0 on success, non-zero on failure
- Print clear error messages
- Be fast (< 5 seconds)
- Have no external dependencies beyond standard library
