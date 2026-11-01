"""Banned code patterns check.

Enforces: harness/standards/coding.md
"""

import ast
import sys
from pathlib import Path

BANNED_CALLS = {"print", "breakpoint", "pdb.set_trace"}


def _call_name(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _call_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return ""


def check(root: Path) -> list[str]:
    """Return banned-pattern violations in app/ and main.py."""
    violations = []
    files = list((root / "app").rglob("*.py")) if (root / "app").is_dir() else []
    if (root / "main.py").exists():
        files.append(root / "main.py")
    for f in sorted(files):
        rel = f.relative_to(root)
        tree = ast.parse(f.read_text(), filename=str(f))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and any(a.name == "*" for a in node.names):
                violations.append(f"{rel}:{node.lineno}: wildcard import")
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                violations.append(f"{rel}:{node.lineno}: bare except")
            if isinstance(node, ast.Call) and _call_name(node.func) in BANNED_CALLS:
                violations.append(f"{rel}:{node.lineno}: banned call {_call_name(node.func)}()")
    return violations


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    violations = check(root)
    for v in violations:
        print(v)
    print(
        "OK: banned-pattern checks passed"
        if not violations
        else f"FAILED: {len(violations)} violation(s)"
    )
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
