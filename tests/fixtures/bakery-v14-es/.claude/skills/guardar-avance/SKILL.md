---
name: guardar-avance
description: Ritual de cierre de hito o sesión — persiste el avance del proyecto para futuras sesiones (PLAN, BITACORA, ARQUITECTURA, control de versiones) con verificación de presupuestos y compactación. Usar cuando el usuario diga "guardar avance", "guardá lo que hicimos", "cerrar sesión", "registrar esto", o proactivamente al completar un hito significativo (feature terminada, decisión importante, fase completada, problema relevante resuelto).
---


# Guardar avance — ritual de persistencia

Ejecutá TODOS los pasos, en orden. El objetivo: que una sesión futura pueda
retomar exactamente desde aquí sin perder contexto ni pisar nada.

## 0. Medir antes de escribir
- `python3 scripts/lint_continuidad.py --margen`: cuánto cabe en cada documento con tope. Si lo
  que vas a escribir no cabe: rotá (`python3 scripts/rotar_bitacora.py`, ensayo primero; herederos
  verificados) o compactá archivando ANTES de redactar.
- ¿Hay otra sesión o subagente trabajando en el proyecto? Entonces tocá
  solo lo tuyo, releé y escribí en el mismo paso, no rotes ni compactes lo
  ajeno, y al confirmar hacé staging archivo por archivo.

## 1. PLAN.md
- Actualizá estados (✅/🔄/⏳/💡) de lo trabajado en la sesión.
- Tareas 🔄 a medio hacer: "quedamos en: <punto exacto>" + próximo paso
  concreto. Agregá tareas/ideas nuevas acordadas con el usuario.
- Refrescá la fecha de última actualización.

## 2. BITACORA.md (append-only — NUNCA borrar ni editar entradas)
- Una entrada fechada por cada decisión o hallazgo: QUÉ se hizo/decidió +
  POR QUÉ + qué NO hacer (si aplica).
- Incluí los porqués del usuario (preferencias expresadas, opciones que
  rechazó).

## 3. ARQUITECTURA.md (solo si cambió la estructura)
- Piezas/automatismos nuevos o modificados → actualizar.
- Reglas críticas nuevas → sección INVARIANTES.
- Reglas nuevas → instrucciones del PROYECTO (o INVARIANTES). Nunca a las
  instrucciones globales/personales del usuario, si su entorno las tiene:
  esas se pagan en todas las sesiones de todos sus proyectos y solo admiten
  reglas genéricas; una regla llega ahí únicamente por graduación (ritual de
  introspección, con OK).
- Fragilidades detectadas → deuda técnica.

## 4. Retro de criterio (solo si el sistema de metacognición está instalado)
- ¿Hubo correcciones del usuario que revelen un patrón, predicciones
  refutadas, estrategias superadoras, ineficiencias? → PROPONÉ la lección
  (solo se ficha con OK del usuario) o declará "sin lecciones de criterio".

## 5. Presupuestos y compactación (verificar SIEMPRE)
- Correr `python3 scripts/lint_continuidad.py`: OK / ALARMA / EXCESO contra los presupuestos de
  PLAN (líneas Y bytes). EXCESO → COMPACTAR archivando (el rotador para la
  bitácora; secciones cerradas de PLAN a 1-3 líneas + puntero), nunca
  borrando. Dejá nota de qué se archivó. Un documento que cierra al filo del
  tope sesión tras sesión → proponer al usuario partición o recalibración.
- Si el cerebro (wiki crítica) está instalado y hubo operaciones en la
  wiki: su verificador en verde y su LOG al día.

## 6. Control de versiones
- Staging POR ARCHIVO, nunca «todo lo modificado»: primero el estado del
  árbol (`git status --short`); lo modificado que NO tocaste en esta sesión
  es de otra sesión o de un subagente — no se agrega ni se confirma;
  después `git add <archivo> …` solo con lo tuyo y otro `git status --short`
  para ver que quedó exactamente eso.
- Revisá qué entra ANTES de confirmar: nada de secretos, datos pesados ni
  generados (si aparecen, excluilos, no los fuerces).
- Commit descriptivo en el idioma del proyecto: qué + por qué (nunca
  "cambios varios"). Sin push a remotos salvo pedido del usuario.
- Si el agente tiene memoria persistente propia: actualizala también.

## 7. Confirmación al usuario
- Resumí en 3-5 líneas qué quedó registrado y dónde, y si quedó algo 🔄
  con su "quedamos en". Si algo hecho en la sesión CONTRADICE una
  invariante de ARQUITECTURA.md, decílo explícitamente ahora.
