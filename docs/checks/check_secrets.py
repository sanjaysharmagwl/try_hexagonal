"""Committed-secret scan.

Enforces: docs/standards/security.md
"""

import re
import subprocess
import sys
from pathlib import Path

PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (
        re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
        "hardcoded credential",
    ),
]
SKIP = {"uv.lock"}


def tracked_files(root: Path):
    try:
        r = subprocess.run(
            ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
        )
        return [root / line for line in r.stdout.splitlines() if line.strip()]
    except Exception:
        return [p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]


def check(root: Path) -> list[str]:
    """Return secret-scan violations across tracked files."""
    violations = []
    for f in tracked_files(root):
        if f.name in SKIP or not f.exists():
            continue
        try:
            text = f.read_text()
        except (UnicodeDecodeError, ValueError):
            continue  # binary
        rel = f.relative_to(root).as_posix()
        # skip this check and its own test files (they contain fixture secrets)
        if "check_secrets" in f.name or rel.startswith("docs/checks/tests/"):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for pat, desc in PATTERNS:
                if pat.search(line):
                    violations.append(f"{f.relative_to(root)}:{i}: possible {desc}")
    return violations


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    violations = check(root)
    for v in violations:
        print(v)
    print("OK: secret scan passed" if not violations else f"FAILED: {len(violations)} violation(s)")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
