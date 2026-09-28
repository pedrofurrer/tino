# ESQUEMA — Convenciones del cerebro de panadería artesanal

> Este documento disciplina al agente que mantiene la wiki. Leerlo ANTES
> de cualquier operación sobre `conocimiento/`. Co-evoluciona con el uso; los
> cambios de esquema se registran en LOG.md.

## Propósito

Base de conocimiento CRÍTICA sobre panadería artesanal. Objetivo: que el agente
actúe como experto escéptico que asesora al usuario y, con sus datos
reales, valide o refute afirmaciones y estrategias. NO es un archivo de
apuntes: es una síntesis viva y trazable.

## Subdominios (uno por sub-índice)

- **masas-y-fermentacion** — harinas, hidratación, masa madre, tiempos y temperaturas de fermentación.
- **horneado** — horno de leña, vapor, cortes, curvas de temperatura.
- **costos-y-precios** — costo por pieza, insumos, márgenes, fijación de precios.
- **venta-y-clientela** — qué se vende y cuándo, hábitos de la clientela de barrio, promociones.

Cada subdominio tiene su sub-índice `INDICE-<subdominio>.md`. Cada página se lista UNA vez, en su subdominio dominante; los cruces se resuelven con enlaces wiki. Ante la duda: ¿a qué pregunta del dominio responde primero?.md`. Cada página se
lista UNA vez, en su subdominio dominante; los cruces se resuelven con
enlaces wiki. Ante la duda: ¿a qué pregunta del dominio responde primero?>

## Arquitectura

```
fuentes/    → crudo INMUTABLE (transcripts, clips, PDFs).
  clips/    → bandeja de entrada del usuario; sin ficha = pendiente.
fichas/     → una por fuente procesada (lectura crítica; estables).
conceptos/  → una página por concepto/estrategia/entidad (vivas).
sintesis/   → "qué creemos HOY y por qué" por tema + análisis valiosos
              archivados. Lo primero que se consulta al asesorar.
INDICE.md   → PORTADA: protocolo de lectura + mapa de sub-índices. SE LEE
              PRIMERO, SIEMPRE (entera; es chica).
INDICE-<subdominio>.md → sub-índices (uno por subdominio + INDICE-fuentes.md):
              las entradas (enlace + 1 línea), con contador en cabecera y
              línea FIN al pie (sin FIN visto, no está leído).
LOG.md      → append-only: ## [AAAA-MM-DD] operacion | Título
PENDIENTES.md → cola de fuentes, temas a cosechar y lagunas.
```

## Reglas duras (no negociables)

1. **Un solo escritor**: la wiki la escribe el agente (vía rituales). El
   usuario aporta por `fuentes/clips/` y `PENDIENTES.md`, y navega/lee.
2. `fuentes/` es inmutable; `LOG.md` es append-only.
3. Toda operación actualiza el SUB-ÍNDICE del subdominio afectado
   (entrada + contador de cabecera + línea FIN) y agrega entrada a
   `LOG.md`; la portada solo cambia si cambia el mapa. Cierre mecánico:
   ``python3 scripts/lint_indice.py conocimiento`` en verde.
4. Toda afirmación importante lleva nivel de confianza y es rastreable a
   su ficha (y la ficha a su fuente).
5. **Sin vetos del agente**: tácticas/decisiones sensibles o de riesgo se
   documentan (mecánica, impacto estimado, riesgos, nivel de confianza),
   se marcan "pendiente de decisión del usuario" y se le avisa. La
   decisión de uso es SIEMPRE del usuario, caso por caso.
6. Material de pago: notas para uso personal; NUNCA republicar.
7. Respuestas valiosas de consultas → archivar en `sintesis/`.
8. No inflar: pocas páginas buenas > muchas mediocres.
9. **NADA se ficha sin OK explícito del usuario** — lote o pieza suelta,
   lo haya traído él o no; explorar y analizar NO es fichar (el trabajo
   previo vive fuera de la wiki hasta la aprobación). En bloque: criterios
   declarados antes → inventario → muestreo → veredicto por pieza → las
   DOS listas completas (el usuario rescata lo tirado y corta lo metido)
   → mapa de triaje aprobado. Pieza suelta: veredicto + recomendación
   explícita antes de fichar. Lo rechazado se registra (`triaje`).

## Niveles de confianza y vigencia

- 🔸 `dixit` — sin evidencia verificable. Se registra, no se recomienda.
- 🔹 `consenso` — múltiples fuentes independientes o mecánica oficial.
- ✅ `validado` — contrastado con `datos/ventas-2026.csv` (ventas reales) y el cuaderno de horneadas (hoy en papel; laguna). Único nivel que
  habilita recomendación fuerte.
- Vigencia: `vigente` / `dudosa` / `obsoleta`. Umbral orientativo para
  este campo: técnica de panificación: 5 años; precios de insumos y hábitos de compra: 12 meses. Fuentes oficiales: autoritativas en
  mecánica, interesadas en estrategia — separar ambos planos.

## Contexto del usuario (para juzgar aplicabilidad)

Panadería de barrio: dos personas, horno de leña, producción diaria chica (tres productos), sin local grande ni reparto. Toda ficha evalúa: ¿aplica a ESTE caso o es consejo para una panadería industrial, una cadena o un horno eléctrico?

## Formatos

- **Ficha** (`fichas/<slug>.md`): frontmatter (tipo, titulo, fuente,
  autor, url, fecha_fuente, fecha_ingesta, temas, confianza, vigencia) +
  Resumen → Afirmaciones clave (numeradas, cada una con nivel) → Lectura
  crítica (mecánica vs venta; vigencia; contradicciones con enlace) →
  Aplicabilidad al contexto del usuario → Conceptos afectados.
- **Concepto** (`conceptos/<slug>.md`): definición breve → estado del
  conocimiento (niveles + enlaces a fichas) → relaciones → aplicación.
- **Síntesis** (`sintesis/<slug>.md`): recomendación vigente → evidencia
  (niveles + enlaces) → qué evidencia nueva la cambiaría.
.md`):
  foto FECHADA con `fecha_datos`; nunca se edita una vieja: se escribe una
  nueva (serie histórica). - **Actor** (`mercado/actor-<nombre>.md`):
  página viva por rival/proveedor/referente; observaciones fechadas en
  append.>
- **Mapa de triaje** (`fuentes/<slug>-mapa.md`): resultado APROBADO del
  triaje de un conjunto (regla 9). Cabecera: qué es el conjunto, cuándo se
  inventarió y de dónde. Cuerpo: criterios declarados → inventario →
  decisión fechada (qué se ficha, qué NO y por qué, qué quedó `dudoso`),
  distinguiendo la propuesta del agente de las correcciones del usuario.
  Regla de repesca: lo descartado no se re-evalúa desde cero; si el
  alcance se amplía, el mapa dice qué hay disponible.
- **LOG**: `## [AAAA-MM-DD] operacion | Título` — operaciones: fundacion,
  ingesta, cosecha, consulta, lint, esquema, correccion, triaje.

## Rituales y escala

Ingerir fuente / Cosechar tema / Lint — ver sus procedimientos
(instalados como skills o en las instrucciones del proyecto). Consulta:
SIEMPRE la portada `INDICE.md` entera; UN subdominio claro → su sub-índice
COMPLETO (hasta la línea FIN); consulta transversal, comparativa o de
subdominio dudoso → TODOS los sub-índices (en la duda, TODOS: responder
con medio catálogo es el modo de falla que motivó la partición). Después
síntesis/conceptos → fichas; responder citando páginas y niveles; cruzar
con `datos/ventas-2026.csv` (ventas reales) y el cuaderno de horneadas (hoy en papel; laguna) cuando aplique. Escala: topes POR ARCHIVO —
ALARMA 140 líneas / 35 KB (proponer partición de 2º nivel del subdominio;
nunca de oficio), TOPE 170 líneas / 45 KB (impostergable; decide el
usuario; KB = 1000 bytes); verificador ``python3 scripts/lint_indice.py conocimiento`` al cerrar cada
operación (lint ESTRUCTURAL, mecánico); el lint de CONTENIDO es periódico
— el verificador cuenta las ingestas desde el último y avisa a partir de
~10. Idioma: español; archivos kebab-case sin acentos.
