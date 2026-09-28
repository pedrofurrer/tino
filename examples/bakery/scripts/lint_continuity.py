#!/usr/bin/env python3
"""Continuity verifier — size budgets and integrity of the living documents.

Template from the `continuity` skill of tino (v2.0). The installer copies it
into the project (e.g. `scripts/lint_continuity.py`) and writes the
machine-readable budgets line into PLAN.md (alarm/cap in lines and alarm/cap
in KB, KB = 1000 bytes; segments separated by «|», all optional):

  <!-- lint-budgets: PLAN 120/150 14.4/18 | ARCHITECTURE 160/200 24/30 | LOGBOOK 160/200 20/25 | INSTRUCTIONS 200/300 12/20 | BLOCK 20 -->

  · `<DOC> al/tl ak/tk` — alarm and cap in lines and in KB (alarm = 80 % of the cap).
  · `INSTRUCTIONS` — the agent's whole instructions file (CLAUDE.md,
    AGENTS.md…; detected automatically, or fixed with `INSTRUCTIONS=<file>`).
    Warning only: it is paid in every session and its diet is the user's call.
  · `BLOCK n` — line cap of the continuity block; `BLOCK <component> n` for
    the blocks of the other tino components (default 15). A block is counted
    from its heading (`## `) to its version marker, both included, and is
    located BY THE MARKER, so it works in any language. Whatever follows the
    marker (the lesson index, a rituals section) does not count.
  · `DOCS PLAN` (minimal scale) or `DOCS PLAN,LOGBOOK` — which documents
    exist and are checked; without it, all three.
Without a budgets line, the same defaults apply.

Usage, from the project root (or with --root):
  python3 scripts/lint_continuity.py            → verify; exit 1 on EXCESS or failure
  python3 scripts/lint_continuity.py --margin   → bytes and lines still available in each
                                                   document: measure BEFORE writing; if it
                                                   does not fit, rotate or compact FIRST.
  python3 scripts/lint_continuity.py --resume   → print the "where we left off" and 🔄 lines
                                                   of PLAN.md (for the optional session-start
                                                   hook in Claude Code); never fails.

Checks: 1) budgets per document → OK / ALARM (warns) / EXCESS (fails);
2) the whole instructions file and each tino block (warnings only);
3) version marker of the continuity block (the legacy "Sistema: … vX.Y"
warns: the upgrade replaces the block's text and marker); 4) "at the edge":
a document in ALARM with less than 3 % of its cap free, in bytes or in lines
⇒ ESCALATE (propose to the user an index-style split or a recalibration,
never on your own); 5) if ARCHITECTURE has a numbered "## INVARIANTS"
section, its numbering increases without repeats (a gap warns; disorder
fails: never renumber); 6) invisible characters (bidi controls, Unicode
tags, zero-width spaces) warn — that is how instructions get hidden.
Read-only; standard library only.

Fixed tokens: the document names, the INVARIANTS heading, the budgets keys
and the version marker are read by this script and stay fixed in every
language. They exist in two sets — English, and the Spanish set that 1.x
projects use and that the installer writes for Spanish-language projects —
and both are accepted, in any mix (docs/format.md lists them).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ── Fixed tokens and defaults ───────────────────────────────────────────────
# canonical key: (file names in order of preference, (alarm lines, cap lines, alarm KB, cap KB))
DOCS = {
    "PLAN": (("PLAN.md",), (120, 150, 14.4, 18.0)),
    "ARCHITECTURE": (("ARCHITECTURE.md", "ARQUITECTURA.md"), (160, 200, 24.0, 30.0)),
    "LOGBOOK": (("LOGBOOK.md", "BITACORA.md"), (160, 200, 20.0, 25.0)),
    "INSTRUCTIONS": ((), (200, 300, 12.0, 20.0)),
}
DOC_ALIASES = {"ARQUITECTURA": "ARCHITECTURE", "BITACORA": "LOGBOOK", "INSTRUCCIONES": "INSTRUCTIONS"}
BLOCK_CAPS = {"continuity": 20, "metacognition": 15, "brain": 15}
COMPONENT_ALIASES = {"continuidad": "continuity", "metacognicion": "metacognition", "cerebro": "brain"}
INSTRUCTION_FILES = ("CLAUDE.md", "AGENTS.md", "GEMINI.md", ".cursorrules")
INVARIANTS_HEADING = r"(?:INVARIANTS|INVARIANTES)"
RESUME_PHRASES = ("where we left off", "quedamos en")  # how PLAN.md marks the exact point of a task in progress
LEGEND_MARKER = "<!-- tino:legend -->"
LEGEND_TEXTS = (("✅ done", "🔄 in progress"), ("✅ hecho", "🔄 en curso"))  # the states legend is not a task
RE_MARKER = re.compile(r"<!--\s*(?:tino|suite-agentica):\s*([a-z]+)\s+v(\d+)\.(\d+)\s*-->")
RE_LEGACY = re.compile(r"Sistema:\s*(continuidad|metacognicion|cerebro)\s+v(\d+)\.(\d+)")
RE_LEGACY_TITLE = re.compile(r"^#{2,3} .*(?:continuity|continuidad)", re.M | re.I)
RE_BUDGETS = re.compile(r"<!--\s*lint-(?:budgets|topes):\s*(.+?)\s*-->")
MARGIN_FLAGS = ("--margin", "--margen")  # a current continuity block mentions one of them
AT_EDGE = 0.03  # fraction of the cap
INVISIBLE = re.compile("[" + "".join(chr(a) + ("-" + chr(b) if b != a else "") for a, b in (
    (0x200B, 0x200C), (0x200E, 0x200F), (0x202A, 0x202E), (0x2060, 0x2064), (0x2066, 0x2069),
    (0xFEFF, 0xFEFF), (0xE0000, 0xE007F))) + "]")  # bidi, Unicode tags, zero width (no invisible literals here)
BOM = chr(0xFEFF)
# ─────────────────────────────────────────────────────────────────────────────

failures: list = []
alarms: list = []
ROOT = Path.cwd()


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        print(f"  ✗ {path.name} is not UTF-8 (byte {e.start}): convert it; the verifier cannot continue.")
        sys.exit(1)


def invisible(name: str, text: str) -> None:
    found = [(text.count("\n", 0, m.start()) + 1, f"U+{ord(m.group(0)):04X}")
             for m in INVISIBLE.finditer(text) if not (m.start() == 0 and m.group(0) == BOM)]
    if found:
        sample = ", ".join(f"line {ln} {cp}" for ln, cp in found[:3])
        alarms.append(f"{name}: {len(found)} invisible character(s) ({sample}) — review: this is how instructions get hidden")


def canon(doc: str) -> str:
    return DOC_ALIASES.get(doc, doc)


def parse_budgets():
    budgets = {k: v[1] for k, v in DOCS.items()}
    blocks = dict(BLOCK_CAPS)
    instructions = None
    plan = ROOT / "PLAN.md"
    if not plan.exists():
        print(f"  ✗ PLAN.md not found in {ROOT}: run the verifier from the project root (or with --root).")
        sys.exit(1)
    m = RE_BUDGETS.search(read(plan))
    if not m:
        alarms.append("PLAN.md has no «<!-- lint-budgets: … -->» line: using the default budgets")
        return budgets, blocks, instructions
    for seg in m.group(1).split("|"):
        seg = seg.strip()
        if not seg or re.match(r"\S+-(?:partition|particion)\s+\S+$", seg):
            continue  # segments that belong to other variants of the lint: ignored
        mdocs = re.match(r"DOCS\s+([\w,]+)$", seg)
        mb = re.match(r"(?:BLOCK|BLOQUE)\s+(\d+)$", seg)
        mbp = re.match(r"(?:BLOCK|BLOQUE)\s+([a-z]+)\s+(\d+)$", seg)
        mi = re.match(r"(?:INSTRUCTIONS|INSTRUCCIONES)=(\S+)$", seg)
        md = re.match(r"(\S+)\s+(\d+)/(\d+)\s+(\d+(?:[.,]\d+)?)/(\d+(?:[.,]\d+)?)$", seg)
        if mdocs:
            chosen = {canon(d.strip()) for d in mdocs.group(1).split(",") if d.strip()} | {"INSTRUCTIONS"}
            budgets = {k: v for k, v in budgets.items() if k in chosen}
        elif mb:
            blocks["continuity"] = int(mb.group(1))
        elif mbp:
            blocks[COMPONENT_ALIASES.get(mbp.group(1), mbp.group(1))] = int(mbp.group(2))
        elif mi:
            instructions = mi.group(1)
        elif md:
            doc, al, tl, ak, tk = md.groups()
            budgets[canon(doc)] = (int(al), int(tl), float(ak.replace(",", ".")), float(tk.replace(",", ".")))
        else:
            alarms.append(f"unreadable segment in lint-budgets: {seg!r} (format in this script's header)")
    return budgets, blocks, instructions


def instructions_file(fixed):
    if fixed:
        return ROOT / fixed
    for c in INSTRUCTION_FILES:
        if (ROOT / c).exists():
            return ROOT / c
    return None


def names_of(doc: str):
    return DOCS[doc][0] if doc in DOCS else (f"{doc}.md",)


def doc_path(doc: str, instructions):
    if doc == "INSTRUCTIONS":
        return instructions_file(instructions)
    names = names_of(doc)
    for n in names:
        if (ROOT / n).exists():
            return ROOT / n
    return ROOT / names[0]


def measure(path: Path):
    text = read(path)
    return text.count("\n") + (0 if text.endswith("\n") or not text else 1), path.stat().st_size, text


def check_budgets(budgets, instructions) -> bool:
    excess = False
    for doc, (al, tl, ak, tk) in budgets.items():
        path = doc_path(doc, instructions)
        if not path or not path.exists():
            if doc != "INSTRUCTIONS":
                names = names_of(doc)
                alt = f" (nor {', '.join(names[1:])})" if len(names) > 1 else ""
                alarms.append(f"{names[0]} does not exist{alt} (on a minimal scale, declare it with the «DOCS PLAN» segment)")
            continue
        lines, size, text = measure(path)
        invisible(path.name, text)
        cap_b, alarm_b = int(tk * 1000), int(ak * 1000)
        if lines > tl or size > cap_b:
            status = "EXCESS"
        elif lines > al or size > alarm_b:
            status = "ALARM "
        else:
            status = "OK    "
        note = ""
        if doc == "INSTRUCTIONS":
            if status == "EXCESS":
                status, note = "ALARM ", " (warning only: paid in every session; its diet is the user's call)"
        elif status == "EXCESS":
            excess = True
        if status == "ALARM " and doc != "INSTRUCTIONS" and (
                (cap_b - size) < AT_EDGE * cap_b or (tl - lines) < AT_EDGE * tl):
            note += " · ESCALATE: at the edge of the cap → PROPOSE to the user an index-style split or a recalibration"
        print(f"  {status}  {path.name}: {lines} lines (alarm {al} / cap {tl}) · "
              f"{size/1000:.1f} KB (alarm {ak} / cap {tk}){note}")
        if status == "ALARM ":
            alarms.append(f"{path.name} in ALARM{note}")
    return excess


def check_blocks(instructions, block_caps) -> None:
    path = instructions_file(instructions)
    if not path or not path.exists():
        alarms.append("agent instructions file not found (CLAUDE.md / AGENTS.md…)")
        return
    text = read(path)

    def report(component: str, block: str, label: str) -> None:
        n = block.count("\n") + 1
        cap = block_caps.get(component, 15)
        print(f"  {'OK    ' if n <= cap else 'ALARM '}  {component} block{label} in {path.name}: "
              f"{n} lines (cap {cap})")
        if n > cap:
            alarms.append(f"{component} block: {n} lines > {cap} (paid in every session)")

    with_marker = set()
    measured = {}  # heading position → component whose block was measured from it
    for mk in RE_MARKER.finditer(text):
        component = COMPONENT_ALIASES.get(mk.group(1), mk.group(1))
        version = (int(mk.group(2)), int(mk.group(3)))
        label = f" v{version[0]}.{version[1]}"
        headings = ([h.start() for h in re.finditer(r"^## ", text[: mk.start()], re.M)]
                    or [h.start() for h in re.finditer(r"^#{1,6} ", text[: mk.start()], re.M)])
        if not headings:
            alarms.append(f"{path.name}: the {component} marker has no block heading above it")
            continue
        with_marker.add(component)
        if headings[-1] in measured:  # a block that lives inside another one's heading is measured with it
            print(f"  OK      {component} block{label} in {path.name}: shares its heading with the "
                  f"{measured[headings[-1]]} block (measured with it)")
            continue
        measured[headings[-1]] = component
        block = text[headings[-1]: mk.end()]
        report(component, block, label)
        if component == "continuity" and version >= (1, 4) and not any(f in block for f in MARGIN_FLAGS):
            alarms.append(f"{path.name}: the marker says v{version[0]}.{version[1]} but the continuity block's text is "
                          f"older (it does not mention «--margin»): replace the TEXT with the current template's")
        if version < (2, 0):
            print(f"  INFO    {component} block{label} is a 1.x block: the tino installer can upgrade it")
    legacies = {}
    for lg in RE_LEGACY.finditer(text):
        component = COMPONENT_ALIASES[lg.group(1)]
        if component not in with_marker and component not in legacies:
            legacies[component] = lg.group(0).strip()
            alarms.append(f"{path.name}: LEGACY marker «{lg.group(0).strip()}» — the upgrade replaces the block's "
                          f"TEXT and adds the HTML marker")
    if "continuity" in with_marker:
        print("  OK      continuity version marker present")
        return
    m = RE_LEGACY_TITLE.search(text)  # project older than 1.4: located by its heading
    if not m:
        alarms.append(f"{path.name}: continuity block not found (neither its marker nor its heading)")
        return
    rest = text[m.end():]
    end = re.search(r"^## ", rest, re.M)
    report("continuity", text[m.start(): m.end() + (end.start() if end else len(rest))].rstrip("\n"), " (no HTML marker)")
    if "continuity" not in legacies:
        alarms.append(f"{path.name}: continuity block without a version marker «<!-- tino: continuity vX.Y -->» "
                      f"(the installer will not be able to detect its version)")


def check_invariants() -> None:
    arch = doc_path("ARCHITECTURE", None)
    if not arch.exists():
        return
    m = re.search(r"^## " + INVARIANTS_HEADING + r".*?(?=^## |\Z)", read(arch), re.M | re.S | re.I)
    if not m:
        return
    numbers = [int(n) for n in re.findall(r"^(\d+)\.\s", m.group(0), re.M)]
    if not numbers:
        return
    if numbers != sorted(numbers) or len(numbers) != len(set(numbers)):
        failures.append(f"INVARIANTS: numbering out of order or repeated {numbers} (never renumber)")
        return
    gaps = sorted(set(range(1, max(numbers) + 1)) - set(numbers))
    if gaps:
        alarms.append(f"INVARIANTS: numbers {gaps} are missing (was an invariant deleted? leave a tombstone)")
        return
    print(f"  OK      INVARIANTS: {len(numbers)} numbered, increasing, no repeats or gaps")


def margin(budgets, instructions) -> None:
    print("── writing margin (measure BEFORE writing) ──")
    for doc, (al, tl, ak, tk) in budgets.items():
        path = doc_path(doc, instructions)
        if not path or not path.exists():
            continue
        lines, size, _ = measure(path)
        free = int(tk * 1000) - size
        status = f"{free} B fit" if free >= 0 else f"EXCESS: {-free} B over"
        print(f"  {path.name}: {size} B → {status} (cap {int(tk*1000)} B) · {lines}/{tl} lines → {tl - lines} fit")


def is_legend(line: str) -> bool:
    if LEGEND_MARKER in line:
        return True
    low = line.lower()
    return any(all(t in low for t in pair) for pair in LEGEND_TEXTS)


def resume() -> None:
    plan = ROOT / "PLAN.md"
    try:
        lines = plan.read_text(encoding="utf-8").splitlines() if plan.exists() else []
    except UnicodeDecodeError:
        lines = []
    live, i = [], 0
    while i < len(lines) and len(live) < 40:
        line = lines[i]
        if (not line.lstrip().startswith(">") and not is_legend(line)
                and (any(p in line.lower() for p in RESUME_PHRASES) or "🔄" in line)):
            indent = len(line) - len(line.lstrip())
            live.append(line.rstrip())
            i += 1
            while i < len(lines) and lines[i].strip() and len(lines[i]) - len(lines[i].lstrip()) > indent:
                live.append(lines[i].rstrip())  # continuation of the item: the "next step" usually lives here
                i += 1
            continue
        i += 1
    if live:
        print("── PLAN.md: where we left off (re-shown by the continuity check on resume or after compaction) ──")
        for line in live:
            print(f"  {line}")


def main() -> None:
    global ROOT
    ap = argparse.ArgumentParser(description="Budgets and integrity verifier for the living documents.")
    ap.add_argument("--margin", "--margen", dest="margin", action="store_true",
                    help="only print how much still fits in each document")
    ap.add_argument("--root", "--raiz", dest="root", default=".", help="project root (default: current directory)")
    ap.add_argument("--resume", "--retomar", dest="resume", action="store_true",
                    help="only print the «where we left off» and 🔄 lines of PLAN.md")
    a = ap.parse_args()
    ROOT = Path(a.root).resolve()
    if a.resume:
        resume()
        return
    budgets, block_caps, instructions = parse_budgets()
    if a.margin:
        margin(budgets, instructions)
        return
    print("── lint_continuity ──")
    excess = check_budgets(budgets, instructions)
    check_blocks(instructions, block_caps)
    check_invariants()
    for x in alarms:
        print(f"  ⚠ {x}")
    for f in failures:
        print(f"  ✗ {f}")
    if excess or failures:
        print("RESULT: ❌ EXCESS or failure — archive or repair BEFORE the closing commit.")
        sys.exit(1)
    if alarms:
        print("RESULT: ⚠️  ALARM — review the warnings above; if they are about size, compact in this session (does not block).")
        sys.exit(0)
    print("RESULT: ✅ everything within budget.")


if __name__ == "__main__":
    main()
