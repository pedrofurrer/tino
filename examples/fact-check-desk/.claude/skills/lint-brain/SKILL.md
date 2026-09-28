---
name: lint-brain
description: Health check of the knowledge wiki: contradictions, validity, orphans and gaps. Use with «lint the wiki» or every ~10 ingests (the verifier counts them).
---

# Lint the wiki

Two planes: the **structural** one (step 2) — the mechanical part is done by
the verifier at the close of every ritual, and this lint adds the checks the
script cannot do —; the **content** one (steps 3-5) is the lint proper,
periodic — the verifier prints "ingests since the last lint: N" and warns
from ~10 on; a green verifier does not mean a healthy wiki.

## Checks

1. Read `knowledge/SCHEMA.md` + `INDEX.md` (front page) + ALL the
   sub-indexes `INDEX-*.md` (the lint is cross-cutting by definition; each
   one down to its END line) + the latest entries of `LOG.md`.
2. **Structural consistency**:
   - Run `python3 scripts/lint_index.py knowledge` (front page ↔ disk, counters, END lines, caps per
     file, page ↔ entry bijection; warnings about the inbox, a large PENDING
     and invisible characters) and fix what it reports.
   - By hand (the script does not see it): link orphans — pages without any
     incoming [[link]] — and concepts repeatedly mentioned as a [[link]]
     without a page of their own.
   - Inbox: whatever has been in `sources/clips/` for a while without a
     verdict → propose its ingest or its triage.
   - A sub-index over the ALARM (140 lines / 35 KB) → propose to the user a
     second-level split of that subdomain (SCHEMA §Rituals and scale) —
     never on your own.
3. **Content consistency**:
   - Contradictions between cards, concepts and syntheses that are not
     noted.
   - 🔸 dixit claims that could already be validated against the user's
     validation source → propose the check (that is what raises them to ✅).
   - Syntheses outdated with respect to newer cards that touch them.
   - Claims whose certainty grew on the way from a card to a concept, a
     synthesis, an index line or the LOG (a "matches" that became "comes
     from", a 🔸 that reads as ✅) → back to the source's certainty.
   - Quotations that differ from the raw source → verbatim again.
4. **Validity**: cards whose `source_date` is older than the SCHEMA's
   threshold on topics the field changes fast → are they still `current`,
   or do they become `doubtful`? Propose a spot check. If there is a
   perishable layer (`landscape/`): review its `data_date` in EVERY lint.
5. **Gaps**: questions of the domain without a synthesis that answers them;
   stalled topics in PENDING.
6. **Meta** (only if metacognition is installed): did the lint reveal an
   error pattern of the agent itself (filing without a level,
   over-validating, badly assigned subdomains)? → propose it as a signal for
   its introspection.

## Output

7. Mechanical fixes (index, broken links): apply them directly. Content
   changes (validity, contradictions, merges): present the list to the user
   and apply with their OK.
8. Update `PENDING.md` (gaps and harvest proposals) and `LOG.md`
   (`## [date] lint | summary`). If the lint changed the SCHEMA and the
   project has a logbook (continuity), an entry there too. Final report:
   overall health in 3-5 lines + which action would pay off most.
