# Changelog

tino follows semantic versioning. Each skill keeps its own detailed
changelog, with the upgrade steps its installer applies:
[continuity](plugins/tino/skills/continuity/CHANGELOG.md),
[metacognition](plugins/tino/skills/metacognition/CHANGELOG.md) and
[brain](plugins/tino/skills/brain/CHANGELOG.md).

## 2.0.1 — 2026-10-10

Documentation and wording only; no change to the files' formats or to what
the scripts check.

- The descriptions, the READMEs, the guide and `PRIVACY.md` now say exactly
  what needs your OK: installations, lessons, wiki pages and graduations.
  The plan, the logbook and the architecture document are kept up to date by
  the closing ritual, which reports what it changed.
- The skills call a lesson a lesson everywhere; "card" is kept for the
  brain's cards.
- The skills and the guide describe `.claude/` as a protected path whose
  write behavior depends on the permission mode, instead of saying that
  Claude Code always asks.
- The ingest ritual and the brain's protocol agree that a single piece of
  unknown origin is read first in a subagent.
- `docs/evals.md`: corrected counts for the hidden-instruction case (all six
  baseline runs read the post), the judge and cost lines, and new caveats on
  git, memory and CLAUDE.md inside the eval sandbox; five checks are graded
  by a model, not two.
- The READMEs open with "Memory is not judgment." (in Spanish, "Recordar no
  es tener criterio.") instead of "Memory is easy. Judgment is hard."
- Correction to the 2.0.0 notes: the piece-by-piece check of what the
  rituals and installers write (figures from their source, quotations
  verbatim, no claim more certain than its evidence) is an instruction to
  the agent, not a mechanism. The changelogs now say so.
- Also included, from commits after 2.0.0: the plugin has an icon and links
  to its documentation, support and privacy pages; the READMEs and
  `CITATION.cff` carry the Zenodo DOI for all versions; the README's bakery
  example says that the agent rejects a post whose advice the bake log had
  already tried with poor results, instead of saying the log "refutes" it.

## 2.0.0 — 2026-09-28

First public release.

- A Claude Code plugin (`tino`, in the `pfm` marketplace) with three skills:
  `continuity`, `metacognition` and `brain`. Each one also works as a
  standalone Agent Skill.
- English is the source language. Installed files are written in the
  project's language, with two token sets: English, and the Spanish one of
  the 1.x releases, which the installers use for Spanish-language projects.
  The scripts accept both, in any mix.
- The installers no longer write permission rules or hooks. Optional
  guardrails for Claude Code are documented in
  [`docs/guardrails.md`](docs/guardrails.md).
- The skills never read the agent's own memory or past conversations; the
  lessons and the wiki live in the project (a rule graduated across
  projects goes to the user's global instructions, with the user's OK).
- The rituals and installers instruct the agent to check what it writes,
  piece by piece: figures from their source, quotations verbatim, and no
  claim more certain than its evidence.
- A ritual that cannot be installed as a skill goes to `rituals/<name>.md`,
  read on demand, instead of the instructions file.
- A test bench (`tests/test_suite.py`) and an eval suite
  (`plugins/tino/evals/`).

## 1.x — July to September 2026

Private releases in Spanish, used in the author's own projects. Upgrading a
1.x project to 2.0 keeps its Spanish file names; see each skill's changelog.
