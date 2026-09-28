#!/usr/bin/env python3
"""Regression bench for tino — standard library only.

Three layers:
  static  Coherent version in every piece (plugin.json, SKILL, PROTOCOL,
          CHANGELOG, scripts); name and description of every skill (Agent
          Skills spec and ≤200 characters for claude.ai); block caps counted
          from the heading to the marker; no invisible characters; Python 3.8
          syntax; declared placeholders; executable bit; the index formats
          written in the SCHEMA template; manifests consistent; no local paths
          or generation trailers anywhere.
  smoke   A test project is seeded following the SKILL.md texts (budgets line,
          seeded names, SCHEMA formats), in English and with the Spanish token
          set, and the three verifiers must come out green.
  edges   Edge cases of the scripts (the 1.x audits, the 1.5 end-to-end test,
          the four template defects fixed in 2.0) and compatibility with 1.x
          Spanish projects.

Usage: python3 tests/test_suite.py [-v] [--only static,smoke,edges]
Writes only inside a temporary directory.
"""
from __future__ import annotations

import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PLUGIN = REPO / "plugins" / "tino"
SKILLS = PLUGIN / "skills"
COMPONENTS = ("continuity", "metacognition", "brain")
BLOCK_CAPS = {"continuity": 20, "metacognition": 15, "brain": 15}
FM_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
INVISIBLE = [(0x200B, 0x200F), (0x202A, 0x202E), (0x2060, 0x2064), (0x2066, 0x2069), (0xFEFF, 0xFEFF),
             (0xE0000, 0xE007F)]
# built from pieces so that this file does not match itself
TRACE = re.compile("(?i)(" + "co-" + "authored-by:|generated with \\[?claude|noreply@" + "anthropic\\.com|/" + "Users/)")
PY = sys.executable
VERBOSE = "-v" in sys.argv
results: list = []

S_CONT = SKILLS / "continuity" / "templates" / "lint_continuity.py"
S_ROT = SKILLS / "continuity" / "templates" / "rotate_logbook.py"
S_LES = SKILLS / "metacognition" / "templates" / "lint_lessons.py"
S_IDX = SKILLS / "brain" / "templates" / "lint_index.py"
SCRIPTS = (S_CONT, S_ROT, S_LES, S_IDX)


def case(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, bool(ok), detail))


def run(script: Path, args, cwd: Path, stdin: str = None, env: dict = None):
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    if env:
        e.update(env)
    r = subprocess.run([PY, "-B", str(script)] + list(args), cwd=str(cwd), input=stdin, env=e,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding="utf-8")
    return r.returncode, r.stdout


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write(p: Path, text: str, encoding: str = "utf-8") -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode(encoding, errors="replace"))  # in Latin-1, «ñ» becomes a byte invalid in UTF-8
    return p


def without_comment(text: str) -> str:
    """Drop a template's leading HTML comment, as the installer does."""
    m = re.match(r"\s*<!--.*?-->\s*\n", text, re.S)
    return text[m.end():] if m else text


def frontmatter(text: str) -> dict:
    parts = text.split("---", 2)
    fm, parent = {}, None
    for line in parts[1].splitlines():
        m = re.match(r"^(\s*)([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            continue
        v = m.group(3).strip().strip('"')
        if not m.group(1):
            parent = m.group(2) if not v else None
            fm[m.group(2)] = v if v else {}
        elif parent:
            fm[parent][m.group(2)] = v
    return fm


def is_invisible(c: str) -> bool:
    o = ord(c)
    return any(a <= o <= b for a, b in INVISIBLE)


def block_lines(text: str) -> int:
    lines = text.split("\n")
    start = next(i for i, line in enumerate(lines) if line.startswith("## "))
    end = next(i for i, line in enumerate(lines) if "<!-- tino:" in line)
    return end - start + 1


# ─────────────────────────── static ───────────────────────────
def static() -> None:
    manifest = json.loads(read(PLUGIN / ".claude-plugin" / "plugin.json"))
    market = json.loads(read(REPO / ".claude-plugin" / "marketplace.json"))
    version = manifest.get("version", "")
    short = ".".join(version.split(".")[:2])
    entry = next((p for p in market.get("plugins", []) if p.get("name") == manifest.get("name")), None)
    case("S0 marketplace lists the plugin with the same name and a source inside the repo",
         entry is not None and (REPO / entry.get("source", "")).resolve() == PLUGIN.resolve(), str(entry))
    case("S0 plugin folder carries README.md (40+ words) and LICENSE (directory requirement)",
         (PLUGIN / "LICENSE").exists() and (PLUGIN / "README.md").exists()
         and len(re.sub(r"```.*?```", "", read(PLUGIN / "README.md"), flags=re.S).split()) >= 40)
    for c in COMPONENTS:
        d = SKILLS / c
        skill = read(d / "SKILL.md")
        fm = frontmatter(skill)
        versions = {"plugin.json": short, "SKILL": fm.get("metadata", {}).get("version"),
                    "PROTOCOL": (re.search(r"^> v(\d+\.\d+) \(", read(d / "PROTOCOL.md"), re.M) or [None, None])[1],
                    "CHANGELOG": (re.search(r"^## v(\d+\.\d+)", read(d / "CHANGELOG.md"), re.M) or [None, None])[1]}
        for s in (d / "templates").glob("*.py"):
            m = re.search(r"\(v(\d+\.\d+)\)", read(s))
            versions[s.name] = m.group(1) if m else None
        case(f"S1 {c}: coherent version in every piece", len(set(versions.values())) == 1, str(versions))
        case(f"S2 {c}: admitted frontmatter keys", set(fm) <= FM_KEYS, str(sorted(fm)))
        case(f"S2 {c}: valid name equal to its folder",
             fm.get("name") == c and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm.get("name", "")) is not None)
        n = len(fm.get("description", ""))
        case(f"S2 {c}: description ≤200 characters (claude.ai) and without «<»/«>»",
             0 < n <= 200 and not re.search(r"[<>]", fm.get("description", "")), f"{n} chars")
        case(f"S2 {c}: SKILL.md under 500 lines", skill.count("\n") < 500)
        for rit in sorted((d / "templates").glob("*-SKILL.md")):
            fr = frontmatter(read(rit))
            nr = len(fr.get("description", ""))
            case(f"S2 {c}/{rit.name}: ritual with a valid name and a description ≤200 characters",
                 re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fr.get("name", "")) is not None and 0 < nr <= 200
                 and not re.search(r"[<>]", fr.get("description", "")), f"{nr} chars")
        bl = without_comment(read(d / "templates" / "instructions-block.md"))
        nb = block_lines(bl)
        case(f"S3 {c}: block ≤{BLOCK_CAPS[c]} lines from heading to marker", nb <= BLOCK_CAPS[c], f"{nb} lines")
        case(f"S3 {c}: the block carries the invariant HTML marker", f"<!-- tino: {c} v<VERSION> -->" in bl)
        for f in sorted(d.rglob("*")):
            if f.is_file() and f.suffix in (".md", ".py") and "templates" in f.parts:
                t = read(f)
                m = re.match(r"(?:---.*?---\s*)?\s*<!--(.*?)-->", t, re.S)
                if m:
                    used = set(re.findall(r"<([A-Z][A-Z_+]*)>", t[m.end():]))
                    missing = sorted(u for u in used if f"<{u}" not in m.group(1))
                    case(f"S6 {f.relative_to(SKILLS)}: placeholders declared", not missing, str(missing))
    bad_inv, bad_trace = [], []
    for f in sorted(REPO.rglob("*")):
        if ".git" in f.parts or not f.is_file() or f.suffix not in (".md", ".py", ".sh", ".txt", ".json", ".yml", ".yaml", ".cff"):
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        if any(is_invisible(c) for c in t):
            bad_inv.append(str(f.relative_to(REPO)))
        if TRACE.search(t):
            bad_trace.append(str(f.relative_to(REPO)))
    case("S4 no file with invisible characters (bidi, tags, zero width)", not bad_inv, str(bad_inv))
    case("S4 no file with local home paths or generation trailers", not bad_trace, str(bad_trace))
    for s in SCRIPTS:
        try:
            ast.parse(read(s), feature_version=(3, 8))
            ok = True
        except SyntaxError:
            ok = False
        case(f"S5 {s.name}: syntax compatible with Python 3.8", ok)
        case(f"S7 {s.name}: executable bit set", os.access(str(s), os.X_OK))
    schema = read(SKILLS / "brain" / "templates" / "schema-template.md")
    for literal in ("> Entries: N.", "END OF SUB-INDEX · ", " — N entries", "END OF INDEX (front page) — N sub-indexes",
                    "[[folder/slug]]", "## [YYYY-MM-DD] operation | Title"):
        case(f"S8 SCHEMA documents the format the verifier reads: {literal!r}", literal in schema)
    case("S8 the continuity installer writes the complete lint-budgets line",
         "<!-- lint-budgets: PLAN " in read(SKILLS / "continuity" / "SKILL.md"))
    inlined = re.compile(r"section of (?:the|these|the project's) instructions")
    for c in COMPONENTS:
        skill = read(SKILLS / c / "SKILL.md")
        case(f"S9 {c}: a ritual that cannot be a skill goes to rituals/, never into the instructions",
             "`rituals/<name>.md`" in skill and "`rituales/`" in skill and not inlined.search(skill)
             and "never a second copy" in skill)
    stale = sorted(f.name for c in COMPONENTS for f in (SKILLS / c / "templates").glob("*.md") if inlined.search(read(f)))
    case("S9 no template sends a ritual into the instructions", not stale, str(stale))
    ingest = read(SKILLS / "brain" / "templates" / "ingest-source-SKILL.md")
    case("S10 ingest moves only what is in the inbox and copies everything else",
         "COPIED from anywhere else" in ingest and "never moved or emptied" in ingest
         and not re.search(r"its raw file moves to", ingest))
    stale_ex = []
    for ex in sorted((REPO / "examples").iterdir()) if (REPO / "examples").is_dir() else []:
        for s in SCRIPTS:
            installed = ex / "scripts" / s.name
            if installed.exists() and installed.read_bytes() != s.read_bytes():
                stale_ex.append(f"{ex.name}/scripts/{s.name}")
    case("S11 the examples carry the current scripts byte for byte (regenerate them after a template change)",
         not stale_ex, str(stale_ex))
    body = without_comment(read(SKILLS / "brain" / "templates" / "schema-template.md"))
    plain = re.sub(r"\{\{IF LANDSCAPE\}\}.*?\{\{END IF LANDSCAPE\}\}", "", body, flags=re.S)
    plain = re.sub(r"\{\{IF LANDSCAPE:[^}]*\}\}", "", plain)
    case("S12 the SCHEMA mentions the landscape layer only inside its conditional markers",
         "landscape" not in plain.lower() and "{{" not in plain and "LANDSCAPE_IF_APPLICABLE" not in body
         and body.count("{{IF LANDSCAPE}}") == body.count("{{END IF LANDSCAPE}}") > 0)
    memory_use = re.compile(r"(automatic|agent'?s?|project|persistent|own) memory|MEMORY\.md|session transcripts|chat history|past conversations", re.I)
    offending = []
    for f in sorted(SKILLS.rglob("*")):
        if f.is_file() and f.suffix in (".md", ".py") and f.name != "CHANGELOG.md":
            lines = read(f).splitlines()
            for n, line in enumerate(lines, 1):
                context = line + " " + (lines[n] if n < len(lines) else "")
                if memory_use.search(line) and not re.search(r"\b(not|never|no longer)\b", context):
                    offending.append(f"{f.relative_to(SKILLS)}:{n}")
    case("S13 the skills never read the agent's memory or past conversations (directory policy 1.F)",
         not offending, str(offending[:8]))
    rituals = {n: read(SKILLS / c / "templates" / f"{n}-SKILL.md")
               for c, n in (("brain", "ingest-source"), ("brain", "harvest"), ("brain", "lint-brain"),
                            ("continuity", "save-progress"))}
    case("S14 the writing rituals check figures, quotations and certainty piece by piece",
         "recomputed from its source" in rituals["ingest-source"] and "verbatim" in rituals["ingest-source"]
         and "a match is not an" in rituals["ingest-source"] and "piece-by-piece check" in rituals["harvest"]
         and "certainty grew" in rituals["lint-brain"] and "not from memory" in rituals["save-progress"]
         and "went stale" in rituals["save-progress"] and "never the wiki's queue" in rituals["ingest-source"]
         and "known on its date" in read(SKILLS / "continuity" / "SKILL.md"))
    fmt = read(REPO / "docs" / "format.md")
    case("S9 format.md documents the rituals/ fallback in both sets",
         "`rituals/<name>.md`" in fmt and "`rituales/<name>.md`" in fmt)


# ─────────────────────────── smoke ───────────────────────────
def budgets_line() -> str:
    return re.search(r"`(<!-- lint-budgets: .*? -->)`", read(SKILLS / "continuity" / "SKILL.md")).group(1)


def resolved_block(component: str, replacements: dict) -> str:
    t = without_comment(read(SKILLS / component / "templates" / "instructions-block.md"))
    for k, v in replacements.items():
        t = t.replace(k, v)
    return t


def seed_continuity(root: Path, minimal: bool = False) -> None:
    budgets = budgets_line()
    if minimal:
        budgets = budgets.replace(" -->", " | DOCS PLAN -->")
    write(root / "PLAN.md", f"# PLAN\n\n{budgets}\n\n## F1 🔄 Draft\n- where we left off: chapter 2, section 3\n")
    if not minimal:
        write(root / "LOGBOOK.md", "# LOGBOOK\n\n> append-only.\n\n## 2026-09-01 — earlier decision\nWhat and why.\n\n"
                                   "## 2026-09-26 — continuity installed\nStandard scale.\n")
        write(root / "ARCHITECTURE.md", "# ARCHITECTURE\n\n## INVARIANTS\n\n1. One.\n2. Two.\n3. Three.\n")
    block = resolved_block("continuity", {"<RITUAL>": "skill `save-progress`", "<VERSION>": "2.0",
                                          "<VERIFIER>": "python3 scripts/lint_continuity.py",
                                          "<ROTATOR>": "python3 scripts/rotate_logbook.py"})
    write(root / "CLAUDE.md", "# Test project\n\n" + block)


def smoke(tmp: Path) -> None:
    p = tmp / "smoke-standard"
    seed_continuity(p)
    code, out = run(S_CONT, [], p)
    case("B1 standard continuity seeded per SKILL.md → green", code == 0 and "✅" in out, out)
    code, out = run(S_CONT, ["--resume"], p)
    case("B1 --resume prints the PLAN's «where we left off»", "where we left off: chapter 2" in out, out)
    p = tmp / "smoke-minimal"
    seed_continuity(p, minimal=True)
    code, out = run(S_CONT, [], p)
    case("B2 minimal-scale continuity (DOCS PLAN) → green", code == 0 and "✅" in out, out)

    p = tmp / "smoke-meta"
    seed_continuity(p)
    lessons = p / "lessons"
    lessons.mkdir(parents=True, exist_ok=True)
    for name in ("lesson-example-gatekeeper.md", "TEMPLATE-lesson.md"):  # the seeding names of the SKILL.md
        shutil.copy(str(SKILLS / "metacognition" / "templates" / name), str(lessons / name))
    meta = resolved_block("metacognition", {"<PATH>": "lessons/", "<INDEX>": "below, down to its END line",
                                            "<CADENCE>": "weekly", "<RITUAL>": "skill `introspect`", "<VERSION>": "2.0"})
    with open(p / "CLAUDE.md", "a", encoding="utf-8") as f:
        f.write("\n" + meta)
    code, out = run(S_LES, ["--dir", "lessons", "--index", "CLAUDE.md"], p)
    case("B3 metacognition seeded per SKILL.md (index in CLAUDE.md) → green", code == 0 and "✓ green" in out, out)
    write(lessons / "lesson-figure-from-press.md",
          "---\nname: lesson-figure-from-press\ndescription: \"figure from a press release → check it against own data #1\"\n"
          "metadata:\n  type: lesson\n  validation: hypothesis\n  scope: test\n  evidence: user\n---\n"
          "**Trigger**: x\n**Original error**: y\n**Principle**: z\n**Application**: w\n"
          "**Cases**:\n- 2026-09-26 · origin — the editor corrected the figure\n")
    t = read(p / "CLAUDE.md").replace("END OF LESSON INDEX — 0 entries",
                                      "- lesson-figure-from-press — figure from a press release → check it against own data\n"
                                      "END OF LESSON INDEX — 1 entries")
    write(p / "CLAUDE.md", t)
    code, out = run(S_LES, ["--dir", "lessons", "--index", "CLAUDE.md"], p)
    case("B3 first lesson + index → green, no evidence warnings", code == 0 and "✓ green" in out
         and "without a declared `evidence`" not in out, out)
    code, out = run(S_CONT, [], p)
    case("B3 with two blocks, continuity stays green and measures both", code == 0 and "metacognition block" in out, out)
    code, out = run(S_LES, ["--dir", "lessons", "--summary"], p)
    case("B3 --summary shows evidence and applied", "user" in out and "applied=0" in out, out)

    w = tmp / "smoke-brain" / "knowledge"
    subs = ("biology", "practice", "sources")
    write(w / "INDEX.md", "# Front page\n\nReading protocol…\n\n" + "".join(f"- [[INDEX-{s}]] — {s}\n" for s in subs)
          + f"\nEND OF INDEX (front page) — {len(subs)} sub-indexes\n")
    for s in subs:
        write(w / f"INDEX-{s}.md", f"# Sub-index {s}\n> Entries: 0.\n\nEND OF SUB-INDEX · {s} — 0 entries\n")
    for d in ("sources/clips", "cards", "concepts", "syntheses"):
        write(w / d / ".gitkeep", "")
    write(w / "LOG.md", "# LOG\n\n## [2026-09-26] founding | Founding\n")
    write(w / "PENDING.md", "# PENDING\n")
    code, out = run(S_IDX, ["knowledge"], w.parent)
    case("B4 brain founded with the SCHEMA formats → green", code == 0 and "✓ green" in out, out)
    write(w / "cards" / "hydration.md", "# Card\n")
    write(w / "INDEX-practice.md", "# Sub-index practice\n> Entries: 1.\n\n- [[cards/hydration|Hydration]] — one line\n\n"
                                   "END OF SUB-INDEX · practice — 1 entries\n")
    code, out = run(S_IDX, ["knowledge"], w.parent)
    case("B4 first card with an alias → green", code == 0 and "✓ green" in out, out)


# ─────────────────────────── edges ───────────────────────────
LOGBOOK_BASE = ("# LOGBOOK\n\n> append-only.\n\n## Conventions\nUndated: never rotated.\n\n"
                "## 2026-01-10 — alpha\nAlpha text.\n\n\n\nThree blanks above.\n\n"
                "## [2026-01-05] beta\n```\n## not a heading\n```\nEnd beta.\n\n"
                "## 2026-02-01 — gamma\nGamma text.\n")


def edges_rotator(tmp: Path) -> None:
    p = tmp / "rot"
    write(p / "LOGBOOK.md", LOGBOOK_BASE)
    code, out = run(S_ROT, [], p)
    case("C1 rotator: the undated section is not rotated; the oldest is the bracketed date",
         code == 0 and "2026-01-05" in out and "Conventions" not in out.split("DRY RUN")[1].split("\n", 1)[1], out)
    code, out = run(S_ROT, ["--n", "1", "--apply", "--carried-to", "test"], p)
    arc, log = read(p / "LOGBOOK-archive.md"), read(p / "LOGBOOK.md")
    case("C2 rotator: a «## » inside a code block does not split the entry",
         "## not a heading" in arc and "End beta." in arc and "## not a heading" not in log, arc)
    case("C3 rotator: what stays in the logbook is unchanged (the three blanks remain)",
         "Alpha text.\n\n\n\nThree blanks above." in log and "## Conventions" in log, log)
    case("C3 rotator: rotation index in the header and net bytes reported",
         "Rotation index" in log and "net freed" in out, out)
    code, out = run(S_ROT, ["--until", "20-09-2026"], p)
    case("C4 rotator: --until with an invalid format → explicit error", code != 0 and "YYYY-MM-DD" in out, out)
    for bad in ("20260920", "2026-W39-5"):
        code, out = run(S_ROT, ["--until", bad], p)
        case(f"D1 rotator: --until {bad} (accepted by fromisoformat on Python 3.11+) → error, nothing chosen",
             code != 0 and "YYYY-MM-DD" in out and "DRY RUN" not in out, out)
    write(p / "L1.md", "## 2026-01-01 — ñandú\ntext\n", "latin-1")
    code, out = run(S_ROT, ["--logbook", "L1.md"], p)
    case("C5 rotator: Latin-1 file → clean error, no traceback", code != 0 and "UTF-8" in out and "Traceback" not in out, out)
    q = tmp / "rot-es"
    write(q / "BITACORA.md", "# BITÁCORA\n\n> append-only.\n\n## 2026-01-01 — a\nx\n\n## 2026-02-01 — b\ny\n")
    code, out = run(S_ROT, ["--n", "1", "--ejecutar", "--herederos", "prueba"], q)
    log, arc = read(q / "BITACORA.md"), read(q / "BITACORA-archivo.md")
    case("L1 1.x Spanish logbook: Spanish aliases work and the texts written stay in Spanish",
         code == 0 and "Índice de rotaciones" in log and "Archivo histórico" in arc and "herederos verificados: prueba" in arc,
         out + log + arc)


def edges_continuity(tmp: Path) -> None:
    budgets = "<!-- lint-budgets: PLAN 120/150 14.4/18 | ARCHITECTURE 160/200 24/30 | LOGBOOK 160/200 20/25 -->"

    def project(name: str, claude: str, arch: str = "# ARCH\n", plan_extra: str = "") -> Path:
        p = tmp / name
        write(p / "PLAN.md", f"# PLAN\n{budgets}\n{plan_extra}")
        write(p / "LOGBOOK.md", "# L\n\n## 2026-01-01 — x\ny\n")
        write(p / "ARCHITECTURE.md", arch)
        write(p / "CLAUDE.md", claude)
        return p

    en = ("## Session continuity (MANDATORY)\n\n1. Read PLAN.md before editing.\n5. Measure first with "
          "`python3 scripts/lint_continuity.py --margin`.\n<!-- tino: continuity v2.0 -->\n")
    p = project("en", en)
    code, out = run(S_CONT, [], p)
    case("C8 block located by its marker", code == 0 and "continuity block v2.0" in out and "not found" not in out, out)
    p = project("es-block", "## Continuidad entre sesiones\n\n1. Leé PLAN.\n5. `--margen`.\n<!-- suite-agentica: continuidad v1.5 -->\n")
    code, out = run(S_CONT, [], p)
    case("C8 a 1.x marker is recognized and reported as upgradable", "continuity block v1.5" in out and "1.x block" in out, out)
    p = project("inv-disorder", en, "# ARCH\n\n## Invariants\n\n1. a\n3. c\n2. b\n")
    code, out = run(S_CONT, [], p)
    case("C9 invariants in lower case and out of order → failure", code == 1 and "out of order" in out, out)
    p = project("inv-gap", en, "# ARCH\n\n## INVARIANTS\n\n1. a\n2. b\n4. d\n")
    code, out = run(S_CONT, [], p)
    case("C10 a gap in the invariants → alarm, without the invariants OK", "numbers [3] are missing" in out
         and "OK      INVARIANTS" not in out, out)
    p = project("edge", en, plan_extra="x\n" * 145)
    code, out = run(S_CONT, [], p)
    case("C11 «at the edge» by lines too → ESCALATE", "ESCALATE" in out, out)
    (p / "scripts").mkdir(exist_ok=True)
    code, out = run(S_CONT, [], p / "scripts")
    case("C12 run from a subdirectory → clear failure (exit 1)", code == 1 and "root" in out, out)
    code, out = run(S_CONT, ["--root", ".."], p / "scripts")
    case("C12 with --root it works from a subdirectory", "lint_continuity" in out and "PLAN.md not found" not in out, out)
    p = project("legacy", "## Continuidad entre sesiones\n\n1. Leé PLAN.\nSistema: continuidad v1.3.\n")
    code, out = run(S_CONT, [], p)
    case("C13 legacy «Sistema: … v1.3» marker → upgrade alarm", "LEGACY" in out, out)
    p = project("old-text", "## Continuidad entre sesiones\n\n1. Leé PLAN.\n<!-- suite-agentica: continuidad v1.4 -->\n")
    code, out = run(S_CONT, [], p)
    case("C14 a v1.4 marker over older text → alarm", "block's text is older" in out, out)
    p = project("latin", en)
    write(p / "PLAN.md", f"# PLAN ñ\n{budgets}\n", "latin-1")
    code, out = run(S_CONT, [], p)
    case("C15 PLAN in Latin-1 → clean error (exit 1), no traceback", code == 1 and "UTF-8" in out and "Traceback" not in out, out)
    p = project("invisible", en, plan_extra="text" + chr(0x202E) + "hidden\n")
    code, out = run(S_CONT, [], p)
    case("C16 invisible character in PLAN → alarm", "invisible" in out, out)
    # 1.x Spanish project, untouched: still green
    p = tmp / "es-project"
    write(p / "PLAN.md", "# PLAN\n<!-- lint-topes: PLAN 120/150 14.4/18 | ARQUITECTURA 160/200 24/30 | "
                         "BITACORA 160/200 20/25 | BLOQUE 20 -->\n- 🔄 F1. quedamos en: tabla\n")
    write(p / "BITACORA.md", "# BITÁCORA\n\n## 2026-01-01 — x\ny\n")
    write(p / "ARQUITECTURA.md", "# ARQUITECTURA\n\n## INVARIANTES\n\n1. a\n2. b\n")
    write(p / "CLAUDE.md", "## Continuidad entre sesiones (OBLIGATORIO)\n\n1. Leé PLAN.\n5. Medí con `--margen`.\n"
                           "<!-- suite-agentica: continuidad v1.5 -->\n")
    code, out = run(S_CONT, [], p)
    case("L2 1.x Spanish project (lint-topes, ARQUITECTURA, BITACORA, Spanish block) → green",
         code == 0 and "✅" in out and "BITACORA.md" in out and "INVARIANTS: 2 numbered" in out, out)
    code, out = run(S_CONT, ["--retomar"], p)
    case("L2 the --retomar alias keeps working and finds «quedamos en»", "quedamos en: tabla" in out, out)
    code, out = run(S_CONT, ["--margen"], p)
    case("L2 the --margen alias keeps working", "writing margin" in out and "BITACORA.md" in out, out)


def lesson(slug: str, validation: str, evidence: str = "data", cases: str = "", desc: str = None,
           scope: str = "test", cases_label: str = "**Cases**:") -> str:
    d = desc if desc is not None else f"\"{slug} → principle\""
    ev = f"  evidence: {evidence}\n" if evidence else ""
    return (f"---\nname: {slug}\ndescription: {d}\nmetadata:\n  type: lesson\n  validation: {validation}\n  scope: {scope}\n"
            f"{ev}---\n**Trigger**: t\n**Original error**: e\n**Principle**: p\n**Application**: a\n{cases_label}\n{cases}")


def edges_lessons(tmp: Path) -> None:
    p = tmp / "les"
    write(p / "mem" / "lessons" / "lesson-a.md", lesson("lesson-a", "hypothesis", cases="- 2026-09-01 · origin — x\n"))
    write(p / "mem" / "NOTES.md", "## Agent judgment\n- lesson-a — a → b\nEND OF LESSON INDEX — 1 entries\n"
                                  "- [A note](note_x.md) — a pointer written after the index\n"
                                  "- [Another](note_y.md) — another pointer\n")
    code, out = run(S_LES, ["--dir", "mem/lessons", "--index", "mem/NOTES.md"], p)
    case("C17 an index file with pointers after the END line → green (the section ends at END)",
         code == 0 and "1 bullets" in out, out)
    d = p / "c2"
    write(d / "lesson-hash.md", lesson("lesson-hash", "hypothesis", cases="- 2026-09-01 · origin — x\n",
                                       desc="\"uses #1 and # too\"", scope="\"team #2\""))
    write(d / "lesson-multi.md", lesson("lesson-multi", "hypothesis", cases="- 2026-09-01 · origin — x\n", desc=">"))
    write(d / "lesson-rec.md", lesson("lesson-rec", "recurring", cases="- 2026-09-01 · origin — x\n"))
    write(d / "lesson-conf.md", lesson("lesson-conf", "confirmed", "user",
                                       cases="- 2026-09-01 · origin — x\n- 2026-09-10 · applied — y\n- 2026-09-12 · recurrence — z\n"))
    write(d / "INDEX.md", "## Agent judgment\n" + "".join(f"- {s}\n" for s in ("lesson-hash", "lesson-multi", "lesson-rec", "lesson-conf"))
          + "END OF LESSON INDEX — 4 entries\n")
    code, out = run(S_LES, ["--dir", "c2"], p)
    case("C18 a quoted description with « #» is not cut", "lesson-hash.md: empty description" not in out, out)
    case("C19 a multi-line YAML description → failure", code == 1 and "lesson-multi.md: empty description or a multi-line" in out, out)
    case("C20 recurring with 1 case → warning", "lesson-rec.md: validation «recurring» with 1 dated case" in out, out)
    case("C21 confirmed resting only on the user's word → warning", "the user's word" in out, out)
    code, out = run(S_LES, ["--dir", "c2", "--summary"], p)
    case("C23 --summary counts applied cases and the recurrence rate", "applied=1" in out and "recur=1/2" in out, out)
    case("C18 a quoted value with « #» is read whole (not cut at «#»)", "team #2" in out, out)
    d = p / "c3"
    write(d / "lesson-latin.md", lesson("lesson-latin", "hypothesis") + "ñandú\n", "latin-1")
    write(d / "INDEX.md", "## Agent judgment\nEND OF LESSON INDEX — 0 entries\n")
    code, out = run(S_LES, ["--dir", "c3"], p)
    case("C22 a lesson in Latin-1 → clean failure, no traceback", code == 1 and "UTF-8" in out and "Traceback" not in out, out)
    d = p / "c4"
    write(d / "lessons" / "lesson-a.md", lesson("lesson-a", "hypothesis", cases="- 2026-09-01 · origin — x\n"))
    filler = "".join(f"filler line {i}\n" for i in range(210))
    index = "## Agent judgment\n- lesson-a — a\nEND OF LESSON INDEX — 1 entries\n" + filler
    write(d / "CLAUDE.md", index)
    code, out = run(S_LES, ["--dir", "c4/lessons", "--index", "c4/CLAUDE.md", "--lines-max", "200"], p)
    case("C24 a 213-line index with --lines-max 200 → failure for the load limit", code == 1 and "load limit" in out, out)
    code, out = run(S_LES, ["--dir", "c4/lessons", "--index", "c4/CLAUDE.md"], p)
    case("C24 the same index without a load limit → green", code == 0, out)
    code, out = run(S_LES, ["--dir", "c4/lessons", "--index", "c4/CLAUDE.md", "--bytes-max", "1000"], p)
    case("C24 the byte limit alone also applies", code == 1 and "load limit" in out, out)
    d = p / "c5"
    write(d / "lesson-old.md", lesson("lesson-old", "recurring", evidence="",
                                      cases="- 2026-08-01 — untyped\n- 2026-08-05 — untyped\n"))
    write(d / "INDEX.md", "## Agent judgment\n- lesson-old\nEND OF LESSON INDEX — 1 entries\n")
    code, out = run(S_LES, ["--dir", "c5"], p)
    case("C25 a lesson older than 1.5 (no evidence, untyped cases) → green with a single grouped warning",
         code == 0 and out.count("without a declared `evidence`") == 1, out)
    d = p / "c6"
    write(d / "lesson-label.md", lesson("lesson-label", "hypothesis", cases="- 2026-09-01 · origin — x\n",
                                        cases_label="**Cases of the pilot**:"))
    write(d / "INDEX.md", "## Agent judgment\n- lesson-label — a\nEND OF LESSON INDEX — 1 entries\n")
    code, out = run(S_LES, ["--dir", "c6"], p)
    case("D4 cases under a longer «**Cases …**» label are counted (same criterion as the section check)",
         code == 0 and "0 dated case" not in out and "missing section" not in out, out)
    q = tmp / "les-es"
    write(q / "criterio" / "leccion-uno.md",
          "---\nname: leccion-uno\ndescription: \"cifra → contrastar\"\nmetadata:\n  type: leccion\n  validacion: confirmada\n"
          "  ambito: prueba\n  evidencia: dato\n---\n**Gatillo**: g\n**Error original**: e\n**Principio**: p\n"
          "**Aplicación**: a\n**Casos**:\n- 2026-09-01 · origen — x\n- 2026-09-10 · aplicada — y\n")
    write(q / "CLAUDE.md", "## Criterio del agente (metacognición)\n\n1. Lecciones.\n<!-- suite-agentica: metacognicion v1.5 -->\n"
                           "### Índice de lecciones\n- leccion-uno — cifra → contrastar\nFIN DEL ÍNDICE DE CRITERIO — 1 entradas\n")
    code, out = run(S_LES, ["--dir", "criterio", "--indice", "CLAUDE.md"], q)
    case("L3 1.x Spanish lessons and index (Spanish keys, values, sections and END) → green", code == 0 and "✓ green" in out, out)
    code, out = run(S_LES, ["--dir", "criterio", "--resumen"], q)
    case("L3 the --resumen alias keeps working and shows the value as written", "confirmada" in out and "applied=1" in out, out)
    q = tmp / "les-en-index"
    write(q / "lessons" / "lesson-one.md", lesson("lesson-one", "hypothesis", cases="- 2026-09-01 · origin — x\n"))
    write(q / "lessons" / "lesson-two.md", lesson("lesson-two", "hypothesis", cases="- 2026-09-01 · origin — x\n"))
    write(q / "lessons" / "INDEX.md", "### Lesson index\n- lesson-one — a → b (see lesson-two)\n"
                                      "- lesson-two — c → d\nEND OF LESSON INDEX — 2 entries\n")
    code, out = run(S_LES, [], q)
    case("E4 index moved to lessons/INDEX.md under «Lesson index» (default folder and index) → green", code == 0, out)
    case("E4 a cross reference inside a bullet does not count as a repeated entry", "appears in 2 bullets" not in out, out)


def edges_index(tmp: Path) -> None:
    def wiki(name: str) -> Path:
        w = tmp / name / "knowledge"
        write(w / "INDEX.md", "# P\n- [[INDEX-a|Subdomain A]]\n- [[INDEX-sources]]\nEND OF INDEX (front page) — 2 sub-indexes\n")
        write(w / "cards" / "x.md", "# x\n")
        write(w / "concepts" / "y.md", "# y\n")
        write(w / "INDEX-a.md", "# A\n> Entries: 2.\n- [[cards/x|Card x]] — one\n- [[concepts/y#Definition]] — two\n"
                                "END OF SUB-INDEX · a — 2 entries\n")
        write(w / "INDEX-sources.md", "# S\n> Entries: 0.\nEND OF SUB-INDEX · sources — 0 entries\n")
        write(w / "LOG.md", "# LOG\n## [2026-09-01] founding | f\n" + "".join(f"## [2026-09-{i:02d}] Ingest | i{i}\n" for i in range(2, 14)))
        return w

    w = wiki("i1")
    code, out = run(S_IDX, ["knowledge"], w.parent)
    case("C26 entries with alias and anchor → green", code == 0 and "✓ green" in out, out)
    case("C27 LOG operations with a capital letter count", "Ingests since the last content lint: 12" in out, out)
    write(w / "sources" / "clips" / "new-video.txt", "transcript\n")
    write(w / "cards" / "x.md", "# x\ntext" + chr(0x2066) + "hidden\n")
    write(w / "PENDING.md", "# P\n" + "x" * 26000 + "\n")
    code, out = run(S_IDX, ["knowledge"], w.parent)
    case("C28 a piece in the inbox → warning", "inbox: 1 piece" in out, out)
    case("C29 invisible character in a card → warning", "invisible characters" in out and "cards/x.md" in out, out)
    case("C30 large PENDING → warning", "PENDING.md: 26" in out, out)
    w = wiki("i2")
    write(w / "INDEX-a.md", "# A ñ\n> Entries: 0.\nEND OF SUB-INDEX · a — 0 entries\n", "latin-1")
    code, out = run(S_IDX, ["knowledge"], w.parent)
    case("C31 sub-index in Latin-1 → clean error, no traceback", code == 1 and "UTF-8" in out and "Traceback" not in out, out)
    w = wiki("i3")
    write(w / "sources" / "raw.md", "raw\n")
    root = str(w.parent)
    for path, expected in (("knowledge/sources/raw.md", 2), ("knowledge/sources/new.md", 0),
                           ("knowledge/sources/clips/c.md", 0), ("knowledge/cards/x.md", 0)):
        code, out = run(S_IDX, ["--guard", "knowledge"], w.parent,
                        stdin=json.dumps({"tool_name": "Write", "tool_input": {"file_path": path}}),
                        env={"CLAUDE_PROJECT_DIR": root})
        case(f"C32 guard: {path} → exit {expected}", code == expected, out)
    code, out = run(S_IDX, ["--guard", "knowledge"], w.parent, stdin="not json", env={"CLAUDE_PROJECT_DIR": root})
    case("C32 guard: unreadable input → does not block", code == 0, out)

    w = tmp / "e2e-wiki" / "knowledge"
    write(w / "INDEX.md", "# P\n- [[INDEX-a]]\nEND OF INDEX (front page) — 1 sub-indexes\n")
    write(w / "sources" / "raw-trap.md", "text" + chr(0xE0041) + "hidden\n")
    write(w / "sources" / "raw-unreviewed.md", "other" + chr(0x202E) + "text\n")  # control: this one must warn
    write(w / "cards" / "card-trap.md", "---\nsource: \"[[sources/raw-trap]]\"\n---\nFlags: invisible characters: reviewed.\n")
    write(w / "cards" / "card-broken.md", "---\nsource: \"[[sources/clips/gone]]\"\n---\nx\n")
    write(w / "INDEX-a.md", "# A\n> Entries: 2.\n- [[cards/card-trap]] — t\n- [[cards/card-broken]] — b\nEND OF SUB-INDEX · a — 2 entries\n")
    code, out = run(S_IDX, ["knowledge"], w.parent)
    case("E5 the invisibles warning turns off when the raw file's card notes them as reviewed (and stays for the rest)",
         "raw-unreviewed" in out and "raw-trap" not in out, out)
    case("E6 a card's source field linking a missing raw file → warning", "cards/card-broken.md: the source field" in out, out)

    w = tmp / "es-wiki" / "conocimiento"
    write(w / "INDICE.md", "# Portada\n- [[INDICE-a]]\n- [[INDICE-fuentes]]\nFIN DEL ÍNDICE (portada) — 2 sub-índices\n")
    write(w / "fichas" / "x.md", "---\nfuente: \"[[fuentes/crudo]]\"\n---\n# x\n")
    write(w / "fuentes" / "crudo.md", "crudo\n")
    write(w / "INDICE-a.md", "# A\n> Entradas: 1.\n- [[fichas/x]] — una\nFIN DEL SUB-ÍNDICE · a — 1 entradas\n")
    write(w / "INDICE-fuentes.md", "# F\n> Entradas: 1.\n- [[fuentes/crudo]] — crudo\nFIN DEL SUB-ÍNDICE · fuentes — 1 entradas\n")
    write(w / "LOG.md", "# LOG\n## [2026-09-01] fundacion | f\n## [2026-09-02] ingesta | i\n")
    code, out = run(S_IDX, [], w.parent)
    case("L4 1.x Spanish wiki (conocimiento/, INDICE, fichas, fuentes, FIN lines), default folder → green",
         code == 0 and "✓ green" in out and "Ingests since the last content lint: 1" in out, out)
    code, out = run(S_IDX, ["--guardia", "conocimiento"], w.parent,
                    stdin=json.dumps({"tool_name": "Edit", "tool_input": {"file_path": "conocimiento/fuentes/crudo.md"}}),
                    env={"CLAUDE_PROJECT_DIR": str(w.parent)})
    case("L4 the --guardia alias protects fuentes/ (exit 2)", code == 2, out)


def edges_e2e(tmp: Path) -> None:
    p = tmp / "e2e-resume"
    write(p / "PLAN.md", "# PLAN\n> States: ✅ done · 🔄 in progress · ⏳ pending\n\n"
                         "- 🔄 Ch. 2 «Watering». where we left off: table per pot drafted\n"
                         "  with the manual's values; next step: check against the CSV.\n- ⏳ Ch. 3\n")
    code, out = run(S_CONT, ["--resume"], p)
    case("E1 --resume brings the continuation line (the «next step»)", "next step: check" in out, out)
    case("E1 --resume does not repeat the states legend", "States:" not in out, out)
    p = tmp / "d2-resume"
    write(p / "PLAN.md", "# PLAN\nStates: ✅ done · 🔄 in progress · ⏳ pending <!-- tino:legend -->\n"
                         "Estados: ✅ hecho · 🔄 en curso · ⏳ pendiente\n"
                         "- ✅ F5 shipped · 🔄 F6 where we left off: pricing table\n- ⏳ F7\n")
    code, out = run(S_CONT, ["--resume"], p)
    case("D2 --resume keeps a task line that mixes ✅ and 🔄 (only the legend is skipped)",
         "F6 where we left off: pricing table" in out, out)
    case("D2 --resume skips the legend recognized by its marker or its text, in either language",
         "States:" not in out and "Estados:" not in out, out)
    p = tmp / "e2e-rot"
    old = "> **Rotation index** — " + " · ".join(f"2026-0{m}-01: 1 → archive :{m}" for m in range(1, 8))
    write(p / "LOGBOOK.md", "# L\n\n" + old + "\n\n## 2026-01-01 — a\n" + "text\n" * 40 + "\n## 2026-02-01 — b\ny\n")
    code, out = run(S_ROT, ["--apply"], p)
    case("E2 --apply without --carried-to refuses before announcing the rotation", code != 0 and "ROTATION" not in out, out)
    code, dry = run(S_ROT, [], p)
    before = (p / "LOGBOOK.md").stat().st_size
    code, out = run(S_ROT, ["--apply", "--carried-to", "test"], p)
    net = before - (p / "LOGBOOK.md").stat().st_size
    case("E2 the rotation frees net bytes (the rotation index is compact)", net > 0, out)
    case("E2 the dry run announces exactly the net that is freed afterwards", f"frees {net} B net" in dry, dry + out)
    case("E2 the rotation index keeps at most five items",
         read(p / "LOGBOOK.md").split("\n")[2].count(" · ") <= 4, read(p / "LOGBOOK.md")[:600])
    p = tmp / "e2e-block"
    write(p / "PLAN.md", "# PLAN\n<!-- lint-budgets: DOCS PLAN -->\n")
    write(p / "CLAUDE.md", "## Brain of something\n\n" + "rule\n" * 6 + "### Rituals\n" + "step\n" * 10
          + "<!-- tino: brain v2.0 -->\n## Continuity\n1. --margin\n<!-- tino: continuity v2.0 -->\n")
    code, out = run(S_CONT, [], p)
    case("E3 a block is counted from its ## heading even with a ### subsection", "brain block v2.0 in CLAUDE.md: 20 lines" in out, out)
    p = tmp / "d3-shared"
    write(p / "PLAN.md", "# PLAN\n<!-- lint-budgets: DOCS PLAN -->\n")
    write(p / "CLAUDE.md", "## Continuity and judgment\n\n1. --margin\n<!-- tino: continuity v2.0 -->\n2. lessons\n"
          + "rule\n" * 16 + "<!-- tino: metacognition v2.0 -->\n")
    code, out = run(S_CONT, [], p)
    case("D3 two markers sharing one heading: the second is reported as measured with the first, not measured twice",
         "shares its heading with the continuity block" in out and "metacognition block: " not in out, out)


def main() -> None:
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    tmp = Path(tempfile.mkdtemp(prefix="tino-tests-"))
    try:
        if not only or "static" in only:
            static()
        if not only or "smoke" in only:
            smoke(tmp)
        if not only or "edges" in only:
            edges_rotator(tmp)
            edges_continuity(tmp)
            edges_lessons(tmp)
            edges_index(tmp)
            edges_e2e(tmp)
    finally:
        shutil.rmtree(str(tmp), ignore_errors=True)
    for d in REPO.rglob("__pycache__"):
        shutil.rmtree(str(d), ignore_errors=True)
    bad = [r for r in results if not r[1]]
    for name, ok, detail in results:
        if VERBOSE or not ok:
            print(f"{'✓' if ok else '✗'} {name}")
            if not ok and detail:
                print("    " + detail.strip().replace("\n", "\n    ")[:1500])
    print(f"tino bench (Python {sys.version.split()[0]}): {len(results) - len(bad)}/{len(results)} cases green.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
