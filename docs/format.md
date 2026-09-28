# File formats and fixed tokens

tino writes plain Markdown into your project. The prose is written in your
project's language. A small set of names and markers is read by the verifier
scripts, so it stays fixed. Those tokens exist in two sets:

- **English**, used for every language except Spanish.
- **Spanish**, the set that 1.x projects use. The installers also write it
  for Spanish-language projects.

The scripts accept both sets, in any mix. A project created with 1.x keeps
working without changes.

Version markers are HTML comments. They are invisible when rendered and are
always written in English.

## Version markers

| Purpose | Written by 2.x | Also accepted |
|---|---|---|
| Block marker, last line of each block | `<!-- tino: continuity v2.0 -->` · `metacognition` · `brain` | `<!-- suite-agentica: continuidad v1.5 -->` · `metacognicion` · `cerebro` |
| Oldest projects | — | `Sistema: continuidad v1.3` (reported as legacy) |

## Continuity

| Item | English | Spanish |
|---|---|---|
| Plan | `PLAN.md` | `PLAN.md` |
| Logbook, append-only | `LOGBOOK.md` | `BITACORA.md` |
| Logbook archive | `LOGBOOK-archive.md` | `BITACORA-archivo.md` |
| Architecture | `ARCHITECTURE.md` | `ARQUITECTURA.md` |
| Invariants heading | `## INVARIANTS` | `## INVARIANTES` |
| Budgets line, in PLAN.md | `<!-- lint-budgets: … -->` | `<!-- lint-topes: … -->` |
| Budget keys | `PLAN` · `ARCHITECTURE` · `LOGBOOK` · `INSTRUCTIONS` · `BLOCK` · `INSTRUCTIONS=<file>` · `DOCS` | `ARQUITECTURA` · `BITACORA` · `INSTRUCCIONES` · `BLOQUE` · `INSTRUCCIONES=<file>` |
| Resume phrase | `where we left off:` | `quedamos en:` |
| Rotation index, in the logbook header | `> **Rotation index** — …` | `> **Índice de rotaciones** — …` |

**Budgets line.** Each segment reads `<DOC> alarm/cap alarmKB/capKB`, with
lines first and then KB (1 KB = 1000 bytes). `BLOCK n` caps the continuity
block and `BLOCK <component> n` caps the other blocks. `DOCS PLAN` declares
the minimal scale. For example:

```
<!-- lint-budgets: PLAN 120/150 14.4/18 | ARCHITECTURE 160/200 24/30 | LOGBOOK 160/200 20/25 | INSTRUCTIONS 200/300 12/20 | BLOCK 20 -->
```

**Logbook entries.** Each entry starts with `## YYYY-MM-DD — <topic>`;
`## [YYYY-MM-DD] …` also works. The rotator uses that date. Sections without
a date never rotate.

**Plan states.** The states are ✅ done · 🔄 in progress · ⏳ pending ·
💡 idea. The legend line carries `<!-- tino:legend -->`. The Spanish legend
text "✅ hecho … 🔄 en curso" is also recognized, so it is never mistaken for
a task.

## Metacognition

| Item | English | Spanish |
|---|---|---|
| Lessons folder | `lessons/` | `criterio/` |
| Lesson file | `lesson-<slug>.md` | `leccion-<slug>.md` |
| `metadata.type` | `lesson` | `leccion` |
| `metadata.validation` | `proposed` · `hypothesis` · `recurring` · `confirmed` · `graduated` · `archived` · `example` | `validacion`: `propuesta` · `hipotesis` · `recurrente` · `confirmada` · `graduada` · `archivada` · `ejemplo` |
| `metadata.scope` | `<project>` · `cross-project` | `ambito`: `<proyecto>` · `transversal` |
| `metadata.evidence` | `data` · `source` · `reality` · `user` | `evidencia`: `dato` · `fuente` · `realidad` · `usuario` |
| `metadata.carried_to` | the instrument that enforces it | `heredero` |
| Body sections, bold labels | **Trigger** · **Original error** · **Principle** · **Application** · **Cases** | **Gatillo** · **Error original** · **Principio** · **Aplicación** · **Casos** |
| Case line | `- YYYY-MM-DD · origin\|applied\|recurrence — …` | `origen\|aplicada\|reincidencia` |
| Index heading, which contains one of these | `Agent judgment` · `Lesson index` | `Criterio del agente` · `Índice de lecciones` |
| Index entry | `- lesson-<slug> — <trigger → principle>` | `- leccion-<slug> — …` |
| Index closing line | `END OF LESSON INDEX — N entries` | `FIN DEL ÍNDICE DE CRITERIO — N entradas` |

## Brain

| Item | English | Spanish |
|---|---|---|
| Wiki folder | `knowledge/` | `conocimiento/` |
| Schema | `SCHEMA.md` | `ESQUEMA.md` |
| Front page | `INDEX.md` | `INDICE.md` |
| Sub-index | `INDEX-<subdomain>.md` · `INDEX-sources.md` | `INDICE-<subdominio>.md` · `INDICE-fuentes.md` |
| Pending queue | `PENDING.md` · `PENDING-archive.md` | `PENDIENTES.md` · `PENDIENTES-archivo.md` |
| Log, append-only | `LOG.md` | `LOG.md` |
| Raw sources, immutable | `sources/` | `fuentes/` |
| Inbox | `sources/clips/` | `fuentes/clips/` |
| One card per source | `cards/` | `fichas/` |
| Concepts | `concepts/` | `conceptos/` |
| Syntheses | `syntheses/` | `sintesis/` |
| Perishable, dated snapshots | `landscape/` | `mercado/` |
| Sub-index header | `> Entries: N.` | `> Entradas: N.` |
| Sub-index footer, last non-empty line | `END OF SUB-INDEX · <subdomain> — N entries` | `FIN DEL SUB-ÍNDICE · … — N entradas` |
| Front page footer | `END OF INDEX (front page) — N sub-indexes` | `FIN DEL ÍNDICE (portada) — N sub-índices` |
| LOG operations | `founding` · `ingest` · `harvest` · `query` · `lint` · `schema` · `correction` · `triage` | `fundacion` · `ingesta` · `cosecha` · `consulta` · `esquema` · `correccion` · `triaje` |
| Card fields | `type` · `title` · `source` · `author` · `url` · `source_date` · `ingested` · `topics` · `confidence` · `validity` | `tipo` · `titulo` · `fuente` · `autor` · `url` · `fecha_fuente` · `fecha_ingesta` · `temas` · `confianza` · `vigencia` |
| Confidence levels | 🔸 `dixit` · 🔹 `consensus` · ✅ `validated` | `dixit` · `consenso` · `validado` |
| Validity | `current` · `doubtful` · `obsolete` | `vigente` · `dudosa` · `obsoleta` |
| Triage verdicts | `file` · `do not file` · `doubtful` · `discard` | `fichar` · `no fichar` · `dudoso` · `descartar` |
| Invisible characters already reviewed, noted in the card | `invisible characters: reviewed` | `caracteres invisibles: revisados` |

**Index entries.** Each entry reads `- [[folder/slug]] — one line`, and
also accepts `[[folder/slug|alias]]` and `[[folder/slug#section]]`.

**LOG entries.** Each entry reads `## [YYYY-MM-DD] operation | Title`.
Operations are case-insensitive.

## Scripts installed into your project

The Spanish set also keeps the 1.x file names. Upgrading a 1.x project
therefore replaces each script's content under the same name, and the
commands and hooks that point to it keep working.

| English set | Spanish set (1.x) | Spanish flags still accepted |
|---|---|---|
| `lint_continuity.py` | `lint_continuidad.py` | `--margen` · `--retomar` · `--raiz` |
| `rotate_logbook.py` | `rotar_bitacora.py` | `--bitacora` · `--archivo` · `--hasta` · `--ejecutar` · `--herederos` |
| `lint_lessons.py` | `lint_criterio.py` | `--indice` · `--tope` · `--posicion-max` · `--lineas-max` · `--resumen` |
| `lint_index.py` | `lint_indice.py` | `--guardia` |

## Rituals installed into your project

| English set | Spanish set (1.x) |
|---|---|
| `save-progress` | `guardar-avance` |
| `introspect` | `introspeccion` |
| `ingest-source` | `ingerir-fuente` |
| `harvest` | `cosechar` |
| `lint-brain` | `lint-cerebro` (the 1.x templates called it `lint-wiki`) |

Where a project skill cannot be written (no skill system, or the write into
`.claude/` is denied), the same file goes to `rituals/<name>.md` in the
English set and `rituales/<name>.md` in the Spanish set, read on demand.
