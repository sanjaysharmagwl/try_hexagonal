#!/usr/bin/env python3
"""
Secret scan check.

Enforces security standards from harness/standards/security.md:
- No API keys in code
- No passwords in code
- No tokens in code
- No private keys in code
"""

import re
import sys
from pathlib import Path


SECRET_PATTERNS = [
    (r"api[_-]?key\s*=\s*['\"][^'\"]{10,}['\"]", "API key"),
    (r"password\s*=\s*['\"][^'\"]{8,}['\"]", "Password"),
    (r"token\s*=\s*['\"][^'\"]{20,}['\"]", "Token"),
    (r"secret\s*=\s*['\"][^'\"]{10,}['\"]", "Secret"),
    (r"-----BEGIN.*PRIVATE KEY-----", "Private key"),
]


def check_file(file_path: Path) -> bool:
    """Check a single file for secrets."""
    with open(file_path, "r") as f:
        content = f.read()

    all_passed = True
    for pattern, description in SECRET_PATTERNS:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            line_num = content[:match.start()].count("\n") + 1
            print(f"ERROR: {file_path}:{line_num} possible {description}")
            all_passed = False

    return all_passed


def main():
    """Run secret scan on all files."""
    app_dir = Path("app")
    if not app_dir.exists():
        print("ERROR: app/ directory not found")
        return 1

    all_passed = True
    for py_file in app_dir.rglob("*.py"):
        if not check_file(py_file):
            all_passed = False

    if all_passed:
        print("OK: Secret scan passed")
        return 0
    else:
        print("FAILED: Secret scan failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
