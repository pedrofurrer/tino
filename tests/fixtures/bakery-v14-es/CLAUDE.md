# Panadería Los Robles — instrucciones del proyecto

Idioma de trabajo: español. Proyecto chico: recetario en markdown + análisis de ventas (CSV + script).

## Continuidad entre sesiones (OBLIGATORIO, leer primero)

1. **ANTES de modificar** código, estructura, contenido o configuración:
   leé `PLAN.md` (estado del roadmap y "quedamos en") y `ARQUITECTURA.md`
   (mapa del sistema y sus **INVARIANTES**). Si tu cambio contradice una
   invariante o una decisión registrada en `BITACORA.md`, **DETENETE y
   alertá al usuario** antes de tocar nada.
2. **AL CERRAR un hito o sesión significativa** (o cuando el usuario lo
   pida): ejecutá el ritual de cierre completo (skill `guardar-avance` del proyecto) — PLAN,
   BITACORA, ARQUITECTURA si cambió, presupuestos/compactación, commit.
3. **`BITACORA.md` es append-only**: nunca borres ni edites entradas; las
   reversiones se documentan con una entrada nueva.
4. Los planes multi-sesión viven en `PLAN.md` con su avance exacto
   ("quedamos en X"); retomá desde ahí, no desde tu suposición.
5. Presupuestos en líneas y bytes (los exactos, en `PLAN.md`, línea
   `lint-topes`): medí ANTES de escribir (`python3 scripts/lint_continuidad.py --margen`); si no
   cabe, rotá (`python3 scripts/rotar_bitacora.py`) o compactá archivando ANTES, nunca borrando.
   Con otra sesión activa: tocá solo lo tuyo, staging archivo por archivo.
<!-- suite-agentica: continuidad v1.4 -->

## Criterio del agente (metacognición)

1. Este proyecto mantiene **lecciones de criterio** en `criterio/` (índice en
   `criterio/INDICE.md`, al principio y hasta su línea FIN): errores de razonamiento
   ya corregidos, destilados como gatillo → principio. Leelo al arrancar
   trabajo de peso.
2. **Chequeo pre-entrega**: antes de entregar un entregable de peso
   (informe, estrategia, plan, texto a terceros), pasá por el índice; si el
   gatillo de una lección matchea, aplicala y citala en una línea al final
   ("Criterio aplicado: <lección>"). No aplica a respuestas rápidas.
3. **Captura**: si una corrección del usuario revela un PATRÓN, o la
   realidad/datos refutan una predicción tuya, PROPONÉ una lección (gatillo
   + principio, 2-3 líneas). Solo se ficha con su OK; en trabajo autónomo
   queda como `propuesta` pendiente.
4. **Introspección** (semanal, fusionada con la revisión periódica de `PLAN.md`; invocación: skill `introspeccion` del proyecto): consolida, mide
   reincidencia y poda. Ante un hito de replanteo (premisa refutada,
   resultado muy distinto al esperado, reincidencia), proponela de
   inmediato.
<!-- suite-agentica: metacognicion v1.4 -->

## Cerebro de panadería artesanal (`conocimiento/`)

Wiki crítica que mantiene el agente (UN solo escritor) sobre panadería artesanal.
Antes de operarla, leé `conocimiento/ESQUEMA.md` (convenciones, niveles,
reglas duras); navegá `INDICE.md` (la PORTADA) primero y de ahí los
sub-índices: subdominio claro → ese COMPLETO (hasta su línea FIN); en la
duda, TODOS. **NADA se ficha sin OK explícito del usuario** (veredicto por
pieza o mapa de triaje por lote; explorar no es fichar). Al asesorar:
síntesis/fichas + los datos reales del usuario, citando niveles (🔸 dixit
/ 🔹 consenso / ✅ validado). Tácticas o decisiones sensibles: el agente
documenta mecánica, impacto y riesgos y AVISA — la decisión es SIEMPRE
del usuario. Aportes: `fuentes/clips/` y `PENDIENTES.md`. Rituales:
skills `ingerir-fuente`, `cosechar` y `lint-wiki` (ingesta, cosecha, lint — proponer el lint cada ~10 fichas; el
verificador cuenta las ingestas desde el último).
<!-- suite-agentica: cerebro v1.4 -->
