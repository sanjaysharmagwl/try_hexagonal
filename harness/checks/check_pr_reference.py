"""PR CP-reference check (CI only).

Enforces: harness/standards/git.md and harness/workflow/lifecycle.md
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "cp"))
import cp  # noqa: E402


def check(root: Path) -> list[str]:
    """Return violations; empty when env not provided (local run)."""
    body = os.environ.get("PR_BODY")
    title = os.environ.get("PR_TITLE")
    labels = os.environ.get("PR_LABELS", "")
    changed = os.environ.get("CHANGED_FILES", "")
    if body is None and title is None:
        print("skipped: PR_* env not provided (local run)")
        return []
    if "trivial" in {x.strip() for x in labels.split(",")}:
        return []
    touched = [x for x in changed.splitlines() if x.startswith("app/") or x == "main.py"]
    if not touched:
        return []
    text = f"{title or ''}\n{body or ''}"
    ids = set(re.findall(r"CP-\d{4}", text))
    if not ids:
        return [f"PR touches app code {touched} but references no CP-NNNN"]
    bad = []
    for cid in ids:
        d = cp.find_cp(root, cid)
        if not d:
            bad.append(f"{cid}: no proposal directory found")
            continue
        status = (cp.parse_fm(d / "proposal.md") or {}).get("status")
        if status != "In-Progress":
            bad.append(f"{cid}: status is {status}, must be In-Progress")
    return bad


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    violations = check(root)
    for v in violations:
        print(v)
    if violations:
        print(f"FAILED: {len(violations)} violation(s)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
