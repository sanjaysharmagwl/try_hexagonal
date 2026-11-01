#!/usr/bin/env python3
"""
Banned patterns check.

Enforces coding standards from harness/standards/coding.md:
- No wildcard imports
- No bare except clauses
- No print statements in production code
- No commented-out code
"""

import ast
import re
import sys
from pathlib import Path


BANNED_PATTERNS = [
    (r"from .* import \*", "Wildcard import"),
    (r"except\s*:", "Bare except clause"),
    (r"print\(", "Print statement in production code"),
]


def check_file(file_path: Path) -> bool:
    """Check a single file for banned patterns."""
    with open(file_path, "r") as f:
        content = f.read()

    all_passed = True
    for pattern, description in BANNED_PATTERNS:
        if re.search(pattern, content):
            print(f"ERROR: {file_path} contains {description}")
            all_passed = False

    # Check for commented-out code (heuristic)
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") and any(c in stripped for c in ["=", "def ", "class ", "import "]):
            # Skip if it's a comment explaining code
            if not any(word in stripped.lower() for word in ["todo", "fixme", "hack", "note"]):
                print(f"WARNING: {file_path}:{i} possible commented-out code: {stripped[:50]}")

    return all_passed


def main():
    """Run banned pattern checks on all Python files."""
    app_dir = Path("app")
    if not app_dir.exists():
        print("ERROR: app/ directory not found")
        return 1

    all_passed = True
    for py_file in app_dir.rglob("*.py"):
        if not check_file(py_file):
            all_passed = False

    if all_passed:
        print("OK: Banned pattern checks passed")
        return 0
    else:
        print("FAILED: Banned pattern checks failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
