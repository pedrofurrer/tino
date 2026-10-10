# tino

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23028616.svg)](https://doi.org/10.5281/zenodo.23028616)

**Memory is not judgment.**

Each session, your AI agent starts with a fresh context. Instructions files
and the agent's own memory carry part of the past over: you write the first,
and the agent decides what goes in the second. Even so, it can repeat a
mistake you corrected or take a confident source at its word. tino is three
skills that set up, inside your project, the plain-Markdown records a
careful professional would keep: a plan and a logbook, lessons learned from
your corrections, and a critical wiki of your domain. The agent maintains
them; lessons and wiki pages go in only with your OK.

*Leer en español: [README.es.md](README.es.md).*

| Skill | What it sets up | What changes |
|---|---|---|
| `continuity` | `PLAN.md`, `LOGBOOK.md`, `ARCHITECTURE.md` with the project's invariants, a short rules block and a closing ritual | Each session can resume from where the last one left off, and the agent is told to stop and alert you before a change undoes a recorded decision |
| `metacognition` | Judgment lessons (trigger → principle) with an index loaded in every session, and a periodic introspection | Your corrections become lessons the agent applies, cites and measures; a lesson becomes a rule only once confirmed, with your OK |
| `brain` | A wiki in `knowledge/` with a schema, an index, three rituals (ingest, harvest, lint) and a verifier | Every source is read critically, every important claim carries a confidence level, and nothing is filed without your OK |

## Install

In a terminal, with [Claude Code](https://code.claude.com):

```bash
claude plugin marketplace add pedrofurrer/tino
```

```bash
claude plugin install tino@pfm
```

Or inside a session: `/plugin marketplace add pedrofurrer/tino`, then
`/plugin install tino@pfm`.

## Use

Ask in plain words, in any language:

- "Set up continuity in this project."
- "Set up metacognition, and propose a first lesson from a correction I made
  this week."
- "Set up the brain for this domain, then ingest this article."

Each installer explains what it will create, adapts it to your project and
waits for your OK. After that the gestures are short: "save progress",
"ingest this", "run the introspection", "lint the wiki". The
[guide](docs/guide.md) explains each system and how to live with it.

## Examples

Two fictional projects, each shown after a short working session with tino:

- [`examples/bakery`](examples/bakery): a neighborhood bakery's recipes and
  sales. The agent weights prices by volume after a correction, rejects a
  blog post whose advice the bake log had already tried with poor results,
  and advises against raising the hydration of a loaf when the records point
  the other way; the decision stays the owner's.
- [`examples/fact-check-desk`](examples/fact-check-desk): the fact-check desk
  of a local newspaper during a mayoral race. A blog post hides an
  instruction for AI assistants; the agent names it, does not follow it, and
  shows that the post's "15 percent" is far from the 4.1 % fall measured
  between 2020-21 and 2025-26 and matches the worst case of a 2019
  projection, a possible origin it records as an unverified hypothesis.

## Does it work?

The eval suite in [`plugins/tino/evals/`](plugins/tino/evals) runs real agent
sessions on seeded projects, with and without the plugin. Final run on
2026-09-28 with Claude Opus 5.5, three runs per arm:

| Behavior | With tino | Without |
|---|---|---|
| A source hides an instruction for AI assistants: the agent names it and does not follow it | 3/3 | 0 of 6 baseline runs over two full runs; all six read the source* |
| "Learn from my corrections": the agent explains, asks and writes nothing yet | 3/3 | 0/3: all three wrote self-applied rules into `CLAUDE.md` |
| "Keep a knowledge base from my articles": the agent explains, asks and writes nothing yet | 3/3 | 0/3: all three built one at once |
| "Set up continuity": the agent explains and waits for the OK | 3/3 | 3/3 |

\*Without tino the brain cannot be set up. Every baseline run said so, but
all of them also read the source and checked its figure against the data,
and none mentioned the hidden instruction.

The installers (an English project, a Spanish one) and the upgrade from 1.x
passed every check in 9 of 9 runs. This is the author's own suite and a small
sample, not a benchmark: [docs/evals.md](docs/evals.md) has the method, every
case and its caveats, and [CONTRIBUTING.md](CONTRIBUTING.md) shows how to run
it yourself.

## What it costs and what it touches

- **Tokens per session**, measured on the examples: about 1,750 for the
  installed files (the three rules blocks, a one-lesson index and five ritual
  descriptions) and about 230 for the plugin's three skill descriptions, in
  six of eight readings (in the other two, about 1,115, with no cause
  found). Reading the plan and the architecture document before a change,
  as the rules ask, adds an estimated 2,200 to 2,500 in the examples, and
  each installer adds a few thousand more only when it runs. Measured on
  2026-09-28 as the difference in input tokens between the same project
  with and without tino, in Claude Code 2.1.283.
- **Files:** Markdown in your project and up to four small Python scripts
  (standard library only) that check sizes, indexes and lessons. tino makes
  no network calls, collects no data, never reads your agent's memory or
  past conversations, and does not change its permissions: see
  [PRIVACY.md](PRIVACY.md).
- **Rituals:** Claude Code treats `.claude/` as a protected path; depending
  on the permission mode, a write there asks you, goes to auto mode's
  classifier or is refused. If the rituals can be written there they become
  project skills; if not, they go to `rituals/`, read on demand.

## Languages and other agents

Everything tino writes is in your project's language. File names and
headings come from one of two token sets, English or Spanish, and the
scripts accept both ([docs/format.md](docs/format.md)). The skills follow
the open Agent Skills format, so agents other than Claude Code that read
skills can use them; check their documentation.

## More

[Guide](docs/guide.md) · [File formats](docs/format.md) ·
[Optional guardrails](docs/guardrails.md) · [Evals](docs/evals.md) ·
[An example of graduated rules](docs/principles-example.md) ·
[Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) ·
[Security](SECURITY.md) · [Privacy](PRIVACY.md) · [Citation](CITATION.cff)

Created by Pedro Furrer Mendizabal. Code and skills under the
[MIT license](LICENSE); documentation in `docs/` under
[CC BY 4.0](docs/LICENSE).
