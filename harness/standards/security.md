# Security Standards

This document defines security practices for this repository.

## Secrets Management

### Never Commit Secrets
Never commit:
- API keys
- Database passwords
- Access tokens
- Private keys
- Certificates
- Environment-specific configuration

### Environment Variables
Use environment variables for secrets:
```python
import os

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")
```

### Secret Storage
- Use environment variables or secret managers
- Document required variables in README
- Provide example `.env.example` file

## Input Validation

### Validate All Inputs
- HTTP request bodies: Use Pydantic models
- Query parameters: Use Pydantic models
- Path parameters: Validate type and format
- File uploads: Validate type, size, content

### Sanitization
- Escape user-generated content before display
- Validate file paths (prevent directory traversal)
- Validate URLs (prevent SSRF)

### Length Limits
- Enforce maximum lengths on strings
- Limit array/list sizes
- Validate numeric ranges

## Authentication and Authorization

### Authentication
- Use industry-standard libraries (e.g., FastAPI Security)
- Never implement crypto yourself
- Use strong algorithms (Argon2, bcrypt)
- Store password hashes only

### Authorization
- Check permissions on every protected endpoint
- Use principle of least privilege
- Log authorization failures
- Never rely on client-side checks

## Dependencies

### Dependency Policy
- Review new dependencies before adding
- Prefer actively maintained libraries
- Check for known vulnerabilities
- Use `uv` lock file for reproducibility

### Minimum Age
- Prefer dependencies published at least 7 days ago
- Avoid brand-new versions (supply chain risk)
- Pin versions in lock file

### Auditing
Run security audit regularly:
```bash
# Audit dependencies for known vulnerabilities (optional, not run in CI) <!-- inferred: confirm -->
uvx pip-audit

# Review dependencies
uv pip list --outdated
```

The lock file `uv.lock` MUST be committed so audits and installs are reproducible.

### Secret Scanning
Committed files are scanned by `harness/checks/check_secrets.py` (run locally and via `harness/checks/run_all.py`).

## SQL Injection

### Use Parameterized Queries
Never concatenate strings into SQL:
```python
# Bad
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# Good
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### ORMs
Use ORMs with built-in protection (SQLAlchemy, etc.)

## XSS Prevention

### Escaping
- Escape user-generated content
- Use template engines with auto-escaping
- Sanitize HTML if allowing user HTML

### Content Security Policy
- Configure CSP headers
- Restrict script sources
- Use nonces or hashes

## Logging

### What to Log
- Security events (auth failures, authorization failures)
- Errors with context
- Audit trail for sensitive operations

### What NOT to Log
- Passwords
- API keys
- Personal identifiers (PII)
- Request bodies with sensitive data

### Log Sanitization
Sanitize sensitive data before logging:
```python
# Bad
logger.info(f"User logged in: {user.email}, password: {password}")

# Good
logger.info(f"User logged in: {user.email}")
```

## Error Handling

### Don't Leak Information
- Return generic error messages to users
- Log detailed errors server-side
- Don't expose stack traces in production

### Custom Error Pages
- Custom 404, 500 pages
- No debug information in production

## HTTPS

### Always Use HTTPS
- Redirect HTTP to HTTPS
- Use HSTS headers
- Valid TLS certificates

### TLS Configuration
- Use strong cipher suites
- Disable outdated protocols (SSLv3, TLS 1.0, 1.1)
- Keep certificates updated

## Code Review Security Checklist

When reviewing code, check:
- [ ] No secrets committed
- [ ] All inputs validated
- [ ] Authorization checked
- [ ] SQL uses parameterized queries
- [ ] User output escaped
- [ ] No sensitive data logged
- [ ] Error messages are generic
- [ ] Dependencies reviewed
- [ ] No hardcoded credentials

## Vulnerability Reporting

If you find a security vulnerability:
1. Do NOT open a public issue
2. Contact maintainers privately
3. Allow time for fix before disclosure
4. Follow responsible disclosure

## Tools

### Security Scanning
Consider adding:
- `bandit` for Python security linting
- `safety` for dependency vulnerability checking
- `pip-audit` for known vulnerabilities

### Running Security Checks
```bash
# Bandit
bandit -r app/

# Safety
safety check

# Pip-audit
pip-audit
```
