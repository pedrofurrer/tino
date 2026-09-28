---
name: ingerir-fuente
description: Ingesta crítica de una fuente a la wiki de conocimiento del proyecto, con compuerta de OK del usuario (veredicto por pieza; mapa de triaje por lote). Usar cuando el usuario traiga un link, video, PDF, transcript o notas para incorporar ("ingerí esto", "procesá esta fuente", "fichá este video"), o pida procesar la bandeja de entrada (clips nuevos sin ficha).
---


# Ingerir fuente a la wiki

## Preparación (siempre)

1. Leé `conocimiento/ESQUEMA.md` (convenciones, formatos, niveles, reglas
   duras) y `conocimiento/INDICE.md` (la PORTADA: protocolo de lectura + mapa)
   más los sub-índices `INDICE-<subdominio>.md` de los subdominios que la
   fuente toca — si no está claro, TODOS. Un sub-índice sin su línea FIN
   vista NO está leído. Ahí se verifica qué existe ya.
2. Revisá la bandeja de entrada: material en `fuentes/clips/` sin ficha.
   Si lo hay, listalo y sumalo a la cola de esta ingesta (avisando).

## Triaje previo (material EN BLOQUE) — antes de tocar la wiki

Aplica cuando la fuente es un CONJUNTO: canal de video, curso, podcast,
carpeta de PDFs, lote de clips o cualquier lote de más de 3 piezas (y
siempre que el origen sea desconocido). Durante el triaje NO se escribe
nada en `conocimiento/`: el trabajo va a un espacio de borrador de la sesión.

A. **Declarar el filtro ANTES de aplicarlo**: con qué criterios se va a
   juzgar (fecha de corte y por qué, temas dentro/fuera del alcance,
   señales de calidad, aplicabilidad al contexto del usuario definido en
   el ESQUEMA). Es lo que hace auditable el veredicto.
B. **Inventario** de las piezas: título, fecha, extensión y de dónde sale
   cada metadato, sin abrirlas todavía. Capturar metadatos y transcripts
   en masa es barato cuando la plataforma los ofrece; la transcripción
   local cuesta tiempo real → avisar antes. Capturar el crudo NO es fichar.
C. **Muestreo crítico**: 2-3 piezas representativas (una vieja, una nueva,
   una del tema central) leídas de verdad → veredicto sobre la FUENTE:
   ¿mecánica verificable o venta?, ¿números o adjetivos?, ¿le habla al
   perfil del usuario o a otro? Si el transcript delata contenido visual
   clave, ir al punto exacto y capturarlo; el muestreo es dirigido, nunca
   consumir el material entero.
D. **Veredicto pieza por pieza**, en tabla: pieza | `fichar` /
   `descartar` / `dudoso` | motivo. Un DESCARTE se justifica en una línea
   («anterior al cambio X»; «ya cubierto por [[ficha-y]]»). Una INCLUSIÓN
   necesita tres cosas: qué aporta que la wiki NO tenga ya (verificado
   contra los sub-índices, no de memoria), con qué nivel entraría
   (🔸/🔹/✅ esperado) y qué páginas tocaría. La redundancia con lo ya
   fichado es motivo VÁLIDO de descarte.

## COMPUERTA — OK explícito del usuario (regla dura, TODA ingesta)

**Ninguna ingesta escribe en `conocimiento/` sin OK del usuario**, venga de
donde venga el material — incluido el que trajo él mismo. Lo que cambia
con el volumen es la FORMA de la presentación, no la existencia de la
compuerta. Los clips que el usuario dejó en `fuentes/clips/` son aporte
suyo, pero igual llevan veredicto antes de fichar.

- **Lote** (tras el paso D): presentar, con los criterios a la vista, las
  DOS listas COMPLETAS y con el mismo nivel de detalle — lo que entra con
  su motivo y lo que queda afuera con su motivo. Ninguna se resume ni se
  muestrea: en una el usuario rescata lo que el agente tiró, en la otra
  corta lo que el agente metió, y ambas direcciones pesan igual. Sumar el
  costo estimado (piezas, páginas que tocarían, líneas de sub-índice).
- **Pieza suelta o pocas (1-3)**: sin inventario ni muestreo, pero con
  veredicto ANTES de fichar: qué es (título, autor, fecha), lectura
  crítica, qué aporta que la wiki no tenga ya, nivel esperado, páginas
  que tocaría, banderas (táctica sensible → regla sin vetos; contradicción
  con lo fichado) y recomendación explícita — `fichar` o `no fichar`.
  Decir «esto no aporta» o «ya está cubierto por [[x]]» es parte de la
  recomendación honesta: no se ficha por inercia.

Después, ESPERAR la decisión. El usuario puede aprobar, cortar
inclusiones, rescatar descartes, pedir más muestreo o rechazar todo; el
OK es por lista o por pieza, nunca genérico (si cambia el alcance, se
re-presenta). El agente no defiende su filtro por inercia. Lo RECHAZADO
se registra en `LOG.md` (`## [fecha] triaje | Rechazado: <título> —
motivo`, aclarando si la decisión fue del agente o del usuario) para no
re-evaluarlo desde cero.

Con el OK de una **pieza suelta**: copiar su crudo a `fuentes/` y seguir
los pasos 3-7. Con el OK de un **lote**: guardar el mapa de triaje en
`fuentes/<slug>-mapa.md` (inventario + criterios + decisión aprobada,
fechada, distinguiendo la propuesta del agente de las correcciones del
usuario) y recién entonces ejecutar los pasos 3-7 sobre las piezas
aprobadas. Los `dudoso` los resuelve el usuario: entran, salen o van a
`PENDIENTES.md` con su motivo. El crudo ya capturado se conserva en
`fuentes/` aunque no se fiche; lo no capturado no se baja «por las dudas».

## Por cada fuente aprobada

3. **Obtener el crudo** según el tipo: artículo web → extracto markdown a
   `fuentes/`; video → transcript con URL y fecha; contenido tras login →
   solo notas/transcript destilado (NUNCA ripear streams ni redistribuir);
   PDF/notas del usuario → copiar a `fuentes/`.
4. **Ficha crítica** en `fichas/` según el formato del ESQUEMA: resumen,
   afirmaciones numeradas CADA UNA con nivel (🔸 dixit / 🔹 consenso /
   ✅ validado), lectura crítica (¿mecánica o venta interesada? ¿vigente?
   ¿aplica al contexto del usuario definido en el ESQUEMA?), y
   aplicabilidad concreta — con números de la fuente de validación del
   usuario si los hay.
5. **Detección de contradicciones**: contrastar las afirmaciones contra
   conceptos y fichas existentes. Toda contradicción se anota en AMBAS
   páginas y se reporta al usuario en el resumen final.
6. **Integrar**: crear/actualizar las páginas de `conceptos/` afectadas
   (con [[enlaces]] entre páginas) y las `sintesis/` cuyo estado de
   conocimiento cambie. Una fuente típica toca 3-8 páginas.
7. **Registrar**: por cada página nueva, actualizar el sub-índice de su
   subdominio dominante (`INDICE-<subdominio>.md`: entrada + contador de
   cabecera + línea FIN; la portada `INDICE.md` NO se toca salvo mapa
   nuevo), correr `python3 scripts/lint_indice.py conocimiento` (debe quedar verde) y agregar entrada a
   `LOG.md` (`## [fecha] ingesta | Título`). Lagunas detectadas
   (conceptos sin página, preguntas abiertas) → `PENDIENTES.md`.

## Cierre

8. Resumen al usuario: qué se fichó, veredicto crítico en 2-3 líneas,
   contradicciones halladas, páginas tocadas, y qué quedó pendiente. Si
   una táctica sensible/de riesgo entró en la ingesta: avisarlo
   EXPLÍCITAMENTE y marcarla "pendiente de decisión del usuario" (regla
   dura del ESQUEMA — el agente no veta ni aprueba por su cuenta).
9. Ingesta voluminosa (lote aprobado grande): podés delegar piezas
   individuales en subagentes que sigan este mismo ritual y el ESQUEMA —
   pero la revisión de calidad de sus fichas es tuya antes de cerrar.

## Reglas

- Un solo escritor: solo los rituales modifican la wiki.
- **Sin OK explícito del usuario no se ficha NADA** — lote o pieza
  suelta, la haya traído él o no (ver Compuerta). Explorar y analizar NO
  es fichar.
- `fuentes/` inmutable; `LOG.md` append-only.
- Material de pago: solo notas destiladas para uso personal.
- Idioma del proyecto; archivos kebab-case sin acentos.
