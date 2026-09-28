# Changelog

tino follows semantic versioning. Each skill keeps its own detailed
changelog, with the upgrade steps its installer applies:
[continuity](plugins/tino/skills/continuity/CHANGELOG.md),
[metacognition](plugins/tino/skills/metacognition/CHANGELOG.md) and
[brain](plugins/tino/skills/brain/CHANGELOG.md).

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
  lessons and the wiki live in the project.
- The rituals and installers check what they write, piece by piece:
  figures from their source, quotations verbatim, and no claim more
  certain than its evidence.
- A ritual that cannot be installed as a skill goes to `rituals/<name>.md`,
  read on demand, instead of the instructions file.
- A test bench (`tests/test_suite.py`) and an eval suite
  (`plugins/tino/evals/`).

## 1.x — July to September 2026

Private releases in Spanish, used in the author's own projects. Upgrading a
1.x project to 2.0 keeps its Spanish file names; see each skill's changelog.
