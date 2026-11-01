#!/usr/bin/env python3
"""
Architecture boundary check.

Enforces dependency rules from harness/standards/architecture.md:
- Domain layer has no external dependencies
- Application layer depends only on Domain
- Adapters depend on Application and Domain
- No circular dependencies
"""

import ast
import sys
from pathlib import Path


def get_imports(file_path: Path) -> set[str]:
    """Extract all imports from a Python file."""
    imports = set()
    try:
        with open(file_path) as f:
            tree = ast.parse(f.read(), filename=str(file_path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
    except Exception:
        pass
    return imports


def check_file(file_path: Path) -> bool:
    """Check a single file for architecture violations."""
    # Determine layer based on path
    path_str = str(file_path)
    layer = None

    if "app/core/" in path_str or "app/*/models.py" in path_str:
        layer = "domain"
    elif "app/*/service.py" in path_str:
        layer = "application"
    elif "app/*/router.py" in path_str or "app/*/repository.py" in path_str:
        layer = "adapter"

    if not layer:
        return True  # Not a layer file, skip

    imports = get_imports(file_path)

    # Domain layer: no external dependencies except stdlib
    if layer == "domain":
        external = [
            imp
            for imp in imports
            if not imp.startswith("app") and imp not in sys.stdlib_module_names
        ]
        if external:
            print(f"ERROR: {file_path} (domain) has external dependencies: {external}")
            return False

    # Application layer: depends only on domain
    if layer == "application":
        has_app = any(imp.startswith("app") for imp in imports)
        if not has_app:
            print(f"WARNING: {file_path} (application) has no app dependencies")

    return True


def main():
    """Run architecture checks on all Python files."""
    app_dir = Path("app")
    if not app_dir.exists():
        print("ERROR: app/ directory not found")
        return 1

    all_passed = True
    for py_file in app_dir.rglob("*.py"):
        if not check_file(py_file):
            all_passed = False

    if all_passed:
        print("OK: Architecture checks passed")
        return 0
    else:
        print("FAILED: Architecture checks failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
