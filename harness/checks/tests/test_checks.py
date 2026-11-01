"""Unit tests for harness/checks."""

import sys
from pathlib import Path

CHECKS = Path(__file__).resolve().parents[1]
REPO = CHECKS.parents[1]
sys.path.insert(0, str(CHECKS))
sys.path.insert(0, str(REPO / "tools" / "cp"))

import check_architecture  # noqa: E402
import check_banned_patterns  # noqa: E402
import check_pr_reference  # noqa: E402
import check_secrets  # noqa: E402
import check_templates_sync  # noqa: E402


def make_app(root):
    (root / "app" / "ideas").mkdir(parents=True)


# ---------- check_architecture ----------


def test_architecture_ok(tmp_path):
    make_app(tmp_path)
    (tmp_path / "app" / "ideas" / "models.py").write_text(
        "from pydantic import BaseModel\n\nclass X(BaseModel):\n    pass\n"
    )
    (tmp_path / "app" / "ideas" / "service.py").write_text("from app.ideas.models import X\n")
    assert check_architecture.check(tmp_path) == []


def test_architecture_violation(tmp_path):
    make_app(tmp_path)
    (tmp_path / "app" / "ideas" / "service.py").write_text(
        "import fastapi\nfrom app.ideas.router import router\n"
    )
    v = check_architecture.check(tmp_path)
    assert any("fastapi" in x for x in v)


def test_architecture_models_external(tmp_path):
    make_app(tmp_path)
    (tmp_path / "app" / "ideas" / "models.py").write_text("import requests\n")
    assert check_architecture.check(tmp_path)


# ---------- check_banned_patterns ----------


def test_banned_ok(tmp_path):
    make_app(tmp_path)
    (tmp_path / "app" / "ideas" / "service.py").write_text("x = 1\n")
    assert check_banned_patterns.check(tmp_path) == []


def test_banned_violations(tmp_path):
    make_app(tmp_path)
    (tmp_path / "app" / "ideas" / "service.py").write_text(
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


# ---------- check_templates_sync ----------


def test_templates_sync_ok(tmp_path):
    (tmp_path / "harness" / "templates").mkdir(parents=True)
    (tmp_path / "proposals" / "0000-template").mkdir(parents=True)
    for n in check_templates_sync.FILES:
        (tmp_path / "harness" / "templates" / n).write_text("x")
        (tmp_path / "proposals" / "0000-template" / n).write_text("x")
    assert check_templates_sync.check(tmp_path) == []


def test_templates_sync_diverged(tmp_path):
    (tmp_path / "harness" / "templates").mkdir(parents=True)
    (tmp_path / "proposals" / "0000-template").mkdir(parents=True)
    for n in check_templates_sync.FILES:
        (tmp_path / "harness" / "templates" / n).write_text("x")
        (tmp_path / "proposals" / "0000-template" / n).write_text("y")
    assert len(check_templates_sync.check(tmp_path)) == 3


# ---------- check_pr_reference ----------


def test_pr_reference_skipped(tmp_path, monkeypatch):
    for v in ("PR_BODY", "PR_TITLE", "PR_LABELS", "CHANGED_FILES"):
        monkeypatch.delenv(v, raising=False)
    assert check_pr_reference.check(tmp_path) == []


def test_pr_reference_no_app_changes(tmp_path, monkeypatch):
    monkeypatch.setenv("PR_TITLE", "docs: x")
    monkeypatch.setenv("PR_BODY", "")
    monkeypatch.setenv("PR_LABELS", "")
    monkeypatch.setenv("CHANGED_FILES", "README.md\n")
    assert check_pr_reference.check(tmp_path) == []


def test_pr_reference_trivial_label(tmp_path, monkeypatch):
    monkeypatch.setenv("PR_TITLE", "fix: typo")
    monkeypatch.setenv("PR_BODY", "")
    monkeypatch.setenv("PR_LABELS", "trivial")
    monkeypatch.setenv("CHANGED_FILES", "app/ideas/models.py\n")
    assert check_pr_reference.check(tmp_path) == []


def test_pr_reference_missing_cp(tmp_path, monkeypatch):
    monkeypatch.setenv("PR_TITLE", "feat: x")
    monkeypatch.setenv("PR_BODY", "")
    monkeypatch.setenv("PR_LABELS", "")
    monkeypatch.setenv("CHANGED_FILES", "app/ideas/models.py\n")
    assert check_pr_reference.check(tmp_path)


def test_pr_reference_in_progress(tmp_path, monkeypatch):
    d = tmp_path / "proposals" / "0001-x"
    d.mkdir(parents=True)
    (d / "proposal.md").write_text("---\nid: CP-0001\nstatus: In-Progress\n---\n")
    monkeypatch.setenv("PR_TITLE", "feat: x (CP-0001)")
    monkeypatch.setenv("PR_BODY", "")
    monkeypatch.setenv("PR_LABELS", "")
    monkeypatch.setenv("CHANGED_FILES", "app/ideas/models.py\n")
    assert check_pr_reference.check(tmp_path) == []


def test_pr_reference_wrong_status(tmp_path, monkeypatch):
    d = tmp_path / "proposals" / "0001-x"
    d.mkdir(parents=True)
    (d / "proposal.md").write_text("---\nid: CP-0001\nstatus: Draft\n---\n")
    monkeypatch.setenv("PR_TITLE", "")
    monkeypatch.setenv("PR_BODY", "implements CP-0001")
    monkeypatch.setenv("PR_LABELS", "")
    monkeypatch.setenv("CHANGED_FILES", "main.py\n")
    v = check_pr_reference.check(tmp_path)
    assert any("In-Progress" in x for x in v)
