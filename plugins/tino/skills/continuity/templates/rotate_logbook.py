#!/usr/bin/env python3
"""Mechanical logbook rotation — moves the oldest entries to the archive.

Template from the `continuity` skill of tino (v2.0). Without `--apply` it is
a DRY RUN: it shows which entries it would rotate and how many net bytes it
frees, touching nothing.

  python3 scripts/rotate_logbook.py                       → dry run: the oldest entry
  python3 scripts/rotate_logbook.py --n 3                 → dry run: the 3 oldest
  python3 scripts/rotate_logbook.py --until 2026-09-20    → dry run: every entry dated before that day
  python3 scripts/rotate_logbook.py --n 3 --apply --carried-to "PLAN §F6 · ARCHITECTURE §Rules · commit abc123"

Rules: (1) nothing is deleted — entries MOVE verbatim to the archive, under an
HTML marker with the date, the labels and where their live parts went;
(2) `--apply` requires `--carried-to`: the text where the operator declares
that the LIVE part of each entry already rules from somewhere else (PLAN,
ARCHITECTURE, the instructions, scripts, commit) — the script moves, the check is
human; (3) the logbook header gets (or extends) a compact "Rotation index"
line (date, count and archive line; it keeps the last five — the full detail
is in the archive's markers). The dry run reports the net bytes freed,
counting that line.
An entry is everything from a `## YYYY-MM-DD …` heading (also
`## [YYYY-MM-DD] …`) to the next `## ` outside a code block. Age comes from
the heading's date; on equal dates, the one higher up. The header (before the
first `## `) and every `## ` section WITHOUT a date (conventions, indexes)
never rotate. The rest of the file stays byte for byte as it was: entries
that stay are not edited. Bytes are measured in UTF-8. Standard library only.

Language: the texts this script writes into the logbook and the archive exist
in English and in Spanish. It writes Spanish for a Spanish logbook
(BITACORA.md, or a header that already carries "Índice de rotaciones") and
English otherwise; `--lang` overrides. Flags keep their 1.x Spanish aliases.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

RE_ENTRY = re.compile(r"^## \[?(\d{4}-\d{2}-\d{2})")
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# Texts the rotator writes (the index line is also found by its text, in either language)
TEXTS = {
    "en": {
        "header": ("# LOGBOOK — Archive (rotated entries)\n\n"
                   "> Moved from {logbook} to keep it within its size budget. Same\n"
                   "> append-only rule: never edited, never deleted.\n"),
        "index": "Rotation index",
        "marker": "rotated from {logbook} on {date} ({labels}): entries moved verbatim — live parts carried to: {carried}",
        "item": "{date}: {n} → archive :{line}",
    },
    "es": {
        "header": ("# BITÁCORA — Archivo histórico (entradas rotadas)\n\n"
                   "> Movidas desde {logbook} por presupuesto de tamaño. Mismo carácter\n"
                   "> append-only: nunca se edita ni se borra.\n"),
        "index": "Índice de rotaciones",
        "marker": "rotado desde {logbook} el {date} ({labels}): entradas íntegras — herederos verificados: {carried}",
        "item": "{date}: {n} → archivo :{line}",
    },
}
MAX_IN_INDEX = 5


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        sys.exit(f"✗ {path} is not UTF-8 (byte {e.start}): convert it before rotating; nothing was touched.")


def nbytes(s: str) -> int:
    return len(s.encode("utf-8"))


def split(text: str):
    lines = text.split("\n")
    idx, in_code = [], False
    for i, line in enumerate(lines):
        if line.lstrip().startswith(("```", "~~~")):
            in_code = not in_code
        elif not in_code and line.startswith("## "):
            idx.append(i)
    if not idx:
        return lines, []
    head = lines[: idx[0]]
    entries = []
    for k, i in enumerate(idx):
        j = idx[k + 1] if k + 1 < len(idx) else len(lines)
        m = RE_ENTRY.match(lines[i])
        entries.append({"date": m.group(1) if m else None, "title": lines[i][3:].strip(), "lines": lines[i:j]})
    return head, entries


def index_texts():
    return [t["index"] for t in TEXTS.values()]


def build(head, entries, chosen, today: str, marker_line: int, texts: dict) -> str:
    """The logbook without the chosen entries and with its rotation index up to date (the only thing added)."""
    drop = set(chosen)
    new = list(head)
    for k, e in enumerate(entries):
        if k not in drop:
            new.extend(e["lines"])
    item = texts["item"].format(date=today, n=len(chosen), line=marker_line)
    for i, line in enumerate(new[: len(head)]):
        found = next((t for t in index_texts() if line.startswith(f"> **{t}**")), None)
        if found:  # extend the existing line, keeping its language
            previous = [x.strip() for x in line.split("—", 1)[1].split(" · ")] if "—" in line else []
            new[i] = f"> **{found}** — " + " · ".join((previous + [item])[-MAX_IN_INDEX:])
            break
    else:
        last = max((i for i, line in enumerate(new[: len(head)]) if line.startswith(">")), default=len(head) - 1)
        new[last + 1: last + 1] = [">", f"> **{texts['index']}** — " + item]
    return "\n".join(new)  # blank lines are not normalized: what stays is not edited


def label(title: str) -> str:
    m = re.search(r"\(([^)]{1,30})\)", title)
    return m.group(1) if m else re.sub(r"[*`\[\]]", "", title)[:40]


def default_logbook() -> Path:
    for name in ("LOGBOOK.md", "BITACORA.md"):
        if Path(name).exists():
            return Path(name)
    return Path("LOGBOOK.md")


def default_archive(logbook: Path) -> Path:
    if logbook.name == "BITACORA.md":
        return logbook.with_name("BITACORA-archivo.md")
    return logbook.with_name(f"{logbook.stem}-archive.md")


def pick_language(logbook: Path, text: str, forced) -> str:
    if forced:
        return forced
    head = text.split("\n## ", 1)[0]
    return "es" if logbook.name.upper().startswith("BITACORA") or TEXTS["es"]["index"] in head else "en"


def main() -> None:
    ap = argparse.ArgumentParser(description="Mechanical logbook rotation (dry run by default).")
    ap.add_argument("--logbook", "--bitacora", dest="logbook", default=None,
                    help="default: LOGBOOK.md, or BITACORA.md if that is the one that exists")
    ap.add_argument("--archive", "--archivo", dest="archive", default=None,
                    help="default: <logbook>-archive.md (BITACORA-archivo.md for BITACORA.md)")
    ap.add_argument("--n", type=int, default=1, help="how many entries (the oldest ones)")
    ap.add_argument("--until", "--hasta", dest="until", help="rotate every entry dated before YYYY-MM-DD (ignores --n)")
    ap.add_argument("--apply", "--ejecutar", dest="apply", action="store_true", help="without it, only a dry run")
    ap.add_argument("--carried-to", "--herederos", dest="carried", default="",
                    help="where the live part of each entry rules now (required with --apply)")
    ap.add_argument("--lang", choices=sorted(TEXTS), default=None,
                    help="language of the texts written into the logbook (default: detected)")
    a = ap.parse_args()
    if a.until:
        valid = bool(RE_DATE.match(a.until))
        if valid:
            try:
                dt.date.fromisoformat(a.until)
            except ValueError:
                valid = False
        if not valid:
            sys.exit(f"--until expects YYYY-MM-DD (got {a.until!r}); nothing was touched.")
    if a.apply and not a.carried.strip():
        sys.exit("--apply requires --carried-to \"<where the live part rules now>\" — the check is human. "
                 "Nothing was touched.")

    log = Path(a.logbook) if a.logbook else default_logbook()
    arc = Path(a.archive) if a.archive else default_archive(log)
    if not log.exists():
        sys.exit(f"{log} not found")
    text = read(log)
    texts = TEXTS[pick_language(log, text, a.lang)]
    head, entries = split(text)
    dated = [k for k in range(len(entries)) if entries[k]["date"]]
    if not dated:
        sys.exit("the logbook has no «## YYYY-MM-DD …» entries (undated sections never rotate)")
    order = sorted(dated, key=lambda k: (entries[k]["date"], k))
    if a.until:
        chosen = [k for k in order if entries[k]["date"] < a.until]
    else:
        chosen = order[: max(0, a.n)]
    if not chosen:
        print("nothing to rotate with that criterion.")
        return

    today = dt.date.today().isoformat()
    arc_text = read(arc) if arc.exists() else texts["header"].format(logbook=log.name)
    if not arc_text.endswith("\n"):
        arc_text += "\n"
    marker_line = arc_text.count("\n") + 2
    new = build(head, entries, chosen, today, marker_line, texts)
    before, after = nbytes(text), nbytes(new)
    undated = len(entries) - len(dated)
    print(f"{'ROTATION' if a.apply else 'DRY RUN'} — {len(chosen)} oldest entr{'y' if len(chosen) == 1 else 'ies'} "
          f"of {len(dated)} dated"
          + (f" ({undated} undated section(s): never rotated)" if undated else "")
          + f"; the logbook goes from {before} to {after} B (frees {before - after} B net, counting the rotation index):")
    for k in sorted(chosen):
        e = entries[k]
        print(f"  · {e['date']} [{label(e['title'])}] {len(e['lines'])} lines / "
              f"{nbytes(chr(10).join(e['lines']))} B — {e['title'][:70]}")
    if not a.apply:
        print("Dry run: nothing was touched. Check that the LIVE part of each entry already rules elsewhere and "
              "repeat with --apply --carried-to \"…\".")
        return

    labels = ", ".join(label(entries[k]["title"]) for k in sorted(chosen))
    block = "\n<!-- " + texts["marker"].format(logbook=log.name, date=today, labels=labels,
                                               carried=a.carried.strip()) + " -->\n\n"
    for k in sorted(chosen):
        block += "\n".join(entries[k]["lines"]).rstrip("\n") + "\n\n"
    arc.write_text(arc_text + block, encoding="utf-8")
    log.write_text(new, encoding="utf-8")
    print(f"Done: {len(chosen)} entr{'y' if len(chosen) == 1 else 'ies'} → {arc.name} :{marker_line} · "
          f"logbook {before} → {nbytes(new)} B (net freed: {before - nbytes(new)} B). Review the diff before committing.")


if __name__ == "__main__":
    main()
