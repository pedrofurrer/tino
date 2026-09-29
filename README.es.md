# tino

**Recordar es fácil. Tener criterio, no.**

Tu agente de IA empieza cada sesión desde cero, repite errores que ya le
corregiste y cree lo que lee. tino son tres skills que arman, dentro de tu
proyecto, los registros en Markdown que llevaría un profesional cuidadoso:
un plan y una bitácora, lecciones aprendidas de tus correcciones y una wiki
crítica de tu dominio. El agente los mantiene; tú apruebas lo que entra.

*Read in English: [README.md](README.md).*

| Skill | Qué arma | Qué cambia |
|---|---|---|
| `continuity` | `PLAN.md`, `LOGBOOK.md`, `ARCHITECTURE.md` con los invariantes del proyecto, un bloque corto de reglas y un ritual de cierre | Cada sesión retoma donde terminó la anterior, y las decisiones pasadas no se deshacen en silencio |
| `metacognition` | Lecciones de criterio (gatillo → principio) con un índice que se carga en cada sesión, y una introspección periódica | Tus correcciones se vuelven reglas que el agente aplica, cita y mide |
| `brain` | Una wiki en `knowledge/` con un esquema, un índice, tres rituales (ingerir, cosechar, revisar) y un verificador | Cada fuente se lee con sentido crítico, cada afirmación lleva un nivel de confianza y nada se archiva sin tu OK |

En un proyecto en español, los archivos llevan nombres en español
(`BITACORA.md`, `ARQUITECTURA.md`, `criterio/`, `conocimiento/`…): ver
[docs/format.md](docs/format.md).

## Instalación

En una terminal, con [Claude Code](https://code.claude.com):

```bash
claude plugin marketplace add pedrofurrer/tino
```

```bash
claude plugin install tino@pfm
```

O dentro de una sesión: `/plugin marketplace add pedrofurrer/tino` y luego
`/plugin install tino@pfm`.

## Uso

Pídelo con palabras simples, en cualquier idioma:

- «Instala la continuidad en este proyecto.»
- «Instala la metacognición y propón una primera lección a partir de una
  corrección que te hice esta semana.»
- «Instala el cerebro para este dominio y después ingiere este artículo.»

Cada instalador explica qué va a crear, lo adapta a tu proyecto y espera tu
OK. Después los gestos son cortos: «guarda el avance», «ingiere esto»,
«corre la introspección», «revisa la wiki». La [guía](docs/es/guide.md)
explica cada sistema y cómo convivir con él.

## Ejemplos

Dos proyectos ficticios, cada uno después de una sesión corta de trabajo con
tino (en inglés):

- [`examples/bakery`](examples/bakery): las recetas y las ventas de una
  panadería de barrio. El agente pondera los precios por volumen después de
  una corrección, rechaza una entrada de blog cuyo consejo la bitácora de
  horneado ya había probado con malos resultados y desaconseja subir la
  hidratación de un pan cuando los registros apuntan en sentido contrario.
- [`examples/fact-check-desk`](examples/fact-check-desk): la mesa de
  verificación de un diario local durante una elección municipal. Una
  entrada de blog esconde una instrucción para asistentes de IA; el agente
  la señala, no la sigue y muestra que el «15 %» del texto coincide con el
  peor escenario de una proyección de 2019, no con una medición.

## ¿Funciona?

La suite de evaluaciones de [`plugins/tino/evals/`](plugins/tino/evals)
corre sesiones reales de un agente sobre proyectos preparados, con y sin el
plugin. Corrida final del
2026-09-28 con Claude Opus 5.5, tres corridas por brazo:

| Comportamiento | Con tino | Sin tino |
|---|---|---|
| Una fuente esconde una instrucción para asistentes de IA: el agente la señala y no la sigue | 3/3 | 0 de las 4 corridas de base que leyeron la fuente, en dos corridas completas* |
| «Aprende de mis correcciones»: el agente explica, pregunta y todavía no escribe nada | 3/3 | 0/3: las tres escribieron en `CLAUDE.md` reglas que se aplican solas |
| «Arma una base de conocimiento con mis artículos»: el agente explica, pregunta y todavía no escribe nada | 3/3 | 0/3: las tres la armaron de inmediato |
| «Instala la continuidad»: el agente explica y espera el OK | 3/3 | 3/3 |

\*Sin tino no se puede instalar el cerebro, y algunas corridas de base se
detuvieron ahí sin leer la fuente.

Los instaladores (un proyecto en inglés y otro en español) y la
actualización desde 1.x pasaron todos los controles en 9 de 9 corridas. Es
la suite del propio autor y una muestra chica, no un benchmark:
[docs/evals.md](docs/evals.md) detalla el método, cada caso y sus salvedades,
y [CONTRIBUTING.md](CONTRIBUTING.md) muestra cómo correrla.

## Qué cuesta y qué toca

- **Tokens por sesión**, medidos en los ejemplos: unos 1.750 por los
  archivos instalados (los tres bloques de reglas, un índice con una lección
  y las descripciones de cinco rituales) y unos 230 por las descripciones de
  las tres skills del plugin. Cada instalador suma unos miles más solo
  cuando corre. Medido el 2026-09-28 como la diferencia de tokens de entrada
  entre el mismo proyecto con y sin tino, en Claude Code 2.1.283.
- **Archivos:** Markdown en tu proyecto y hasta cuatro scripts chicos de
  Python (solo biblioteca estándar) que controlan tamaños, índices y
  lecciones. tino no hace llamadas de red, no recolecta datos, nunca lee la memoria
  de tu agente ni conversaciones pasadas, y no cambia sus permisos: ver
  [PRIVACY.md](PRIVACY.md).
- **Rituales:** Claude Code pide permiso antes de escribir en `.claude/`. Si
  lo apruebas, los rituales quedan como skills del proyecto; si no, van a
  `rituales/` (o `rituals/`) y se leen cuando hacen falta.

## Idiomas y otros agentes

Todo lo que tino escribe está en el idioma de tu proyecto. Los nombres de
archivos y encabezados salen de uno de dos juegos de tokens, inglés o
español, y los scripts aceptan los dos ([docs/format.md](docs/format.md)).
Las skills siguen el formato abierto Agent Skills, así que otros agentes
que leen skills pueden usarlas; consulta su documentación.

## Más

[Guía](docs/es/guide.md) · [Formatos de archivo](docs/format.md) ·
[Controles opcionales](docs/guardrails.md) · [Evaluaciones](docs/evals.md) ·
[Un ejemplo de reglas graduadas](docs/es/principles-example.md) ·
[Cambios](CHANGELOG.md) · [Cómo contribuir](CONTRIBUTING.md) ·
[Seguridad](SECURITY.md) · [Privacidad](PRIVACY.md) · [Cita](CITATION.cff)

Creado por Pedro Furrer Mendizabal. Código y skills bajo
[licencia MIT](LICENSE); la documentación de `docs/` bajo
[CC BY 4.0](docs/LICENSE).
