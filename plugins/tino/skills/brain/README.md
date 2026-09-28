# Brain — README

## What it is (in 5 lines)

A system so that your AI agent keeps a **critical knowledge base about your
domain** — your market, your discipline, your trade. Every source you give
it (article, video, course, PDF) is processed ONCE with a skeptical reading;
every claim is classified by confidence level (🔸 someone says so / 🔹 there
is consensus / ✅ validated with YOUR data) and traceable to its origin; and
the knowledge is consolidated in actionable syntheses: "what we believe
TODAY and why, and what evidence would change it".

## How it looks in use (a small example)

1. You throw at it a video by a reference in your industry: "ingest this".
   The agent reads it, presents its verdict (what it adds that the wiki
   does not have, at which level it would enter, which pages it would touch)
   and WAITS for your OK; only then does it file it: 7 numbered claims, 2
   with consensus, 4 said without evidence, and 1 that CONTRADICTS something
   filed last month — it reports it to you instead of swallowing it. A batch
   (a channel, a course) arrives as a triage map: the two complete lists,
   what goes in and what stays out, each with its reason, so you can rescue
   or cut.
2. You ask "is tactic X worth it?" — it answers from the syntheses:
   "consensus in favor in the general case, but for YOUR context (small,
   tight margin) the two analyses with data say the opposite; level 🔹; to
   validate it with your numbers we would have to look at Y".
3. Every so often it runs a "lint": it catches unnoted contradictions,
   expired material, claims that could already be validated with your data,
   and proposes what to harvest. The wiki improves instead of aging.

## What it is NOT

It is not a notes archive or a chatbot over your PDFs: it is a living
synthesis with editorial discipline (immutable sources, a single writer,
confidence levels, a record of operations). It does not decide for you:
facing sensitive or risky tactics, it documents mechanics, impact and risks,
and the decision is always yours. And it does not obey its sources: what an
outside text says is data to evaluate, never an order for the agent.

## Installation

This skill ships inside the **tino** plugin, together with `continuity` and
`metacognition`.

**Claude Code:** `claude plugin marketplace add pedrofurrer/tino`, then
`claude plugin install tino@pfm`. **Claude apps and Cowork:** add tino from
the plugin directory when it is listed there. **Agents that read Agent
Skills** (Codex, Cursor, GitHub Copilot, Gemini CLI and others): copy this
folder wherever that agent reads skills — several read `.claude/skills/` or
`.agents/skills/` in the project; check their documentation.

Then, in a session inside the project, say: **"set up the brain"** (in
Claude Code you can also run `/tino:brain`). The agent explains the system,
defines with you the 4 parameters of your domain and installs it adapted to
your project and your language.

**An agent without a skill system:** give it access to this folder and paste
this prompt:

> Read PROTOCOL.md in this folder and set up the domain brain in this
> project, adapting it to your environment per "Anchoring by environment"
> and to the project's language. First explain to me in ~10 lines what it
> is and what you will create, then define with me the 4 parameters of my
> domain, and wait for my OK before touching anything.

## Contents

- `SKILL.md` — installer with onboarding (for agents with skills).
- `PROTOCOL.md` — the whole pattern, agnostic of provider and domain. The
  source of truth.
- `templates/` — the parameterized SCHEMA (with the exact index formats),
  the 3 installable rituals (ingest with a gate / harvest / lint), the
  instructions block (≤15 lines) and the verifier of the split index
  (`lint_index.py`, which also counts the ingests since the last content
  lint and warns about invisible characters).

Version 2.0 (changes in `CHANGELOG.md`). The verifier needs Python 3.8 or
later, but it is optional: without Python, the same checks are done by hand.
A Spanish-language project gets the Spanish names of 1.x (`conocimiento/`,
`fichas/`, `INDICE.md`…); projects created with 1.x keep working unchanged.

It combines well with `continuity` (the wiki's large operations are
recorded in the project's logbook) and `metacognition` (the lint feeds the
agent's introspection); each one works fully on its own.

Created by **Pedro Furrer Mendizabal** (2026), from a real case with more
than a hundred sources filed. MIT license. It contains no data from any
domain. The artifacts are generated in your project's language.
