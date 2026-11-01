"""Run every local harness check (excludes CI-only check_pr_reference.py)."""

import importlib.util
import sys
from pathlib import Path

CHECKS_DIR = Path(__file__).resolve().parent
ROOT = CHECKS_DIR.parents[1]


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    failed = 0
    for path in sorted(CHECKS_DIR.glob("check_*.py")):
        if path.name == "check_pr_reference.py":
            continue
        violations = load(path).check(ROOT)
        status = "PASS" if not violations else "FAIL"
        print(f"[{status}] {path.name}")
        for v in violations:
            print(f"    {v}")
        failed += bool(violations)
    print("all checks passed" if not failed else f"{failed} check(s) failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
