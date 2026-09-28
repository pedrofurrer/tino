# BITÁCORA — Panadería Los Robles

> Registro cronológico append-only: QUÉ se hizo/decidió + POR QUÉ + qué NO hacer. Nunca se edita ni se borra una entrada; las reversiones son entradas nuevas.
>
> **Índice de rotaciones** — rotación del **2026-09-26** (v1.4 al archivo **:6**; herederos en el marcador)

## 2026-09-26 — Instalación del sistema de metacognición (v1.4)
- Qué: `criterio/` con índice (`criterio/INDICE.md`, sección «Criterio del agente» primero + línea FIN), verificador `scripts/lint_criterio.py`, bloque en CLAUDE.md, ritual `introspeccion`; el ritual de cierre ya incluía la retro de criterio (paso 4), ahora activa.
- Por qué (config elegida): lecciones en el repo y no en la memoria del agente, para que viajen con el proyecto y se restauren en otra máquina; tres disparadores de introspección; captura siempre propuesta antes de fichar.
- Qué NO hacer: no fichar hechos («tal dato era X») como lecciones; sin gatillo ex-ante, va a esta bitácora.

## 2026-09-26 — Fundación del cerebro (wiki crítica) v1.4
- Qué: `conocimiento/` con portada + 4 sub-índices + INDICE-fuentes, ESQUEMA con los 4 parámetros, LOG, PENDIENTES, verificador `scripts/lint_indice.py`, skills `ingerir-fuente`/`cosechar`/`lint-wiki`, bloque en CLAUDE.md.
- Por qué (parámetros): subdominios masas-y-fermentacion / horneado / costos-y-precios / venta-y-clientela; fuente de validación = CSV de ventas + cuaderno de horneadas (laguna: en papel); vigencia técnica 5 años, precios 12 meses; contexto = panadería de barrio, 2 personas, horno de leña. Sin capa `mercado/` por ahora.
- Qué NO hacer: nada se ficha sin OK del usuario; `fuentes/` no se edita; LOG solo se agrega.

## 2026-09-26 01:10 — Cierre de la sesión de instalación y primeras corridas
- Qué: instalados los tres sistemas; primera lección de criterio (promedio ponderado, hipótesis); primera ingesta con compuerta (hidratación 80 %); primer lint de la wiki.
- Por qué se ordenó así: continuidad primero (sustrato), metacognición después, cerebro al final (sus parámetros salen mejor con el proyecto rodado).
- Qué NO hacer: no promediar precios sin ponderar (lección `leccion-promedio-ponderado`).
