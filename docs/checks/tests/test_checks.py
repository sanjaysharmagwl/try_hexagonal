"""Unit tests for docs/checks."""

import sys
from pathlib import Path

CHECKS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CHECKS))

import check_banned_patterns  # noqa: E402
import check_secrets  # noqa: E402


def make_src(root):
    (root / "packages" / "core" / "src" / "core" / "ideas").mkdir(parents=True)
    return root / "packages" / "core" / "src" / "core" / "ideas"


# ---------- check_banned_patterns ----------


def test_banned_ok(tmp_path):
    (make_src(tmp_path) / "service.py").write_text("x = 1\n")
    assert check_banned_patterns.check(tmp_path) == []


def test_banned_violations(tmp_path):
    (make_src(tmp_path) / "service.py").write_text(
        "from x import *\nprint('hi')\ntry:\n    pass\nexcept:\n    pass\n"
    )
    v = check_banned_patterns.check(tmp_path)
    assert len(v) == 3


# ---------- check_secrets ----------


def test_secrets_ok(tmp_path):
    (tmp_path / "a.py").write_text("x = 1\n")
    assert check_secrets.check(tmp_path) == []


def test_secrets_violation(tmp_path):
    (tmp_path / "a.py").write_text('aws = "AKIAIOSFODNN7EXAMPLE"\n')
    assert check_secrets.check(tmp_path)


def test_secrets_password(tmp_path):
    (tmp_path / "a.py").write_text('password = "supersecretpw"\n')
    assert check_secrets.check(tmp_path)
