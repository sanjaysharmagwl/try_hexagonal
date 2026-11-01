"""Tests for the CP CLI (tools/cp/cp.py)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import cp  # noqa: E402

REPO = Path(__file__).resolve().parents[3]


@pytest.fixture()
def repo(tmp_path):
    """A minimal CP repo rooted at tmp_path."""
    tmpl = tmp_path / "proposals" / "0000-template"
    tmpl.mkdir(parents=True)
    for name in ("proposal.md", "spec.md", "plan.md", "log.md"):
        (tmpl / name).write_text((REPO / "proposals" / "0000-template" / name).read_text())
    (tmp_path / "proposals" / "README.md").write_text(
        "# Change Proposals\n\n<!-- cp-index:start -->\nOLD\n<!-- cp-index:end -->\n\nfooter\n"
    )
    return tmp_path


def new(repo, title="Test CP"):
    assert cp.main(["new", title, "--author", "alice"], root=repo) == 0
    return next(d for d in (repo / "proposals").iterdir() if d.name != "0000-template" and d.is_dir())


def set_status(repo, n, state, by=None, extra=None):
    argv = ["status", str(n), state]
    if by:
        argv += ["--by", by]
    if extra:
        argv += extra
    return cp.main(argv, root=repo)


def fill_spec(cp_dir, approved=False):
    spec = cp_dir / "spec.md"
    text = spec.read_text()
    if approved:
        text = text.replace("approved_by:", "approved_by: bob")
        text = text.replace("approved_on:", "approved_on: 2026-11-02")
    spec.write_text(text)


def make_spec_approved(repo, cp_dir):
    set_status(repo, 1, "Proposed")
    assert set_status(repo, 1, "Accepted", by="bob") == 0
    assert cp.main(["spec", "1"], root=repo) == 0
    fill_spec(cp_dir, approved=True)
    assert set_status(repo, 1, "Specified") == 0
    assert set_status(repo, 1, "Spec-Approved", by="bob") == 0


def make_plan(repo, cp_dir):
    assert cp.main(["plan", "1"], root=repo) == 0
    plan = cp_dir / "plan.md"
    plan.write_text(plan.read_text().replace(
        "- **Tests**: <test function names>", "- **Tests**: test_x"))


# ---------- new ----------

def test_new_creates_numbered_cp(repo, capsys):
    d = new(repo, "My First Thing")
    assert d.name == "0001-my-first-thing"
    fm = cp.parse_fm(d / "proposal.md")
    assert fm["id"] == "CP-0001"
    assert fm["status"] == "Draft"
    assert fm["author"] == "alice"
    assert "created as Draft by alice" in (d / "log.md").read_text()
    assert "CP-0001" in (repo / "proposals" / "README.md").read_text()


def test_new_second_cp_gets_0002(repo):
    new(repo)
    d2 = new(repo, "Second")
    assert d2.name.startswith("0002-")


# ---------- status ----------

def test_status_prints_current(repo, capsys):
    new(repo)
    assert cp.main(["status", "CP-0001"], root=repo) == 0
    assert capsys.readouterr().out.strip().splitlines()[-1] == "Draft"


def test_status_id_formats(repo, capsys):
    new(repo)
    for arg in ("1", "0001", "CP-0001"):
        assert cp.main(["status", arg], root=repo) == 0
    capsys.readouterr()


def test_invalid_transition_rejected(repo, capsys):
    new(repo)
    assert set_status(repo, 1, "Implemented") == 1
    assert "invalid transition" in capsys.readouterr().err


def test_gate_requires_by(repo, capsys):
    new(repo)
    set_status(repo, 1, "Proposed")
    assert set_status(repo, 1, "Accepted") == 1
    assert "--by" in capsys.readouterr().err
    assert set_status(repo, 1, "Accepted", by="bob") == 0


def test_rejected_requires_by(repo, capsys):
    new(repo)
    set_status(repo, 1, "Proposed")
    assert set_status(repo, 1, "Rejected") == 1
    assert set_status(repo, 1, "Rejected", by="bob") == 0


def test_specified_requires_spec_file(repo, capsys):
    new(repo)
    set_status(repo, 1, "Proposed")
    set_status(repo, 1, "Accepted", by="bob")
    assert set_status(repo, 1, "Specified") == 1
    assert "spec.md" in capsys.readouterr().err


def test_g2_requires_approved_fields(repo, capsys):
    new(repo)
    set_status(repo, 1, "Proposed")
    set_status(repo, 1, "Accepted", by="bob")
    cp.main(["spec", "1"], root=repo)
    set_status(repo, 1, "Specified")
    d = next(repo.glob("proposals/0001-*"))
    assert set_status(repo, 1, "Spec-Approved", by="bob") == 1
    assert "approved_by" in capsys.readouterr().err
    fill_spec(d, approved=True)
    assert set_status(repo, 1, "Spec-Approved", by="bob") == 0
    assert cp.parse_fm(d / "spec.md")["status"] == "Approved"


def test_planned_requires_plan_file(repo, capsys):
    d = new(repo)
    make_spec_approved(repo, d)
    assert set_status(repo, 1, "Planned") == 1
    assert "plan.md" in capsys.readouterr().err


def test_g3_requires_lint_clean(repo, capsys):
    d = new(repo)
    make_spec_approved(repo, d)
    cp.main(["plan", "1"], root=repo)
    set_status(repo, 1, "Planned")
    # template task references REQ-001 which exists; make it dirty instead
    (d / "plan.md").write_text((d / "plan.md").read_text().replace(
        "- **Status**: todo", "- **Status**: doing"))
    assert set_status(repo, 1, "In-Progress", by="bob") == 1
    (d / "plan.md").write_text((d / "plan.md").read_text().replace(
        "- **Status**: doing", "- **Status**: todo").replace(
        "- **Tests**: <test function names>", "- **Tests**: test_x"))
    assert set_status(repo, 1, "In-Progress", by="bob") == 0
    assert cp.parse_fm(d / "plan.md")["status"] == "Approved"


def test_implemented_requires_all_tasks_done(repo, capsys):
    d = new(repo)
    make_spec_approved(repo, d)
    make_plan(repo, d)
    set_status(repo, 1, "Planned")
    set_status(repo, 1, "In-Progress", by="bob")
    assert set_status(repo, 1, "Implemented") == 1
    plan = d / "plan.md"
    plan.write_text(plan.read_text().replace("- **Status**: todo", "- **Status**: done"))
    assert set_status(repo, 1, "Implemented") == 0


def test_closed_requires_dod_signoff(repo, capsys):
    d = new(repo)
    make_spec_approved(repo, d)
    make_plan(repo, d)
    set_status(repo, 1, "Planned")
    set_status(repo, 1, "In-Progress", by="bob")
    plan = d / "plan.md"
    plan.write_text(plan.read_text().replace("- **Status**: todo", "- **Status**: done"))
    set_status(repo, 1, "Implemented")
    assert set_status(repo, 1, "Closed", by="bob") == 1
    assert "DoD Sign-Off" in capsys.readouterr().err
    log = d / "log.md"
    log.write_text(log.read_text().replace("Status: PENDING", "Status: PASSED"))
    assert set_status(repo, 1, "Closed", by="bob") == 0


def test_deferred_reopen_and_superseded(repo, capsys):
    d = new(repo)
    set_status(repo, 1, "Proposed")
    assert set_status(repo, 1, "Deferred", by="bob") == 0
    assert set_status(repo, 1, "Proposed") == 0  # re-open, no --by needed
    assert set_status(repo, 1, "Superseded", by="bob",
                      extra=["--superseded-by", "CP-0002"]) == 0
    assert cp.parse_fm(d / "proposal.md")["superseded_by"] == "CP-0002"
    hist = (d / "log.md").read_text()
    assert "Proposed -> Deferred by bob" in hist


def test_history_appended(repo):
    d = new(repo)
    set_status(repo, 1, "Proposed")
    set_status(repo, 1, "Accepted", by="bob")
    hist = (d / "log.md").read_text()
    assert "Draft -> Proposed" in hist
    assert "Proposed -> Accepted by bob (G1)" in hist


# ---------- spec / plan scaffolding ----------

def test_spec_requires_accepted(repo, capsys):
    new(repo)
    assert cp.main(["spec", "1"], root=repo) == 1
    assert "Accepted" in capsys.readouterr().err


def test_spec_and_plan_scaffold(repo):
    d = new(repo)
    set_status(repo, 1, "Proposed")
    set_status(repo, 1, "Accepted", by="bob")
    assert cp.main(["spec", "1"], root=repo) == 0
    assert (d / "spec.md").exists()
    assert "CP-0001" in (d / "spec.md").read_text()
    assert cp.main(["spec", "1"], root=repo) == 1  # exists already
    assert cp.main(["plan", "1"], root=repo) == 1  # wrong status


# ---------- lint ----------

def test_lint_clean_cp(repo, capsys):
    new(repo)
    assert cp.main(["lint"], root=repo) == 0
    assert "0 problem(s)" in capsys.readouterr().out


def test_lint_duplicate_req(repo, capsys):
    d = new(repo)
    make_spec_approved(repo, d)
    spec = d / "spec.md"
    spec.write_text(spec.read_text().replace(
        "## Interfaces & Data Contracts",
        "### REQ-001: dup\n\nMUST x\n\n- Given a\n- When b\n- Then c\n\n"
        "## Interfaces & Data Contracts"))
    assert cp.main(["lint", "1"], root=repo) == 1
    assert "duplicate REQ-001" in capsys.readouterr().out


def test_lint_req_missing_from_matrix(repo, capsys):
    d = new(repo)
    make_spec_approved(repo, d)
    make_plan(repo, d)
    spec = d / "spec.md"
    spec.write_text(spec.read_text().replace(
        "## Interfaces & Data Contracts",
        "### REQ-002: extra\n\nMUST x\n\n- Given a\n- When b\n- Then c\n\n"
        "## Interfaces & Data Contracts"))
    set_status(repo, 1, "Planned")
    assert cp.main(["lint", "1"], root=repo) == 1
    assert "REQ-002 missing from traceability matrix" in capsys.readouterr().out


def test_lint_task_without_req(repo, capsys):
    d = new(repo)
    make_spec_approved(repo, d)
    cp.main(["plan", "1"], root=repo)
    plan = d / "plan.md"
    plan.write_text(plan.read_text().replace(
        "- **Requirements**: REQ-001", "- **Requirements**: none").replace(
        "- **Tests**: <test function names>", "- **Tests**: test_x"))
    assert cp.main(["lint", "1"], root=repo) == 1
    assert "no Requirements" in capsys.readouterr().out


def test_lint_unknown_req_referenced(repo, capsys):
    d = new(repo)
    make_spec_approved(repo, d)
    cp.main(["plan", "1"], root=repo)
    plan = d / "plan.md"
    plan.write_text(plan.read_text().replace(
        "- **Requirements**: REQ-001", "- **Requirements**: REQ-099").replace(
        "- **Tests**: <test function names>", "- **Tests**: test_x"))
    assert cp.main(["lint", "1"], root=repo) == 1
    assert "unknown REQ-099" in capsys.readouterr().out


def test_lint_broken_link(repo, capsys):
    d = new(repo)
    prop = d / "proposal.md"
    prop.write_text(prop.read_text() + "\nsee [x](nope.md)\n")
    assert cp.main(["lint", "1"], root=repo) == 1
    assert "broken link" in capsys.readouterr().out


def test_lint_bad_history_chain(repo, capsys):
    d = new(repo)
    set_status(repo, 1, "Proposed")
    log = d / "log.md"
    log.write_text(log.read_text().replace(
        "## Status History\n",
        "## Status History\n\n- 2026-11-03 Specified -> Planned by x\n"))
    assert cp.main(["lint", "1"], root=repo) == 1
    out = capsys.readouterr().out
    assert "invalid transition" in out


def test_lint_status_consistency(repo, capsys):
    d = new(repo)
    fm = {"status": "Planned"}
    cp.set_fm(d / "proposal.md", fm)
    assert cp.main(["lint", "1"], root=repo) == 1
    out = capsys.readouterr().out
    assert "requires spec.md" in out and "requires plan.md" in out


# ---------- index ----------

def test_index_preserves_surrounding_text(repo):
    readme = repo / "proposals" / "README.md"
    before = readme.read_text()
    new(repo, "Indexed One")
    new(repo, "Indexed Two")
    cp.main(["index"], root=repo)
    after = readme.read_text()
    assert after.startswith("# Change Proposals")
    assert "footer" in after
    assert "CP-0001 | Indexed One" in after and "CP-0002 | Indexed Two" in after
    assert "<!-- cp-index:start -->" in after and "<!-- cp-index:end -->" in after
    assert "OLD" not in after


# ---------- next ----------

def test_next_respects_dependencies(repo, capsys):
    d = new(repo)
    make_spec_approved(repo, d)
    cp.main(["plan", "1"], root=repo)
    plan = d / "plan.md"
    text = plan.read_text().replace(
        "- **Tests**: <test function names>", "- **Tests**: test_x")
    second = """
### T-002: second task

- **Status**: todo
- **Requirements**: REQ-001
- **Depends on**: T-001
- **Files**: f
- **Tests**: test_y
- **Done when**: done
- **Size**: S
- **Description**: second
"""
    plan.write_text(text.replace(
        "## Traceability Matrix", second + "\n## Traceability Matrix"))
    set_status(repo, 1, "Planned")
    set_status(repo, 1, "In-Progress", by="bob")
    assert cp.main(["next", "1"], root=repo) == 0
    out = capsys.readouterr().out
    assert "T-001" in out
    plan.write_text(plan.read_text().replace(
        "### T-001: <task title>\n\n- **Status**: todo",
        "### T-001: <task title>\n\n- **Status**: done"))
    assert cp.main(["next", "1"], root=repo) == 0
    assert "T-002" in capsys.readouterr().out


def test_next_all_done(repo, capsys):
    d = new(repo)
    make_spec_approved(repo, d)
    make_plan(repo, d)
    set_status(repo, 1, "Planned")
    set_status(repo, 1, "In-Progress", by="bob")
    plan = d / "plan.md"
    plan.write_text(plan.read_text().replace("- **Status**: todo", "- **Status**: done"))
    assert cp.main(["next", "1"], root=repo) == 0
    assert "All tasks done" in capsys.readouterr().out


def test_next_warns_when_not_in_progress(repo, capsys):
    d = new(repo)
    make_spec_approved(repo, d)
    make_plan(repo, d)
    set_status(repo, 1, "Planned")
    assert cp.main(["next", "1"], root=repo) == 0
    assert "warning" in capsys.readouterr().err
