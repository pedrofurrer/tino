---
name: continuity
description: Sets up session continuity in a project (PLAN, LOGBOOK, ARCHITECTURE, rules and a closing ritual), adapted to it. Use with «set up continuity» or when a project will span several sessions.
compatibility: The templates/ scripts (verifier and rotator) need Python 3.8+; without Python, the ritual measures and rotates by hand (PROTOCOL §Operating principles).
metadata:
  author: Pedro Furrer Mendizabal
  version: "2.0"
---

# Continuity — installer of the 4-layer system

The whole system is in `PROTOCOL.md` (same folder as this skill): on a new
installation, read it in full BEFORE installing; for a review or an upgrade,
`CHANGELOG.md` and the sections the change touches are enough. The pieces to
seed are in `templates/`. Golden rules: adapt, do not copy blindly; seed with
the project's REAL state, never empty templates; and NEVER install before
explaining what it is and getting the user's OK.

## Procedure

### 0. Is it already installed? (review, upgrade or adoption; never reinstall from scratch)
Look FIRST for the marker in the project's instructions (e.g. `grep -ns
"tino: continuity\|suite-agentica: continuidad\|Sistema: continuidad"
CLAUDE.md AGENTS.md 2>/dev/null`): `<!-- tino: continuity vX.Y -->` (2.x),
`<!-- suite-agentica: continuidad vX.Y -->` (1.4-1.5) or the visible line
"Sistema: continuidad vX.Y" (1.1-1.3) give the installed version. No marker
but PLAN.md plus LOGBOOK.md or BITACORA.md (or equivalents): **ask** which
version it is; if the user does not know, infer it from footprints and
confirm — installed scripts state their version in their header; a block
that says "measure BEFORE writing" (or «medí ANTES de escribir») → 1.4 or
later; "where we left off" / «quedamos en» and an append-only logbook without
any of that → 1.0-1.3. A range is treated as its highest version.
ADOPTION is only for a foreign installation (similar documents that were not
born from this skill): compare piece by piece with the templates and propose
the diff, reinserting nothing. Review, upgrade or adoption end with the
current version's marker, a commit of their own and a logbook entry if the
project has one. With the version at hand, compare it with this skill's
(`CHANGELOG.md`):
- **Same version** → REVIEW (documents up to date? budgets respected?
  invariants current? ritual in use?).
- **Newer skill** → UPGRADE: show the CHANGELOG changes between both
  versions and apply, IN ORDER, the "Upgrade" list of every version after
  the installed one. The project's documents are never overwritten (at most
  a line is ADDED, like the budgets line); the instructions block text and
  the ritual are REPLACED once by the current templates, keeping local
  adaptations — the diff is semantic (what is installed may be translated or
  adapted): show it and apply with OK. The project keeps its token set (a
  1.x project keeps its Spanish names, PROTOCOL §Fixed tokens). The marker
  is updated last. If the verifier does not end green (typical: a long
  logbook measured in bytes for the first time), do NOT rotate or
  recalibrate on your own: present the options (rotate, with the user
  verifying where each live part went, or raise the cap in the budgets line
  recording why) and close the upgrade with the state declared (the commit
  and the logbook entry say so).

### 1. Onboarding FIRST (explain, then touch)
Explain to the user in ~10 lines, in their language:
- **What it is**: an agent's sessions are ephemeral; without a system, each
  one re-explores, overwrites earlier work or drops half-finished plans.
  This system makes everything relevant live in project artifacts that the
  agent's instructions REQUIRE it to read before acting and to update when
  closing.
- **The 4 layers**: living documents (PLAN = roadmap with "where we left
  off"; LOGBOOK = decisions with their why, append-only; ARCHITECTURE = map
  and invariants) + a rules block in the instructions + version control + a
  closing ritual, "save progress".
- **What will be created**: those documents seeded with the project's real
  history, the rules block, the ritual and two helper scripts.
Wait for an explicit OK before going on.

### 2. Project diagnosis (BEFORE creating anything)
Detect: type (code / data / writing / operations / mixed), size and expected
life, VCS already in place?, existing agent instructions (CLAUDE.md,
AGENTS.md or another)?, reusable earlier docs?, automations?, secrets or
sensitive data to keep out of the VCS?, working language (it decides the
token set: Spanish → the Spanish set; any other language → the English
set)? Summarize the diagnosis to the user in 3 lines.

### 3. Adapt the scale (with the user's OK if you depart from the standard)
- **Minimal** (small, short life): PLAN + VCS + a short block (item 1 with
  PLAN only, without item 3; the budgets line with the `DOCS PLAN` segment).
- **Standard**: the 4 layers in full.
- **Complete** (multi-module, automations, risk of breaking): 4 layers with
  rich INVARIANTS and a technical-debt section.
Adapt the content to the domain (in writing, ARCHITECTURE = style and
structure guide; in data, data dictionary and assumptions).

### 4. Installation (everything in the project's language)
- Create and SEED the living documents with the real state: known history
  (logbook entries in chronological order, each headed
  `## YYYY-MM-DD — <topic>`; the last one, the installation itself with the
  chosen adaptations and why), current state and next steps the user
  confirms. Every figure in them is computed from the project's files; what
  only the user said is recorded as their word; a rule taken from a project
  document keeps that document's scope; a reconstructed entry states only
  what was known on its date. Names and the invariants heading
  come from the token set (English: `PLAN.md`, `LOGBOOK.md`,
  `ARCHITECTURE.md`, `## INVARIANTS`;
  Spanish: `PLAN.md`, `BITACORA.md`, `ARQUITECTURA.md`, `## INVARIANTES`):
  the scripts read them, so they are not translated further.
- Leave the budgets line in PLAN, as is unless recalibrated with the user's
  OK (alarm = 80 % of the cap; KB = 1000 bytes; the full format is in the
  verifier's header), plus a periodic methodology-review item:
  `<!-- lint-budgets: PLAN 120/150 14.4/18 | ARCHITECTURE 160/200 24/30 | LOGBOOK 160/200 20/25 | INSTRUCTIONS 200/300 12/20 | BLOCK 20 -->`
  (minimal scale: add `| DOCS PLAN` before the closing `-->`). The keys are
  the same in both token sets.
- Insert `templates/instructions-block.md` into the PROJECT's agent
  instructions (create them if missing): translated, placeholders resolved
  (`<VERIFIER>` and `<ROTATOR>` are the FULL commands, e.g.
  `python3 scripts/lint_continuity.py`), without the header comment, with
  the document names of the token set and the HTML marker intact. At most 20
  lines from the heading to the marker: they are paid in every session. The
  user's global or personal instructions (if any) are not touched: they only
  take generic rules. If the file already exceeds ~200 lines or ~12 KB, say
  so: whatever is neither rule nor pointer belongs in documents read on
  demand (or in path-scoped rules, if the environment offers them).
- Install `templates/save-progress-SKILL.md` as a project skill in
  `.claude/skills/<name>/SKILL.md`, where `<name>` is `save-progress`
  (`guardar-avance` in the Spanish set) and equals the frontmatter `name`;
  other agents with skills read `.claude/skills/` or `.agents/skills/`
  (check their documentation). Commands resolved, header comment removed.
  Claude Code asks the user before writing inside `.claude/`: say so just
  before. If the environment has no skills or that write is denied, write
  the same file as `rituals/<name>.md` (Spanish set: `rituales/`), read on
  demand, and make `<RITUAL>` point to it; never paste the procedure into
  the instructions, which are paid in every session. Say so in the report:
  moving it into `.claude/skills/<name>/SKILL.md` later is a plain move. On
  an upgrade, an installed ritual is rewritten where it is; if that write is
  denied, say so and leave it: never a second copy.
- Install `templates/lint_continuity.py` and `templates/rotate_logbook.py`
  as project scripts (e.g. `scripts/`; in the Spanish set,
  `lint_continuidad.py` and `rotar_bitacora.py`) and run the verifier from
  the root: it must be green. Without Python: the budgets stay the same and
  the ritual notes that they are measured by hand (`wc -l`, `wc -c` or what
  the editor shows) before writing.
- Do not write permission rules or hooks into the project's settings. If
  the user works in Claude Code and wants mechanical guardrails (the logbook
  archive cannot be edited; "where we left off" re-shown on resume), point
  them to the optional guardrails in tino's documentation.
- VCS: if missing, propose starting one and do it only with the user's OK
  (there may be a parent repository or a synced folder); CHECK exclusions
  (secrets, heavy data, generated files) BEFORE the first commit. If this
  installer ended up copied into the project's `.claude/skills/`, ask
  whether it is versioned or ignored: it is not part of the installed system
  (it serves future reviews and upgrades). A descriptive initial commit.
- Integrations: metacognition installed → the closing ritual includes the
  judgment retro and the periodic review merges with its introspection;
  brain installed → the ritual checks its verifier and large wiki operations
  also go to the logbook.

### 5. Closing the onboarding (report + how it is used)
Report in ≤8 lines: what was created, with which scale and adaptations (and
why), the VCS state (no secrets: check the tracked files) and the 2 gestures
of use:
1. Before changing anything, the agent reads PLAN and ARCHITECTURE because
   the block requires it in every session — it is an instruction, not a
   mechanism: if it ever skips it, remind it.
2. When closing a milestone (or when the user says "save progress"), the
   agent runs the full ritual and confirms in 3-5 lines.
Close the report with this line (in the project's language): "Built with
tino, by Pedro Furrer Mendizabal."
