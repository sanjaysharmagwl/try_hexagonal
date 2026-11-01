"""Change Proposal (CP) CLI with lifecycle enforcement.

Enforces the lifecycle defined in harness/workflow/lifecycle.md.
"""

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

STATES = [
    "Draft", "Proposed", "Accepted", "Specified", "Spec-Approved",
    "Planned", "In-Progress", "Implemented", "Closed",
    "Rejected", "Deferred", "Withdrawn", "Superseded",
]

TRANSITIONS = {
    "Draft": {"Proposed", "Withdrawn"},
    "Proposed": {"Accepted", "Rejected", "Deferred", "Withdrawn"},
    "Accepted": {"Specified"},
    "Specified": {"Spec-Approved"},
    "Spec-Approved": {"Planned"},
    "Planned": {"In-Progress"},
    "In-Progress": {"Implemented"},
    "Implemented": {"Closed"},
    "Rejected": set(),
    "Deferred": {"Proposed"},
    "Withdrawn": set(),
    "Closed": set(),
}
# ->Superseded is allowed from any state
for s in TRANSITIONS:
    TRANSITIONS[s] = TRANSITIONS[s] | {"Superseded"}

GATES = {"Accepted": "G1", "Spec-Approved": "G2", "In-Progress": "G3", "Closed": "G4"}
NEEDS_BY = set(GATES) | {"Rejected", "Deferred", "Superseded"}

PROPOSAL_KEYS = ["id", "title", "author", "status", "created", "updated",
                 "supersedes", "superseded_by", "tags"]
SPEC_KEYS = ["id", "proposal", "status", "version", "approved_by", "approved_on"]
PLAN_KEYS = ["id", "spec", "status"]
LOG_KEYS = ["id"]

PROPOSAL_SECTIONS = ["Summary", "Motivation / Problem", "Goals", "Non-Goals",
                     "Proposed Solution", "Alternatives Considered", "Impact",
                     "Risks & Mitigations", "Open Questions", "Success Metrics"]
SPEC_SECTIONS = ["Overview", "Definitions", "Requirements",
                 "Interfaces & Data Contracts", "Error Handling & Edge Cases",
                 "Non-Functional Requirements", "Security & Privacy",
                 "Out of Scope", "Amendments"]
PLAN_SECTIONS = ["Approach & Architecture Notes", "Files in Scope", "Task List",
                 "Traceability Matrix", "Rollout / Migration / Rollback",
                 "Verification Steps"]

TASK_FIELDS = ["Status", "Requirements", "Depends on", "Files", "Tests",
               "Done when", "Size", "Description"]


def err(msg):
    print(msg, file=sys.stderr)


def parse_fm(path: Path):
    """Parse simple 'key: value' front matter. Returns dict or None."""
    if not path.exists():
        return None
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def set_fm(path: Path, updates: dict):
    """Update front matter keys in place, preserving everything else."""
    lines = path.read_text().splitlines()
    out, in_fm, done = [], False, set()
    for line in lines:
        if line.strip() == "---":
            in_fm = not in_fm
            if not in_fm:  # closing fence: insert missing keys before it
                for k, v in updates.items():
                    if k not in done:
                        out.append(f"{k}: {v}")
            out.append(line)
            continue
        if in_fm:
            m = re.match(r"^([A-Za-z_]+):", line)
            if m and m.group(1) in updates:
                out.append(f"{m.group(1)}: {updates[m.group(1)]}")
                done.add(m.group(1))
                continue
        out.append(line)
    path.write_text("\n".join(out) + "\n")


def sections(text: str):
    """Split markdown into {heading: body} for '## ' headings."""
    secs, cur, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur is not None:
                secs[cur] = "\n".join(buf)
            cur, buf = line[3:].strip(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        secs[cur] = "\n".join(buf)
    return secs


def subsections(body: str, pattern: str):
    """Find '### ID: title' blocks. Returns list of (id, title, block_text)."""
    matches = list(re.finditer(rf"^### ({pattern}): (.*)$", body, re.M))
    out = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        out.append((m.group(1), m.group(2).strip(), body[m.start():end]))
    return out


def find_cp(root: Path, cp_id: str):
    n = int(re.sub(r"^CP-", "", cp_id.strip(), flags=re.I))
    pdir = root / "proposals"
    if not pdir.exists():
        return None
    hits = [d for d in pdir.iterdir() if d.is_dir() and re.match(rf"^{n:04d}-", d.name)]
    if n == 0 and (pdir / "0000-template").is_dir():
        hits.append(pdir / "0000-template")
    return hits[0] if hits else None


def cp_num(cp_dir: Path):
    return cp_dir.name.split("-")[0]


def git_author(root: Path):
    try:
        r = subprocess.run(["git", "config", "user.name"], cwd=root,
                           capture_output=True, text=True)
        return r.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def parse_tasks(plan_text: str):
    secs = sections(plan_text)
    body = secs.get("Task List", "")
    tasks = []
    for tid, title, block in subsections(body, r"T-\d+"):
        fields = {}
        for m in re.finditer(r"^- \*\*([A-Za-z ]+)\*\*:\s*(.*)$", block, re.M):
            fields[m.group(1).strip()] = m.group(2).strip()
        tasks.append({"id": tid, "title": title, "block": block, "fields": fields})
    return tasks


def parse_reqs(spec_text: str):
    secs = sections(spec_text)
    return subsections(secs.get("Requirements", ""), r"REQ-\d+")


def parse_matrix(plan_text: str):
    """Return {REQ-id: [T-ids]} from the traceability matrix."""
    secs = sections(plan_text)
    rows = {}
    for line in secs.get("Traceability Matrix", "").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or cells[0] in ("REQ", "") or set(cells[0]) <= {"-", " "}:
            continue
        rows[cells[0]] = re.findall(r"T-\d+", cells[1] if len(cells) > 1 else "")
    return rows


def lint_cp(cp_dir: Path, root: Path, structural_only=False):
    """Lint one CP dir. Returns list of 'path: message' problems."""
    problems = []
    def bad(name, msg):
        problems.append(f"{cp_dir.name}/{name}: {msg}")

    if not (cp_dir / "proposal.md").exists():
        bad("proposal.md", "missing")
        return problems
    docs = {
        "proposal.md": (PROPOSAL_KEYS, PROPOSAL_SECTIONS),
        "spec.md": (SPEC_KEYS, SPEC_SECTIONS),
        "plan.md": (PLAN_KEYS, PLAN_SECTIONS),
        "log.md": (LOG_KEYS, []),
    }
    fms = {}
    texts = {}
    for name, (keys, _) in docs.items():
        p = cp_dir / name
        if not p.exists():
            continue
        fm = parse_fm(p)
        if fm is None or fm == {} and p.read_text().splitlines()[0].strip() != "---":
            bad(name, "missing front matter")
            continue
        fms[name] = fm
        for k in keys:
            if k not in fm:
                bad(name, f"front matter missing key '{k}'")
        texts[name] = p.read_text()

    num = cp_num(cp_dir)
    if cp_dir.name == "0000-template":
        expected = "CP-0000"
    else:
        expected = f"CP-{num}"
    pf = fms.get("proposal.md", {})
    if pf.get("id") != expected:
        bad("proposal.md", f"front matter id '{pf.get('id')}' does not match dir '{expected}'")
    if pf.get("status") not in STATES:
        bad("proposal.md", f"unknown status '{pf.get('status')}'")

    for name, (_, wanted) in docs.items():
        if name not in texts:
            continue
        have = sections(texts[name])
        for s in wanted:
            if s not in have:
                bad(name, f"missing '## {s}' section")

    if structural_only:
        return problems

    # --- spec requirement checks ---
    req_ids = []
    if "spec.md" in texts:
        seen = set()
        for rid, title, block in parse_reqs(texts["spec.md"]):
            if rid in seen:
                bad("spec.md", f"duplicate {rid}")
            seen.add(rid)
            req_ids.append(rid)
            if not re.search(r"\b(MUST|SHOULD|MAY)\b", block):
                bad("spec.md", f"{rid} lacks MUST/SHOULD/MAY")
            for kw in ("- Given", "- When", "- Then"):
                if kw not in block:
                    bad("spec.md", f"{rid} missing acceptance criterion '{kw}'")

    # --- plan task checks ---
    task_ids = []
    task_status = {}
    if "plan.md" in texts:
        seen = set()
        for t in parse_tasks(texts["plan.md"]):
            tid, f = t["id"], t["fields"]
            if tid in seen:
                bad("plan.md", f"duplicate {tid}")
            seen.add(tid)
            task_ids.append(tid)
            for fld in TASK_FIELDS:
                if fld not in f:
                    bad("plan.md", f"{tid} missing field '{fld}'")
            st = f.get("Status", "")
            if st and st not in ("todo", "done"):
                bad("plan.md", f"{tid} Status '{st}' not todo|done")
            task_status[tid] = st
            reqs = re.findall(r"REQ-\d+", f.get("Requirements", ""))
            if f.get("Requirements") is not None and not reqs:
                bad("plan.md", f"{tid} has no Requirements")
            for r in reqs:
                if req_ids and r not in req_ids:
                    bad("plan.md", f"{tid} references unknown {r}")
        for t in parse_tasks(texts["plan.md"]):
            for dep in re.findall(r"T-\d+", t["fields"].get("Depends on", "")):
                if dep not in task_ids:
                    bad("plan.md", f"{t['id']} depends on unknown {dep}")

        # --- traceability matrix ---
        matrix = parse_matrix(texts["plan.md"])
        for r in req_ids:
            if r not in matrix:
                bad("plan.md", f"{r} missing from traceability matrix")
        for r, ts in matrix.items():
            if r not in req_ids:
                bad("plan.md", f"matrix references unknown {r}")
            for tid in ts:
                if tid not in task_ids:
                    bad("plan.md", f"matrix references unknown {tid}")

    # --- status consistency ---
    status = pf.get("status", "")
    order = STATES.index(status) if status in STATES else -1
    def at_or_after(s):
        return status in STATES and order >= STATES.index(s)
    if at_or_after("Specified") and "spec.md" not in texts:
        bad("spec.md", f"status {status} requires spec.md")
    if at_or_after("Planned") and "plan.md" not in texts:
        bad("plan.md", f"status {status} requires plan.md")
    if at_or_after("Spec-Approved"):
        sf = fms.get("spec.md", {})
        if not sf.get("approved_by") or not sf.get("approved_on"):
            bad("spec.md", f"status {status} requires approved_by/approved_on")
    if status == "Closed":
        log = texts.get("log.md", "")
        m = re.search(r"^## DoD Sign-Off\s*$(.*?)(?=^## |\Z)", log, re.M | re.S)
        if not m or "Status: PASSED" not in m.group(1):
            bad("log.md", "Closed requires DoD Sign-Off with 'Status: PASSED'")

    # --- status history chain ---
    if "log.md" in texts:
        hist = sections(texts["log.md"]).get("Status History", "")
        prev_to = None
        for line in hist.splitlines():
            line = line.strip()
            if not line.startswith("- "):
                continue
            m = re.match(r"^- \d{4}-\d{2}-\d{2} (\S+) -> (\S+)", line)
            if not m:
                if re.match(r"^- \d{4}-\d{2}-\d{2} created as Draft", line):
                    continue
                if re.match(r"^- \d{4}-\d{2}-\d{2}", line):
                    bad("log.md", f"unparsable status history line: {line}")
                continue
            frm, to = m.group(1), m.group(2)
            if frm not in TRANSITIONS or to not in TRANSITIONS.get(frm, set()):
                bad("log.md", f"invalid transition in history: {frm} -> {to}")
            if prev_to is not None and frm != prev_to:
                bad("log.md", f"history gap: {prev_to} -> ... then {frm} -> {to}")
            prev_to = to

    # --- markdown links ---
    for name, text in texts.items():
        for m in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
            link = m.group(1).split()[0].strip("<>")
            if re.match(r"^(https?://|mailto:|#)", link):
                continue
            target = (cp_dir / link.split("#")[0]).resolve()
            if not target.exists():
                bad(name, f"broken link '{link}'")

    return problems


def lint_all(root: Path):
    problems = []
    pdir = root / "proposals"
    tmpl = pdir / "0000-template"
    if tmpl.is_dir():
        problems += lint_cp(tmpl, root, structural_only=True)
    if pdir.exists():
        for d in sorted(pdir.iterdir()):
            if d.is_dir() and re.match(r"^\d{4}-", d.name) and d.name != "0000-template":
                problems += lint_cp(d, root)
    return problems


def regenerate_index(root: Path):
    pdir = root / "proposals"
    readme = pdir / "README.md"
    rows = []
    if pdir.exists():
        for d in sorted(pdir.iterdir()):
            if d.is_dir() and re.match(r"^\d{4}-", d.name) and d.name != "0000-template":
                fm = parse_fm(d / "proposal.md") or {}
                rows.append(f"| {fm.get('id','?')} | {fm.get('title','?')} "
                            f"| {fm.get('status','?')} | {fm.get('author','?')} |")
    table = "\n".join(["| ID | Title | Status | Author |",
                       "|----|-------|--------|--------|"] + rows)
    text = readme.read_text() if readme.exists() else ""
    start, end = "<!-- cp-index:start -->", "<!-- cp-index:end -->"
    if start in text and end in text:
        pre = text[:text.index(start) + len(start)]
        post = text[text.index(end):]
        new = pre + "\n" + table + "\n" + post
    else:
        new = text.rstrip() + f"\n\n{start}\n{table}\n{end}\n"
    readme.write_text(new)


def append_history(log_path: Path, line: str):
    text = log_path.read_text() if log_path.exists() else "---\nid: \n---\n"
    if "## Status History" not in text:
        text = text.rstrip() + "\n\n## Status History\n"
    lines = text.splitlines()
    idx = next(i for i, l in enumerate(lines) if l.strip() == "## Status History")
    # drop placeholder bullets like '- <YYYY-MM-DD> ...'
    j = idx + 1
    while j < len(lines) and (lines[j].strip() == "" or lines[j].startswith("- <")):
        if lines[j].startswith("- <"):
            lines.pop(j)
        else:
            j += 1
    # insert after last existing history bullet
    k = idx + 1
    last = idx
    while k < len(lines) and not lines[k].startswith("## "):
        if lines[k].startswith("- "):
            last = k
        k += 1
    lines.insert(last + 1, line)
    log_path.write_text("\n".join(lines) + "\n")


def cmd_new(root, title, author):
    pdir, tmpl = root / "proposals", root / "proposals" / "0000-template"
    if not tmpl.is_dir():
        err("proposals/0000-template not found")
        return 1
    nums = [int(d.name[:4]) for d in pdir.iterdir()
            if d.is_dir() and re.match(r"^\d{4}-", d.name) and d.name != "0000-template"]
    n = (max(nums) + 1) if nums else 1
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    cp_dir = pdir / f"{n:04d}-{slug}"
    if cp_dir.exists():
        err(f"{cp_dir.name} already exists")
        return 1
    cp_dir.mkdir()
    cp_id = f"CP-{n:04d}"
    today = date.today().isoformat()
    author = author or git_author(root)

    prop = (tmpl / "proposal.md").read_text()
    cp_dir.joinpath("proposal.md").write_text(prop)
    set_fm(cp_dir / "proposal.md", {
        "id": cp_id, "title": title, "author": author,
        "status": "Draft", "created": today, "updated": today})
    text = (cp_dir / "proposal.md").read_text()
    text = text.replace("# CP-0000:", f"# {cp_id}:", 1)
    (cp_dir / "proposal.md").write_text(text)

    (cp_dir / "log.md").write_text((tmpl / "log.md").read_text())
    set_fm(cp_dir / "log.md", {"id": cp_id})
    log_text = (cp_dir / "log.md").read_text().replace("CP-0000", cp_id)
    (cp_dir / "log.md").write_text(log_text)
    append_history(cp_dir / "log.md", f"- {today} created as Draft by {author}")

    regenerate_index(root)
    print(f"Created {cp_dir}")
    return 0


def cmd_status(root, cp_id, state=None, by=None, superseded_by=None):
    cp_dir = find_cp(root, cp_id)
    if not cp_dir:
        err(f"CP {cp_id} not found")
        return 1
    prop = cp_dir / "proposal.md"
    fm = parse_fm(prop) or {}
    if state is None:
        print(fm.get("status", "unknown"))
        return 0
    if state not in STATES:
        err(f"unknown state '{state}'; valid: {', '.join(STATES)}")
        return 1
    cur = fm.get("status")
    if state not in TRANSITIONS.get(cur, set()):
        err(f"invalid transition {cur} -> {state}")
        return 1
    if state in NEEDS_BY and not by:
        err(f"transition {cur} -> {state} requires --by <name> "
            f"(gate {GATES.get(state, '')} / terminal state)")
        return 1
    # preconditions
    if state == "Specified" and not (cp_dir / "spec.md").exists():
        err("-> Specified requires spec.md (run `cp spec <id>` first)")
        return 1
    if state == "Spec-Approved":
        sf = parse_fm(cp_dir / "spec.md") or {}
        if not sf.get("approved_by") or not sf.get("approved_on"):
            err("G2 requires spec front matter approved_by and approved_on")
            return 1
        probs = lint_cp(cp_dir, root)
        if probs:
            for p in probs:
                err(p)
            err("G2 requires lint clean")
            return 1
    if state == "Planned" and not (cp_dir / "plan.md").exists():
        err("-> Planned requires plan.md (run `cp plan <id>` first)")
        return 1
    if state == "In-Progress":
        probs = lint_cp(cp_dir, root)
        if probs:
            for p in probs:
                err(p)
            err("G3 requires lint clean")
            return 1
    if state == "Implemented":
        plan_text = (cp_dir / "plan.md").read_text() if (cp_dir / "plan.md").exists() else ""
        tasks = parse_tasks(plan_text)
        if not tasks or any(t["fields"].get("Status") != "done" for t in tasks):
            err("-> Implemented requires every task Status: done")
            return 1
    if state == "Closed":
        log = (cp_dir / "log.md").read_text() if (cp_dir / "log.md").exists() else ""
        m = re.search(r"^## DoD Sign-Off\s*$(.*?)(?=^## |\Z)", log, re.M | re.S)
        if not m or "Status: PASSED" not in m.group(1):
            err("G4 requires log.md '## DoD Sign-Off' containing 'Status: PASSED'")
            return 1

    today = date.today().isoformat()
    set_fm(prop, {"status": state, "updated": today})
    if state == "Superseded" and superseded_by:
        set_fm(prop, {"superseded_by": superseded_by})
    if state == "Spec-Approved":
        set_fm(cp_dir / "spec.md", {"status": "Approved"})
    if state == "In-Progress":
        set_fm(cp_dir / "plan.md", {"status": "Approved"})
    gate = GATES.get(state)
    line = f"- {today} {cur} -> {state}"
    if by:
        line += f" by {by}"
    if gate:
        line += f" ({gate})"
    append_history(cp_dir / "log.md", line)
    regenerate_index(root)
    print(f"{fm.get('id')}: {cur} -> {state}")
    return 0


def cmd_scaffold(root, cp_id, kind):
    cp_dir = find_cp(root, cp_id)
    if not cp_dir:
        err(f"CP {cp_id} not found")
        return 1
    need = {"spec": "Accepted", "plan": "Spec-Approved"}[kind]
    fm = parse_fm(cp_dir / "proposal.md") or {}
    if fm.get("status") != need:
        err(f"cp {kind} requires status {need} (current: {fm.get('status')})")
        return 1
    target = cp_dir / f"{kind}.md"
    if target.exists():
        err(f"{kind}.md already exists")
        return 1
    tmpl = root / "proposals" / "0000-template" / f"{kind}.md"
    if not tmpl.exists():
        err(f"template {tmpl} not found")
        return 1
    target.write_text(tmpl.read_text())
    cid = fm.get("id", cp_id if cp_id.startswith("CP-") else f"CP-{int(cp_id):04d}")
    set_fm(target, {"id": cid, kind if kind != "spec" else "proposal": cid})
    text = target.read_text().replace("CP-0000", cid)
    target.write_text(text)
    print(f"Created {target}")
    return 0


def cmd_lint(root, cp_id=None):
    if cp_id:
        cp_dir = find_cp(root, cp_id)
        if not cp_dir:
            err(f"CP {cp_id} not found")
            return 1
        problems = lint_cp(cp_dir, root,
                           structural_only=(cp_dir.name == "0000-template"))
    else:
        problems = lint_all(root)
    for p in problems:
        print(p)
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


def cmd_next(root, cp_id):
    cp_dir = find_cp(root, cp_id)
    if not cp_dir:
        err(f"CP {cp_id} not found")
        return 1
    fm = parse_fm(cp_dir / "proposal.md") or {}
    if fm.get("status") != "In-Progress":
        err(f"warning: CP status is {fm.get('status')}, not In-Progress")
    plan = cp_dir / "plan.md"
    if not plan.exists():
        err("plan.md not found")
        return 1
    tasks = parse_tasks(plan.read_text())
    done = {t["id"] for t in tasks if t["fields"].get("Status") == "done"}
    for t in tasks:
        if t["fields"].get("Status") == "done":
            continue
        deps = set(re.findall(r"T-\d+", t["fields"].get("Depends on", "")))
        if deps <= done:
            print(f"{t['id']}: {t['title']}\n{t['block'].rstrip()}")
            return 0
    print("All tasks done")
    return 0


USAGE = """cp - Change Proposal CLI

  cp new "<title>" [--author NAME]
  cp status <id> [<state> [--by NAME] [--superseded-by CP-XXXX]]
  cp spec <id> | cp plan <id>
  cp lint [<id>]
  cp index
  cp next <id>
"""


def main(argv=None, root=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(root) if root else Path(__file__).resolve().parents[2]
    if not argv:
        print(USAGE)
        return 1
    cmd, rest = argv[0], argv[1:]

    def opt(name):
        return rest[rest.index(name) + 1] if name in rest else None

    if cmd == "new":
        if not rest:
            err("usage: cp new \"<title>\" [--author NAME]")
            return 1
        return cmd_new(root, rest[0], opt("--author"))
    if cmd == "status":
        pos = [a for a in rest if not a.startswith("--")
               and (rest.index(a) == 0 or rest[rest.index(a) - 1] not in
                    ("--by", "--superseded-by"))]
        if not pos:
            err("usage: cp status <id> [<state>] [--by NAME]")
            return 1
        return cmd_status(root, pos[0], pos[1] if len(pos) > 1 else None,
                          opt("--by"), opt("--superseded-by"))
    if cmd in ("spec", "plan"):
        if not rest:
            err(f"usage: cp {cmd} <id>")
            return 1
        return cmd_scaffold(root, rest[0], cmd)
    if cmd == "lint":
        return cmd_lint(root, rest[0] if rest else None)
    if cmd == "index":
        regenerate_index(root)
        print("Index regenerated")
        return 0
    if cmd == "next":
        if not rest:
            err("usage: cp next <id>")
            return 1
        return cmd_next(root, rest[0])
    err(f"unknown command '{cmd}'")
    print(USAGE)
    return 1


if __name__ == "__main__":
    sys.exit(main())
