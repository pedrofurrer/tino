#!/usr/bin/env python3
"""Verifier of the judgment lessons and their index.

Template from the `metacognition` skill of tino (v2.0). The installer copies
it into the project (e.g. `scripts/lint_lessons.py`). Usage:

  python3 scripts/lint_lessons.py --dir lessons --index CLAUDE.md        (index in the instructions: default)
  python3 scripts/lint_lessons.py --dir lessons --index lessons/INDEX.md
  python3 scripts/lint_lessons.py … --summary   → one line per lesson (validation · scope · evidence ·
                                                  cases with applied/recurrences · last change),
                                                  for the introspection

Checks on each `lesson-*.md`: frontmatter with `name` equal to the file,
a one-line `description`, `metadata.type: lesson`, `validation` within the
admitted set (proposed · hypothesis · recurring · confirmed · graduated ·
archived · example), `scope` present, `evidence` declared (data · source ·
reality · user; missing ones are reported in a single line); sections
Trigger / Original error / Principle / Application / Cases (missing →
warning); enough dated cases for its validation (hypothesis ≥1, recurring
≥2, confirmed ≥1 `applied` or ≥2) and a `confirmed` lesson resting only on
the user's word (warning). Cases are written
`- YYYY-MM-DD · origin|applied|recurrence — …`: the summary counts applied
cases and recurrences and gives each lesson's recurrence rate.
On the index (the section whose heading contains "Agent judgment" or "Lesson
index", closed by its "END OF LESSON INDEX — N entries" line; without an END
line, at the next heading of its level): only entries carry a "- " bullet,
and each belongs to the first lesson it names (other mentions are cross
references); a cap on bullets (`--max-entries`, 20 by default), no lesson in
two bullets, no reference to a missing lesson (failure), active lessons not
referenced (warning), END with the exact count. Optionally, for an index
file loaded under a size limit: the section within the first N lines
(--position-max) and the file under a load limit (--lines-max / --bytes-max;
warning at 90 %, failure above). Invisible characters (bidi controls, Unicode tags, zero-width
spaces) in lessons or index: warning. Exit 1 = failure; warnings do not fail.
Read-only; standard library only.

Fixed tokens: the index headings, the END line, the `lesson-` prefix, the
frontmatter keys and values and the section labels are read by this script.
They exist in English and in the Spanish set of 1.x projects (also written
for Spanish-language projects); both are accepted, in any mix
(docs/format.md lists them).
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

# ── Fixed tokens (English · Spanish) ───────────────────────────────────────
INDEX_HEADINGS = ("agent judgment", "lesson index", "criterio del agente", "índice de lecciones")
RE_END = re.compile(r"^(?:END OF LESSON INDEX — (\d+) entries|FIN DEL ÍNDICE DE CRITERIO — (\d+) entradas)\s*$")
PREFIXES = ("lesson-", "leccion-")
TYPES = ("lesson", "leccion")
VALIDATION = {"proposed": "proposed", "hypothesis": "hypothesis", "recurring": "recurring",
              "confirmed": "confirmed", "graduated": "graduated", "archived": "archived", "example": "example",
              "propuesta": "proposed", "hipotesis": "hypothesis", "recurrente": "recurring",
              "confirmada": "confirmed", "graduada": "graduated", "archivada": "archived", "ejemplo": "example"}
ACTIVE = {"hypothesis", "recurring", "confirmed"}
EVIDENCE = {"data": "data", "source": "source", "reality": "reality", "user": "user",
            "dato": "data", "fuente": "source", "realidad": "reality", "usuario": "user"}
KEYS = {"validation": ("validation", "validacion"), "scope": ("scope", "ambito"),
        "evidence": ("evidence", "evidencia"), "carried_to": ("carried_to", "heredero")}
SECTIONS = (("Trigger", "Gatillo"), ("Original error", "Error original"), ("Principle", "Principio"),
            ("Application", "Aplicación"), ("Cases", "Casos"))
CASES_LABEL = r"\*\*(?:Cases|Casos)\b"
CASE_APPLIED = r"(?:applied|aplicada)\b"
CASE_RECURRENCE = r"(?:recurr|reincid)"
# ─────────────────────────────────────────────────────────────────────────────
RE_SLUG = re.compile(r"(?:lesson|leccion)-[a-z0-9]+(?:-[a-z0-9]+)*")
RE_CASE = re.compile(r"^\s*- (\d{4}-\d{2}-\d{2})\b(.*)$", re.M)
INVISIBLE = re.compile("[" + "".join(chr(a) + ("-" + chr(b) if b != a else "") for a, b in (
    (0x200B, 0x200C), (0x200E, 0x200F), (0x202A, 0x202E), (0x2060, 0x2064), (0x2066, 0x2069),
    (0xFEFF, 0xFEFF), (0xE0000, 0xE007F))) + "]")  # bidi, Unicode tags, zero width (no invisible literals here)
BOM = chr(0xFEFF)

failures: list = []
warnings: list = []
no_evidence: list = []


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        failures.append(f"{path.name}: not UTF-8 (byte {e.start}); convert it")
        return ""


def invisible(name: str, text: str) -> None:
    n = sum(1 for m in INVISIBLE.finditer(text) if not (m.start() == 0 and m.group(0) == BOM))
    if n:
        warnings.append(f"{name}: {n} invisible character(s) — review: this is how instructions get hidden")


def frontmatter(text: str) -> dict:
    """Minimal parser: top-level `key: value` and one nested level under `metadata:`."""
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fm: dict = {}
    parent = None
    for line in parts[1].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^(\s*)([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            continue
        raw = m.group(3).strip()
        if len(raw) >= 2 and raw[0] in "\"'" and raw[0] in raw[1:]:  # quoted: a «#» is text
            value = raw[1:raw.index(raw[0], 1)]
        else:
            value = raw.split(" #")[0].strip()
        indent, key = len(m.group(1)), m.group(2)
        if indent == 0:
            parent = key if value == "" else None
            fm[key] = value if value != "" else {}
        elif parent:
            fm[parent][key] = value
    return fm


def field(meta: dict, name: str) -> str:
    return next((meta[k] for k in KEYS[name] if k in meta), "")


def stem_without_prefix(slug: str) -> str:
    return next((slug[len(p):] for p in PREFIXES if slug.startswith(p)), slug)


def check_lesson(p: Path) -> dict:
    text = read(p)
    base = {"slug": p.stem, "validation": "", "raw_validation": "", "scope": "", "evidence": "", "cases": 0,
            "applied": 0, "recurrences": 0, "carried_to": "", "mtime": dt.datetime.fromtimestamp(p.stat().st_mtime)}
    if not text:  # unreadable or empty: the failure is (or will be) recorded; nothing else is chained
        if p.stat().st_size == 0:
            failures.append(f"{p.name}: empty file")
        return base
    invisible(p.name, text)
    fm = frontmatter(text)
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    if not fm:
        failures.append(f"{p.name}: no frontmatter")
    if fm.get("name") != p.stem:
        failures.append(f"{p.name}: name «{fm.get('name')}» ≠ file «{p.stem}»")
    if not fm.get("description") or fm.get("description") in (">", "|", ">-", "|-"):
        failures.append(f"{p.name}: empty description or a multi-line YAML block (the index needs one line)")
    if meta.get("type") not in TYPES:
        warnings.append(f"{p.name}: metadata.type ≠ lesson")
    raw_val = field(meta, "validation")
    val = VALIDATION.get(raw_val, "")
    if not val:
        failures.append(f"{p.name}: validation «{raw_val}» outside {sorted(set(VALIDATION.values()))}")
    if not field(meta, "scope"):
        warnings.append(f"{p.name}: no scope")
    raw_ev = field(meta, "evidence")
    ev = EVIDENCE.get(raw_ev, "")
    if raw_ev and not ev:
        warnings.append(f"{p.name}: evidence «{raw_ev}» outside {sorted(set(EVIDENCE.values()))}")
    elif not raw_ev and val not in ("example", "archived", "graduated"):
        no_evidence.append(p.stem)
    missing = [en for en, es in SECTIONS if not re.search(r"\*\*(?:" + re.escape(en) + "|" + re.escape(es) + r")\b", text)]
    if missing:
        warnings.append(f"{p.name}: missing section(s) {', '.join(missing)}")
    m = re.search(CASES_LABEL + r".*", text, re.S)  # the same label that marks the section is where the cases start
    cases = RE_CASE.findall(m.group(0)) if m else []
    applied = sum(1 for _, rest in cases if re.match(r"\s*[·:—-]?\s*" + CASE_APPLIED, rest, re.I))
    recur = sum(1 for _, rest in cases if re.match(r"\s*[·:—-]?\s*" + CASE_RECURRENCE, rest, re.I))
    minimum = {"hypothesis": 1, "recurring": 2}.get(val)
    if minimum and len(cases) < minimum:
        warnings.append(f"{p.name}: validation «{raw_val}» with {len(cases)} dated case(s); the scale asks for ≥{minimum}")
    if val == "confirmed":
        if applied == 0 and len(cases) < 2:
            warnings.append(f"{p.name}: «{raw_val}» without an `applied` case or 2 dated cases")
        if ev == "user":
            warnings.append(f"{p.name}: «{raw_val}» resting only on the user's word — was it corroborated by data, "
                            f"a source or reality? (if not, back to recurring or hypothesis)")
    base.update({"validation": val, "raw_validation": raw_val, "scope": field(meta, "scope"), "evidence": raw_ev,
                 "cases": len(cases), "applied": applied, "recurrences": recur,
                 "carried_to": field(meta, "carried_to")})
    return base


def end_count(line: str):
    m = RE_END.match(line)
    return int(m.group(1) or m.group(2)) if m else None


def check_index(index: Path, lessons: dict, cap: int, position_max, lines_max, bytes_max) -> None:
    text = read(index)
    if not text:
        failures.append(f"{index.name}: empty or unreadable index")
        return
    invisible(index.name, text)
    lines = text.split("\n")
    total_lines, total_bytes = len(lines) - (1 if text.endswith("\n") else 0), index.stat().st_size
    limits = [(n, m, unit) for n, m, unit in ((total_lines, lines_max, "lines"), (total_bytes, bytes_max, "B")) if m]
    limit_text = " / ".join(f"{m} {unit}" for _, m, unit in limits)
    if any(n > m for n, m, _ in limits):
        failures.append(f"{index.name}: {total_lines} lines / {total_bytes} B exceeds the load limit "
                        f"({limit_text}) — whatever follows is NOT loaded")
    elif any(n > 0.9 * m for n, m, _ in limits):
        warnings.append(f"{index.name}: {total_lines} lines / {total_bytes} B, close to the load limit ({limit_text})")
    start = next((i for i, line in enumerate(lines)
                  if line.startswith("#") and any(t in line.lower() for t in INDEX_HEADINGS)), None)
    if start is None:
        failures.append(f"{index.name}: section «Agent judgment» (or «Lesson index») not found")
        return
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    end_idx = next((j for j in range(start + 1, len(lines)) if RE_END.match(lines[j])), None)
    if end_idx is None:
        end = next((j for j in range(start + 1, len(lines))
                    if lines[j].startswith("#") and len(lines[j]) - len(lines[j].lstrip("#")) <= level), len(lines))
        failures.append("index: no «END OF LESSON INDEX — N entries» line closing the section")
    else:
        end = end_idx + 1
    section = "\n".join(lines[start:end])
    if position_max and start + 1 > position_max:
        warnings.append(f"{index.name}: the lessons section starts at line {start+1} (> {position_max}); it should "
                        f"come first — the tail of the file is the first thing lost")
    bullets = [line for line in lines[start:end] if line.startswith("- ")]
    if len(bullets) > cap:
        failures.append(f"index: {len(bullets)} bullets > cap {cap}")
    seen: dict = {}
    for b in bullets:  # each bullet belongs to the FIRST lesson it names; the others are cross references
        m = RE_SLUG.search(b)
        if m:
            seen[m.group(0)] = seen.get(m.group(0), 0) + 1
    for s, n in seen.items():
        if n > 1:
            failures.append(f"index: {s} appears in {n} bullets")
    referenced = set(RE_SLUG.findall(section))
    for s in lessons:  # a mention without the prefix (e.g. a graduated one compressed to its name) also counts
        if s not in referenced and re.search(r"(?<![\w-])" + re.escape(stem_without_prefix(s)) + r"(?![\w-])", section):
            referenced.add(s)
    for s in sorted(referenced - set(lessons)):
        failures.append(f"index: reference to {s}, which does not exist in the lessons folder")
    for s, d in sorted(lessons.items()):
        if d["validation"] in ACTIVE and s not in referenced:
            warnings.append(f"{s} ({d['raw_validation']}) is not referenced in the index")
    if end_idx is not None and end_count(lines[end_idx]) != len(bullets):
        failures.append(f"index: the END line declares {end_count(lines[end_idx])} entries and there are {len(bullets)} bullets")
    print(f"Index: {index.name}, section from line {start+1} · {len(bullets)} bullets (cap {cap}) · "
          f"{len(referenced)} lessons referenced · file {total_lines} lines / {total_bytes} B"
          + (f" (load limit {limit_text})" if limits else ""))


def default_dir() -> Path:
    for name in ("lessons", "criterio"):
        if Path(name).is_dir():
            return Path(name)
    return Path("lessons")


def default_index(d: Path) -> Path:
    for name in ("INDEX.md", "INDICE.md"):
        if (d / name).exists():
            return d / name
    return d / "INDEX.md"


def main() -> None:
    ap = argparse.ArgumentParser(description="Verifier of the judgment lessons and their index.")
    ap.add_argument("--dir", default=None, help="lessons folder (default: lessons/, or criterio/ in 1.x projects)")
    ap.add_argument("--index", "--indice", dest="index", default=None,
                    help="file holding the «Agent judgment» section (default: <dir>/INDEX.md)")
    ap.add_argument("--max-entries", "--tope", dest="cap", type=int, default=20)
    ap.add_argument("--position-max", "--posicion-max", dest="position_max", type=int, default=None,
                    help="optional: the section must start within the first N lines")
    ap.add_argument("--lines-max", "--lineas-max", dest="lines_max", type=int, default=None,
                    help="optional: load limit of the index file, in lines")
    ap.add_argument("--bytes-max", dest="bytes_max", type=int, default=None,
                    help="optional: load limit of the index file, in bytes")
    ap.add_argument("--summary", "--resumen", dest="summary", action="store_true")
    a = ap.parse_args()
    d = Path(a.dir).expanduser() if a.dir else default_dir()
    if not d.is_dir():
        sys.exit(f"✗ lessons folder {d} not found")
    files = sorted({p for prefix in PREFIXES for p in d.glob(prefix + "*.md")})
    lessons = {p.stem: check_lesson(p) for p in files}
    if no_evidence:  # a single warning: lessons older than 1.5 gain it when the introspection touches them
        warnings.append(f"{len(no_evidence)} lesson(s) without a declared `evidence` (data · source · reality · user; "
                        f"filled in when the introspection touches them): {', '.join(no_evidence[:5])}"
                        + (" …" if len(no_evidence) > 5 else ""))
    if a.summary:
        for s, x in sorted(lessons.items(), key=lambda kv: kv[1]["mtime"], reverse=True):
            uses = x["applied"] + x["recurrences"]
            rate = f" recur={x['recurrences']}/{uses}" if uses else ""
            carried = x["carried_to"]
            print(f"{x['mtime']:%Y-%m-%d %H:%M}  {x['raw_validation']:<11} {x['scope']:<16} {x['evidence'] or '-':<9} "
                  f"cases={x['cases']:<3} applied={x['applied']:<2}{rate} "
                  f"{'carried_to=' + carried + ' ' if carried and carried != '~' else ''}{s}")
        return
    index = Path(a.index).expanduser() if a.index else default_index(d)
    pos, lmax, bmax = a.position_max, a.lines_max, a.bytes_max
    if index.exists():
        check_index(index, lessons, a.cap, pos, lmax, bmax)
    else:
        failures.append(f"index {index} not found")
    count: dict = {}
    for x in lessons.values():
        count[x["raw_validation"]] = count.get(x["raw_validation"], 0) + 1
    print(f"Lessons: {len(lessons)} in {d} · " + " · ".join(f"{k} {v}" for k, v in sorted(count.items())))
    for w in warnings:
        print(f"  ⚠ {w}")
    for f in failures:
        print(f"  ✗ {f}")
    if failures:
        print(f"✗ {len(failures)} failure(s)")
        sys.exit(1)
    print(f"✓ green ({len(warnings)} warning(s))")


if __name__ == "__main__":
    main()
