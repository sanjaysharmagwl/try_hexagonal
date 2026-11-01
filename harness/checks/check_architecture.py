"""Architecture boundary check.

Enforces: harness/standards/architecture.md
"""

import ast
import re
import sys
from pathlib import Path


def imports_of(path: Path):
    """Return the set of top-level module names imported by a file."""
    mods = set()
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                mods.add(a.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(("." * node.level) + node.module)
    return mods


def check(root: Path) -> list[str]:
    """Return architecture violations under root/app."""
    violations = []
    app = root / "app"
    if not app.is_dir():
        return violations
    stdlib = set(sys.stdlib_module_names)
    for f in sorted(app.rglob("*.py")):
        rel = f.relative_to(root)
        parts = f.relative_to(app).parts
        feature = parts[0] if len(parts) > 1 else None
        mods = imports_of(f)
        if any(m == "main" or m.startswith("main.") for m in mods):
            violations.append(f"{rel}: must not import main")
        if f.name == "models.py" and feature:
            allowed = stdlib | {"pydantic", f"app.{feature}.models"}
            for m in mods:
                top = m.lstrip(".").split(".")[0]
                if m not in allowed and top not in stdlib and m != f"app.{feature}.models":
                    violations.append(
                        f"{rel}: models.py may only import stdlib, "
                        f"pydantic, and app.{feature}.models (found {m})"
                    )
        if f.name == "service.py":
            for m in mods:
                top = m.lstrip(".")
                if top.split(".")[0] in ("fastapi", "starlette"):
                    violations.append(f"{rel}: service.py must not import {top}")
                if (
                    re.search(r"\.(router|schemas|core)$", top)
                    or ".router" in top
                    or ".schemas" in top
                    or ".core" in top
                ):
                    violations.append(
                        f"{rel}: service.py must not import app.*.router/schemas/core (found {top})"
                    )
        if f.name == "repository.py":
            for m in mods:
                if m.lstrip(".").split(".")[0] in ("fastapi", "starlette"):
                    violations.append(f"{rel}: repository.py must not import {m}")
        if f.name == "router.py":
            for m in mods:
                if re.search(r"\.repository$", m.lstrip(".")):
                    violations.append(f"{rel}: router.py must not import {m}")
    return violations


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    violations = check(root)
    for v in violations:
        print(v)
    print(
        "OK: architecture checks passed"
        if not violations
        else f"FAILED: {len(violations)} violation(s)"
    )
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
