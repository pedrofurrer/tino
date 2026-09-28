# CHANGELOG — continuity

Author: Pedro Furrer Mendizabal. Each version lists ONLY the changes that
affect a project that has the system installed, and ends with its
**Upgrade** list: what the installer applies, in order, when it brings a
project from an earlier version (step 0). The block text and the ritual are
replaced once, by the current version's. The project's documents are never
overwritten.

## v2.0 — 2026-09-28
- Published in English as part of the tino plugin (Claude Code and Cowork)
  and as a standalone Agent Skill. English is now the source language; the
  artifacts are still written in the project's language.
- Two token sets (PROTOCOL §Fixed tokens): English, and the Spanish set of
  1.x, which the installer also writes for Spanish-language projects. The
  verifier accepts both, in any mix.
- Scripts in the English set: `lint_continuity.py` and `rotate_logbook.py`,
  with English messages; the 1.x flags keep working as aliases (`--margen`,
  `--retomar`, `--raiz`, `--hasta`, `--ejecutar`, `--herederos`).
- Budgets line `<!-- lint-budgets: … -->` (the 1.x `lint-topes` is still
  accepted); keys `ARCHITECTURE`, `LOGBOOK`, `INSTRUCTIONS`, `BLOCK`
  (the Spanish keys are still accepted).
- Fixes: `--resume` recognizes the states legend by its marker
  (`<!-- tino:legend -->`) or its text, so a task line that mixes ✅ and 🔄
  is no longer dropped; two blocks that share one heading are measured once;
  `--until` requires exactly `YYYY-MM-DD` (from Python 3.11 on, other ISO
  forms passed and chose every entry).
- The installer no longer writes permission rules or hooks into the
  project's settings; the optional guardrails for Claude Code are documented
  separately.
- The installer and the closing ritual take every figure, date and
  quotation from its source and write what only the user said as the
  user's word; a reconstructed logbook entry states only what was known on
  its date, and statements a session made stale are corrected in the same
  pass.
- The closing ritual no longer updates the agent's own memory: what matters
  goes to the project's documents.
- Ritual fallback: where the environment has no skills or the write into
  `.claude/` is denied (Claude Code asks before writing there), the ritual
  goes to `rituals/save-progress.md` (Spanish set: `rituales/`), read on
  demand and pointed to by the block, instead of a section of the
  instructions, which is paid in every session.
- **Upgrade** (from any 1.x version): (a) keep the project's token set — a 1.x
  project keeps its Spanish names (documents, headings, ritual and script file
  names); nothing is renamed; (b) replace the CONTENT of the installed scripts
  with `templates/lint_continuity.py` and `templates/rotate_logbook.py`,
  keeping their file names, and run the verifier; (c) if PLAN has no budgets
  line, ADD the `lint-budgets` line (a `lint-topes` line stays as it is; if it
  says `PLAN 120/150 14/18`, propose `14.4/18`, the exact 80 % alarm); minimal
  scale: `| DOCS PLAN`; (d) replace the block text with the current template,
  in the project's language (semantic diff, with OK); a visible "Sistema:
  continuidad vX.Y" line gives way to the HTML marker; (e) replace the closing
  ritual with the current template (semantic diff, with OK), keeping its
  installed name; (f) guardrails that 1.5 wrote into the project's settings
  keep working (same script path; the old flags are aliases): leave them as
  they are; (g) optional: add `<!-- tino:legend -->` at the end of PLAN's
  states legend line; (h) if the instructions file exceeds its budget, propose
  the diet, do not apply it; (i) a ritual that 1.x left as a section of the
  instructions: propose moving it (with OK) to `.claude/skills/`, or to
  `rituals/` if that write is denied; (j) marker
  `<!-- tino: continuity v2.0 -->`.

## 1.x history (Spanish-only releases)
- **v1.5 — 2026-09-26**: upgrade repaired (marker first, footprints,
  cumulative Upgrade lists, block and ritual replaced); a shorter block; the
  rotator keeps undated sections and code blocks intact and leaves the rest
  of the file byte for byte; the verifier locates every block by its marker
  (so it works in any language), adds the minimal scale, `--retomar` and
  invisible-character warnings; optional mechanical controls for Claude
  Code; new principle: outside material comes in as data.
- **v1.4 — 2026-09-26**: budgets in lines AND bytes with a machine-readable
  line in PLAN; the verifier (`--margen`) and the rotator; "measure before
  writing"; staging file by file and concurrent sessions; budget of the whole
  instructions file; invariant HTML version marker (without a marker the
  installer asks, it does not assume 1.0).
- **v1.3 — 2026-09-02**: scope of instructions — what is specific to a
  project lives in its own instructions; global instructions take only
  generic rules.
- **v1.2 — 2026-07-18**: the author's credit added; no functional changes.
- **v1.1 — 2026-07-18**: the installed version is recorded in the project;
  upgrade mode in step 0.
- **v1.0 — 2026-07-18**: foundation — installer with onboarding,
  provider-agnostic protocol (4 layers), closing ritual and instructions
  block.
