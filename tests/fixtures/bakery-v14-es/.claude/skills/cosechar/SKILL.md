---
name: cosechar
description: Cosecha dirigida de fuentes sobre un tema del dominio para la wiki de conocimiento. Usar cuando el usuario diga "cosechá <tema>", "investigá <tema> para la wiki", "buscá fuentes sobre <tema>", o al tomar un tema de la cola de PENDIENTES.md.
---


# Cosechar un tema para la wiki

## Pasos

1. Leé `conocimiento/ESQUEMA.md` + `INDICE.md` (la portada) + los
   sub-índices `INDICE-<subdominio>.md` de los subdominios del tema (si
   no está claro, TODOS; cada uno completo hasta su línea FIN) + la
   sección del tema en `PENDIENTES.md` (si existe). Definí 2-4 preguntas
   concretas que la cosecha debe responder (mostralas al usuario).
2. **Buscar**: fuentes primarias/oficiales del dominio, análisis con
   datos, practicantes con experiencia documentada. Jerarquía del ESQUEMA:
   primaria/oficial > análisis con datos > practicante > divulgador
   genérico. Descartá contenido sin fecha o vencido según el umbral de
   vigencia del ESQUEMA, salvo mecánica estable (anotá la duda).
3. **Filtrar y priorizar**: elegí las 2-4 mejores fuentes para fichar
   AHORA (calidad × relevancia para el contexto del usuario definido en
   el ESQUEMA). El resto de candidatas valiosas → `PENDIENTES.md` con una
   línea de por qué.
4. **Fichar** cada elegida siguiendo el ritual de ingesta — incluida su
   COMPUERTA: veredicto por pieza (qué aporta que la wiki no tenga ya,
   nivel esperado, páginas que tocaría) y OK del usuario ANTES de
   escribir. Si son varias y pesadas, podés delegar en subagentes que
   sigan el ESQUEMA — revisando su calidad antes de cerrar.
5. **Sintetizar**: si la cosecha responde (aunque sea parcialmente) las
   preguntas del paso 1, creá/actualizá la página de `sintesis/` del
   tema: recomendación vigente + evidencia con niveles + qué evidencia
   nueva la cambiaría. Lo que quedó SIN responder → `PENDIENTES.md`.
6. **Registrar**: sub-índice del subdominio de cada página nueva
   (entrada + contador + línea FIN; la portada solo si hay subdominio
   nuevo) + `python3 scripts/lint_indice.py conocimiento` en verde + LOG (`## [fecha] cosecha | <tema>`)
   + tachar el tema en PENDIENTES si quedó cubierto.
7. Resumen al usuario: qué se aprendió (2-4 puntos con niveles de
   confianza), qué se fichó, qué quedó abierto.

## Reglas

- El espíritu crítico es la razón de ser: cada afirmación con nivel
  (🔸/🔹/✅); las contradicciones se registran, no se suavizan.
- Cruzar con la fuente de validación del usuario (datos reales) cuando el
  tema lo permita — es lo que sube afirmaciones a ✅.
- No inflar la wiki: pocas páginas buenas > muchas mediocres.
