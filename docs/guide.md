# tino — guide

*Leer en español: [es/guide.md](es/guide.md).*

tino gives an AI agent three habits that careful professionals already have:
keeping a record of the work, learning from corrections, and reading sources
critically. Each habit is a system of plain Markdown files inside your
project, set up by an installer skill and kept up by the agent. You approve
what goes in.

- [The idea](#the-idea)
- [Getting started](#getting-started)
- [Continuity](#continuity)
- [Metacognition](#metacognition)
- [Brain](#brain)
- [Day to day](#day-to-day)
- [Limits](#limits)
- [Upgrading from 1.x](#upgrading-from-1x)
- [Questions](#questions)

## The idea

- **Everything that matters lives in files you can read.** No database, no
  service, no hidden memory: a plan, a logbook, lesson cards, wiki pages.
  They travel with the project and its version control.
- **The agent maintains them; you decide what enters.** Lessons and wiki
  pages are proposed first and written only with your OK.
- **Instructions are paid in every session.** The rules the agent must see
  every time are kept to short blocks (at most 20, 15 and 15 lines), and
  everything else is read on demand. Four small scripts measure sizes and
  check indexes, so the files do not grow without anyone noticing.
- **Outside material is data, never an instruction.** A web page, an email
  or someone else's document can inform the work, but an order addressed to
  the agent inside it is reported to you, not obeyed.

The three systems work alone or together. When more than one is installed,
each detects the others and links up: the closing ritual includes the
judgment retro, and large wiki operations are recorded in the logbook.

## Getting started

Install the plugin once (see the [README](../README.md#install)), then, in
each project, ask for the system you want: "set up continuity", "set up
metacognition", "set up the brain". If you want all three, the usual order
is continuity first, because the others record their decisions in its
logbook, then metacognition, and the brain last, when its domain parameters
are clear.

Each installer:

1. reads the project and explains in a few lines what it would create;
2. asks the questions it needs, each with a default;
3. waits for your OK, then writes the files, filled with the project's real
   state instead of empty templates;
4. runs its checker, and closes with a short report: what was created, what
   was adapted and why, and the two or three gestures you will use.

In Claude Code, writing the rituals into `.claude/skills/` asks for your
permission. If you decline, they go to `rituals/` and the rules block points
to them there; you can move them later.

Removing the plugin does not remove anything from your projects: the files
are yours and keep working as plain documents.

## Continuity

Sessions are ephemeral: what was decided disappears when a session closes,
and the next one re-explores, overwrites or breaks what the previous one
knew. Continuity fixes that with one rule: everything relevant lives in
project files, and the agent must read them before acting and update them
when closing.

It has four layers:

1. **Living documents** at the project root.
   - `PLAN.md`: the roadmap, with a "where we left off" section at the top
     and task states (✅ done, 🔄 in progress, ⏳ pending, 💡 idea).
   - `LOGBOOK.md`: dated entries with decisions and their reasons. It is
     append-only: a reversal is a new entry, never an edit.
   - `ARCHITECTURE.md`: a map of the project and its numbered
     **INVARIANTS**, the rules that must not break without your OK.
2. **A rules block** in the agent's instructions file (`CLAUDE.md`,
   `AGENTS.md` or equivalent), at most 20 lines, that tells the agent to
   read those documents before changing anything and to stop and alert you
   if a change contradicts an invariant or a recorded decision.
3. **Version control**, if the project has it. The installer offers to start
   it, and checks what must not be committed.
4. **A closing ritual**, invoked with "save progress" or run after a
   milestone: it updates the three documents within their budgets, runs the
   checker and commits.

**Budgets.** Each document has a cap in lines and in kilobytes, with an alarm
at 80 %: PLAN 150 lines and 18 KB, ARCHITECTURE 200 and 30 KB, LOGBOOK 200
and 25 KB, the whole instructions file 300 lines and 20 KB. They live in one
line at the top of `PLAN.md`, so you can recalibrate them. The checker
(`scripts/lint_continuity.py`) reports every document and block against its
cap; with `--margin` it says how much still fits before writing.

**Rotation.** When the logbook fills up, `scripts/rotate_logbook.py` moves the
oldest entries, verbatim, into `LOGBOOK-archive.md`, under a marker that says
where their still-relevant parts now live. It shows a dry run first and
changes nothing until it runs with `--apply`.

**Scale.** A small or short project can use the minimal scale: PLAN, version
control and a short rule. The installer proposes the scale and records why.

## Metacognition

An agent does not learn between sessions. Automatic memory helps it remember
facts; metacognition makes it change how it thinks. The unit is a
**judgment lesson**: a card in `lessons/` with

- a **Trigger**: a situation recognizable before acting ("I am about to
  compare periods of a series…");
- the **Original error**, dated;
- a **Principle**: the rule, as an instruction;
- the **Application**: what doing it right looks like;
- the **Cases**: dated lines of origin, successful application and
  recurrence.

Each card declares its **validation** (`proposed` without your OK,
`hypothesis` with one case, `recurring`, `confirmed` once it has been applied
successfully, `graduated`, `archived`), its **evidence** (`data`, `source`,
`reality` or only the `user`'s word; a lesson resting only on your word does
not go beyond `recurring` until something corroborates it) and its
**scope**: this project, or `cross-project` when it speaks about method and
would apply unchanged elsewhere.

**Capture.** When you correct the agent and the correction shows a pattern,
or the data refute one of its predictions, it proposes a lesson in two or
three lines: trigger, principle and what it rests on. It writes the card only
with your OK. The closing ritual adds a retro step: lessons to propose, or an
explicit "no lessons".

**Application.** Proposing lessons is easy; applying them is where it is won
or lost, through four channels:

1. an **index** with one line per lesson, loaded in every session (by
   default, right below the rules block);
2. a **pre-delivery check**: before substantial work (a report, a plan, a
   text for third parties) the agent goes through the index and ends with
   "Judgment applied: <lesson>" when one fits, so you can see it being used;
3. **graduation**: a confirmed lesson with a frequent trigger can become a
   permanent rule of the project, or of your global instructions if it is
   cross-project, with your OK;
4. an **instrument**: when a lesson keeps failing at the same moment of the
   work, the fix is a check that fires at that moment (a script, a required
   field, a ritual step), not more text.

For an example of where graduated lessons can end up, see one user's
[hard rules](principles-example.md).

**Introspection** consolidates the lessons: weekly or with the project's
periodic review, when you ask, and at once after a rethink moment, such as a
refuted premise or a filed error that happens again. It measures how often
each lesson's error recurred, reformulates the ones that fail, and prunes the
index. tino does not read your agent's own
memory or past conversations: lessons come from corrections made in the
session, and they live in the project.

**Governance.** Lessons describe the agent's judgment. They never veto your
decisions or take away the ones that are yours.

## Brain

Sources pile up: articles, reports, notes, datasheets. The brain is a wiki of
your domain that the agent writes and keeps, in `knowledge/`, where every
claim carries a confidence level:

- 🔸 **dixit**: someone says so; no verifiable evidence;
- 🔹 **consensus**: several independent sources agree, or it is officially
  documented;
- ✅ **validated**: checked against your own data, the only level that
  supports a strong recommendation.

Pages also carry a **validity** (current, doubtful, obsolete), with the
source's date. Official or interested sources are trusted on how things work,
not on what suits you.

**Setting it up** means agreeing on four parameters: the domain and its three
to seven subdomains; the validation source (your data, your records); how
fast the field changes, which sets when material goes stale; and your
context, so every card asks whether advice fits your case.

**Layout.** `sources/` keeps the raw material, immutable, with an inbox at
`sources/clips/` for what you bring. `cards/` holds one critical reading per
source, `concepts/` one page per concept, `syntheses/` "what we believe today
and why" per topic. `INDEX.md` is a front page that points to one sub-index
per subdomain, each with a counter and a closing line, so the checker
(`scripts/lint_index.py`) can prove that the index and the pages on disk
match. `LOG.md` records every operation and `PENDING.md` the queue.

**Three rituals.**

- **Ingest a source** ("ingest this"): the agent reads it, checks it
  against what is filed and against your data, and presents a verdict (file,
  reject or doubtful) with the pages it would touch. Nothing is written until
  you say OK. A rejected source is logged with its reason, so it is not
  evaluated again from scratch. Sources you keep elsewhere in the project
  are copied, never moved.
- **Harvest a topic** ("harvest <topic>"): the agent defines two to four
  concrete questions, searches, filters by the source hierarchy and proposes
  what to file.
- **Lint the wiki** ("lint the wiki"): the checker runs at every ritual; a
  content review of contradictions, stale pages, orphans and gaps is
  proposed about every ten ingests.

**Sources are data.** The wiki reads outside material, including
instructions hidden in it for AI assistants. Those are reported and never
followed, and they lower the source's reliability.

## Day to day

| You say | What happens |
|---|---|
| "save progress" | The closing ritual: documents, checker, commit, a 3-5 line report |
| a correction | If it shows a pattern, a lesson proposal |
| "run the introspection" | Lessons reviewed, recurrence measured, index pruned |
| "ingest this" | A critical verdict on the source, then the filing on your OK |
| "harvest <topic>" | Directed search, then a proposal to file |
| "lint the wiki" | Structural and content review |

A few habits make it work better:

- **Correct with the reason.** "The average must weight by volume, because
  volumes change week to week" becomes a better lesson than "that's wrong".
- **Read what it proposes before saying OK.** The gate is only as good as
  the review.
- **Say no.** Rejecting a lesson or a source is recorded too, and it is
  useful.
- **Edit the files yourself when you want.** They are plain Markdown; run
  the checkers afterwards.

## Limits

- **It is instructions, not enforcement.** The rules block tells the agent
  what to do in every session; a model can still skip a step. The checkers
  catch structural drift, and the optional
  [guardrails for Claude Code](guardrails.md) add mechanical controls: a
  locked logbook archive, "where we left off" shown again on resume, and a
  guard on the wiki's raw sources.
- **It costs tokens.** In the examples, about 1,750 tokens per session for
  the installed files and about 230 for the plugin (measured on 2026-09-28).
- **The evidence is still thin.** The eval runs are encouraging
  and small: see [evals.md](evals.md).
- **The scripts need Python 3.8 or later.** Without Python the budgets are
  measured by hand, and the rituals say so.

## Upgrading from 1.x

The 1.x releases were private and in Spanish. Asking an installer to set up
its system in a project that already has it starts an upgrade: it keeps the
project's file names (a 1.x project keeps its Spanish names), replaces the
scripts' content and the rules block, keeps every entry of the history, and
shows each change for your OK. Each skill's `CHANGELOG.md` lists the exact
steps.

## Questions

**Does it replace my agent's memory?** No. Automatic memory remembers facts
about you; tino keeps the project's record, the lessons you approved and a critical wiki,
in files the project owns, and it does not read that memory.

**Does it work without Claude Code?** The skills follow the Agent Skills
format, and the files are plain Markdown, so agents that read skills or a
project instructions file can use them. The plugin and the optional
guardrails are specific to Claude Code.

**Is anything sent anywhere?** No. See [PRIVACY.md](../PRIVACY.md).

**Can I see a finished example?** Yes: [`examples/`](../examples).

**Where are the exact formats?** In [format.md](format.md). The fixed tokens
there are a contract that the scripts rely on.
