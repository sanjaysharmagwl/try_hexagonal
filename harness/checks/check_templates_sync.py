"""Templates sync check: harness/templates must match proposals/0000-template.

Enforces: harness/standards/docs.md
"""

import sys
from pathlib import Path

FILES = ["proposal.md", "spec.md", "plan.md"]


def check(root: Path) -> list[str]:
    """Return violations when templates diverge from proposals/0000-template."""
    violations = []
    for name in FILES:
        a = root / "harness" / "templates" / name
        b = root / "proposals" / "0000-template" / name
        if not a.exists():
            violations.append(f"{a}: missing")
            continue
        if not b.exists():
            violations.append(f"{b}: missing")
            continue
        if a.read_bytes() != b.read_bytes():
            violations.append(f"{name}: harness/templates and proposals/0000-template diverge")
    return violations


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    violations = check(root)
    for v in violations:
        print(v)
    print("OK: templates in sync" if not violations else f"FAILED: {len(violations)} violation(s)")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
