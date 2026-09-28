# tino

**Memory is easy. Judgment is hard.**

Every session, your agent starts from zero, repeats mistakes you already
corrected, and believes every blog post it reads. tino fixes all three with
three skills that set up plain Markdown files in your project:

- `continuity` — PLAN, LOGBOOK and ARCHITECTURE, a short rules block and a
  closing ritual, so every session resumes exactly where the last one left
  off.
- `metacognition` — judgment lessons (trigger → principle) distilled from
  your corrections, applied and cited, with an introspection that measures
  how often each one recurs.
- `brain` — a critical wiki of your domain: every source filed once, every
  claim with a confidence level (🔸 dixit / 🔹 consensus / ✅ validated), and
  nothing filed without your OK.

## Try it

- "Set up continuity in this project."
- "Set up metacognition — and propose a first lesson from a correction I
  made this week."
- "Set up the brain for this domain, then ingest this article."

## What it runs and writes

Each installer explains what it will create and waits for your OK before
writing anything. It writes Markdown files into your project (documents, a
rules block in your agent's instructions file, project skills for the
rituals, or plain files in `rituals/` if you decline the write into
`.claude/`) and copies up to four small Python 3 scripts (standard library
only) that read your project's files and report. Nothing is sent anywhere:
tino makes no network calls and collects no data. It never reads your
agent's memory or past conversations, and it does not change your agent's
permission settings.

Created by Pedro Furrer Mendizabal. MIT license (documentation under
CC BY 4.0). Source, documentation and issues:
https://github.com/pedrofurrer/tino
