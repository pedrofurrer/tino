---
name: lint-wiki
description: Chequeo de salud de la wiki de conocimiento — contradicciones, vigencias vencidas, páginas huérfanas, lagunas. Usar cuando el usuario diga "lint de la wiki", "revisá la wiki", "chequeo de salud del conocimiento", o periódicamente tras varias ingestas (proponerlo cada ~10 fichas nuevas).
---


# Lint de la wiki

Dos planos: el **estructural** (paso 2) es mecánico y lo cierra cada ritual;
el **de contenido** (pasos 3-5) es el lint propiamente dicho, periódico — el
verificador imprime «ingestas desde el último lint: N» y avisa a partir de
~10; un verificador en verde no significa wiki sana.

## Chequeos

1. Leé `conocimiento/ESQUEMA.md` + `INDICE.md` (portada) + TODOS los
   sub-índices `INDICE-*.md` (el lint es transversal por definición; cada
   uno hasta su línea FIN) + últimas entradas de `LOG.md`.
2. **Consistencia estructural**:
   - Correr `python3 scripts/lint_indice.py conocimiento` (portada↔disco, contadores, líneas FIN, topes
     por archivo, bijección página↔entrada) y arreglar lo que reporte.
   - Huérfanas: páginas sin ningún [[enlace]] entrante.
   - Conceptos mencionados repetidamente como [[enlace]] sin página propia.
   - Bandeja atascada: material en `fuentes/clips/` sin ficha.
   - Sub-índice sobre la ALARMA (140 líneas / 35 KB) → proponer al usuario
     la partición de 2º nivel de ese subdominio (ESQUEMA §Escala) — nunca
     de oficio.
3. **Consistencia de contenido**:
   - Contradicciones entre fichas/conceptos/síntesis no anotadas.
   - Afirmaciones 🔸 dixit que ya podrían validarse contra la fuente de
     validación del usuario → proponer el cruce (es lo que sube a ✅).
   - Síntesis desactualizadas respecto de fichas más nuevas que las tocan.
4. **Vigencia**: fichas con `fecha_fuente` más vieja que el umbral del
   ESQUEMA en temas que el campo cambia rápido → ¿siguen `vigente` o pasan
   a `dudosa`? Proponer verificación puntual. Si existe capa de material
   perecedero (`mercado/`): revisar su `fecha_datos` en CADA lint.
5. **Lagunas**: preguntas del dominio sin síntesis que las responda; temas
   de PENDIENTES estancados.
6. **Meta** (solo si el sistema de metacognición está instalado): ¿el lint
   reveló un patrón de error del propio agente (fichar sin nivel, validar
   de más, dominios mal asignados)? → proponerlo como señal para su
   introspección.

## Salida

7. Correcciones mecánicas (índice, enlaces rotos): aplicalas directo.
   Cambios de contenido (vigencias, contradicciones, fusiones): presentá
   la lista al usuario y aplicá con su OK.
8. Actualizar `PENDIENTES.md` (lagunas y propuestas de cosecha) y `LOG.md`
   (`## [fecha] lint | resumen`). Reporte final: salud general en 3-5
   líneas + qué acción rendiría más.
