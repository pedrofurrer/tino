# Metacognition — README

## What it is (in 5 lines)

A system so that your AI agent **improves its judgment with use**. Every
time you correct it — or the data contradict it, or reality shows it a
better strategy — the agent distills the underlying *way of thinking* into
a "judgment lesson": **trigger** (when it fires) → **principle** (how to
think). The lessons stay in the agent's view in every session (their index
lives in the project's instructions), they are cited when applied, and a
periodic introspection consolidates them, measures how often each one
recurs (recurrences over uses) and prunes the ones that do not help.

## How it looks in use (a small example)

1. Your agent proposes asking a platform's support desk to approve a change
   "because it is due" (an argument on merit). You point out that it is
   better to ask for the minimal technical correction, which invites nobody
   to judge merit. **A correction with a pattern, detected.**
2. The agent proposes the lesson: *"Trigger: a request to a third party with
   a discretionary veto → Principle: ask for the minimal technical
   operation, not the strategic outcome that invites their judgment."* You
   approve it (or correct it, or discard it).
3. Weeks later, facing a similar procedure, the agent drafts the technical
   request directly and tells you: "Judgment applied:
   lesson-minimal-technical-request". That — not repeating the error, and
   being able to verify it — is the whole system.

## What it is NOT

It does not modify the model or "train" anything: LLM agents do not learn
between sessions. It is context engineering + rituals: capture → distill →
keep in view → apply → measure. Honest and verifiable; no magic. And it does
not take your word as revealed truth: every lesson declares what it rests
on, and one that rests only on your correction is not considered confirmed
until data or an outcome back it.

## Installation

This skill ships inside the **tino** plugin, together with `continuity` and
`brain`.

**Claude Code:** `claude plugin marketplace add pedrofurrer/tino`, then
`claude plugin install tino@pfm`. **Claude apps and Cowork:** add tino from
the plugin directory when it is listed there. **Agents that read Agent
Skills** (Codex, Cursor, GitHub Copilot, Gemini CLI and others): copy this
folder wherever that agent reads skills — several read `.claude/skills/` or
`.agents/skills/` in the project; check their documentation. The system
needs a project folder that persists between conversations.

Then, in a session inside the project, say: **"set up metacognition"** (in
Claude Code you can also run `/tino:metacognition`). The agent explains the
system, asks you 3 configuration questions (with sensible defaults) and
installs it adapted to your project and your language.

**An agent without a skill system:** give it access to this folder and paste
this prompt:

> Read PROTOCOL.md in this folder and set up the metacognition system in
> this project, adapting it to your environment per its "Anchoring by
> environment" section and to the project's language. First explain to me
> in ~10 lines what it is and what you will create, and wait for my OK
> before touching anything.

## Contents

- `SKILL.md` — installer with onboarding (for agents with a skill system).
- `PROTOCOL.md` — the whole system, provider-agnostic. The source of truth.
- `templates/` — the lesson format (`TEMPLATE-lesson.md`), an anonymized
  example, the instructions block (≤15 lines, with the index below it), the
  installable introspection ritual and the lessons and index verifier
  (`lint_lessons.py`, with `--summary` for the incremental introspection and
  the recurrence rate).

Version 2.0 (changes in `CHANGELOG.md`). The verifier needs Python 3.8 or
later, but it is optional: without Python, the same checks are done by hand.
A Spanish-language project gets the Spanish names of 1.x (`criterio/`,
`leccion-*.md`…); projects created with 1.x keep working unchanged.

It combines well with `continuity` (the judgment retro in the closing
ritual) and with `brain` (the wiki's lint feeds the introspection). Each one
works fully on its own.

Created by **Pedro Furrer Mendizabal** (2026), from a real case of
agent-user work. MIT license. It contains no data from any business. The
artifacts are generated in your project's language.
