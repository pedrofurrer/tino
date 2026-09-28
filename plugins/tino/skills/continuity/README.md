# Continuity — README

## What it is (in 5 lines)

A system so that your AI agent **does not lose the thread between
sessions**. Without it, every new session re-explores what was already
known, overwrites earlier work or drops half-finished plans. With it,
everything relevant lives in project documents that the agent reads before
acting and updates when closing: a roadmap with the exact point where each
thing was left, a logbook of decisions with their why, and a map of the
system with its untouchable rules.

## How it looks in use (a small example)

1. Monday: you work for 3 hours with your agent on a migration. When
   closing, the agent runs the "save progress" ritual: the roadmap says
   "where we left off: the users table is still to migrate; next step: the
   backfill script", and the logbook records why strategy B was chosen (and
   why NOT strategy A).
2. Thursday: you open a new session. Before touching anything, the agent
   reads the documents — its rules require it, you do not have to ask — and
   resumes from the exact point; and when it proposes something that
   contradicts Monday's decision, the logbook stops it: it alerts you before
   overwriting what was decided.
3. A month later: "why had we ruled out strategy A?" — the answer is
   written down, with its date and context.

## What it is NOT

It is not heavy documentation or bureaucracy: the documents have size
budgets (they are compacted by archiving, never by deleting) and the rules
block the agent loads in every session is at most 20 lines. It is the
minimum structure that turns loose sessions into one continuous project.

## Installation

This skill ships inside the **tino** plugin, together with `metacognition`
and `brain`.

**Claude Code:** add the marketplace and install the plugin:
`claude plugin marketplace add pedrofurrer/tino`, then
`claude plugin install tino@pfm`. **Claude apps and Cowork:** add tino from
the plugin directory when it is listed there. **Agents that read Agent
Skills** (Codex, Cursor, GitHub Copilot, Gemini CLI and others): copy this
folder wherever that agent reads skills — several read `.claude/skills/` or
`.agents/skills/` in the project; check their documentation. The system
needs a project folder that persists between conversations: in a one-off
chat, whatever is written does not survive.

Then, in a session inside the project, say: **"set up continuity"** (in
Claude Code you can also run `/tino:continuity`). The agent explains the
system, diagnoses your project, adapts the scale and seeds the documents with
your real history — in your language.

**An agent without a skill system:** give it access to this folder and paste
this prompt:

> Read PROTOCOL.md in this folder and set up the continuity system in this
> project, adapting it to your environment per its "Anchoring by
> environment" section and to the project's language. First explain to me
> in ~10 lines what it is and what you will create, and wait for my OK
> before touching anything.

## Contents

- `SKILL.md` — installer with onboarding (for agents with a skill system).
- `PROTOCOL.md` — the whole system (4 layers), provider-agnostic. The source
  of truth.
- `templates/` — the installable closing ritual, the instructions block
  (≤20 lines), the budgets verifier (`lint_continuity.py`, with `--margin`
  to measure before writing) and the logbook rotator (`rotate_logbook.py`:
  nothing is deleted, it moves to the archive).

Version 2.0 (changes in `CHANGELOG.md`). The scripts need Python 3.8 or
later, but they are optional: without Python, the same checks are done by
hand. A Spanish-language project gets the Spanish names of 1.x (`BITACORA.md`,
`ARQUITECTURA.md`…); projects created with 1.x keep working unchanged.

It combines well with `metacognition` (the closing ritual adds the judgment
retro) and with `brain` (large wiki operations are recorded in the
logbook). Each one works fully on its own.

Created by **Pedro Furrer Mendizabal** (2026), from a real case of
agent-user work. MIT license. It contains no data from any project. The
artifacts are generated in your project's language.
