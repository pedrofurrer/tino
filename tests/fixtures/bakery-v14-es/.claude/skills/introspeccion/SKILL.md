---
name: introspeccion
description: Consolidación del criterio del agente — revisa las lecciones de criterio del proyecto, mide reincidencia, detecta sesgos transversales, promueve/degrada validaciones y poda el índice. Usar cuando el usuario diga "/introspeccion", "revisá tu criterio", "corré la introspección"; en la revisión periódica del proyecto; o PROPONERLA de inmediato ante un hito de replanteo (ver señales).
---


# Introspección — consolidación del criterio del agente

Las lecciones de criterio viven en el directorio configurado al instalar
(`criterio/leccion-*.md`), indexadas en la sección «Criterio del agente» del
índice del proyecto. Formato: frontmatter (`validacion: propuesta |
hipotesis | recurrente | confirmada`, `ambito`) + cuerpo **Gatillo / Error
original / Principio / Aplicación / Casos**. El Gatillo se escribe por
MECANISMO (acto + insumo); las formas concretas ilustran, no limitan; una
reincidencia por una forma no enumerada ⇒ reformular por mecanismo, no
agregar la forma a la lista.

## Disparadores (los tres valen)

1. **Periódico**: según la cadencia configurada (semanal recomendado,
   fusionada con un ritual de revisión existente).
2. **Manual**: el usuario la invoca cuando quiere.
3. **Por evento**: en CUALQUIER sesión, si detectás una señal de hito de
   replanteo, proponé correrla en el momento (no esperes el calendario):
   - una premisa establecida del proyecto queda refutada por la realidad;
   - un resultado importante difiere fuerte de lo esperado;
   - reincidencia en caliente de un error ya fichado;
   - ≥2 lecciones nuevas en pocos días sobre el mismo eje.
   En sesiones autónomas: registrá la recomendación y presentala en el
   próximo contacto.

## Procedimiento

1. **Leer, de forma incremental**: `python3 scripts/lint_criterio.py --dir criterio --indice criterio/INDICE.md --resumen` lista cada
   lección con validación, ámbito, casos y última modificación; abrí enteras
   solo las que cambiaron desde la corrida anterior o las que una
   reincidencia señala (leer todas no escala: en la casa de origen eran 65
   fichas y ~340 KB). Sumá el registro reciente del proyecto (bitácora,
   changelog o equivalente); si tu entorno permite buscar en transcripts de
   sesiones pasadas y hace falta rastrear un caso, usalo.
2. **Reincidencia** (la señal más valiosa): ¿se repitió un error ya fichado?
   → falló el gatillo (mal formulado) o el canal de aplicación → REFORMULAR
   la lección, no solo anotar el caso. Y preguntá primero «¿qué MOMENTO
   comparten las reincidencias?»: si comparten el acto, el insumo y el
   punto del trabajo, el remedio es un instrumento (verificador, gancho,
   campo obligatorio, paso del ritual con el comando escrito), que se
   registra como `heredero` en la ficha — no otra línea de texto.
3. **Borradores**: lecciones en `validacion: propuesta` (capturadas en
   trabajo autónomo) se presentan al usuario para OK, corrección o descarte.
4. **Patrones transversales**: ¿varias lecciones apuntan a un sesgo de
   fondo? → proponer consolidarlas en una lección madre (las hijas se
   archivan con enlace; no se borra nada).
5. **Promoción/degradación**: hipotesis → recurrente (2+ casos) →
   confirmada (aplicada con éxito observable). Sin recurrencia ni uso en
   ~30 días → archivo. Confirmadas de gatillo frecuente → proponer al
   usuario su graduación a regla permanente, con DESTINO según el `ambito`
   de la ficha: `<proyecto>` → instrucciones, guías o invariantes del
   proyecto; `transversal` → las instrucciones GLOBALES del usuario, si su
   entorno las tiene — reescrita sin referencias al proyecto (ni su dominio
   ni sus herramientas), porque esas instrucciones se cargan en todas las
   sesiones de todos sus proyectos y solo admiten reglas genéricas; la
   ficha conserva la historia. Es `transversal` solo si gatillo y principio
   hablan del MÉTODO y aplicarían sin cambios en otro proyecto. Nunca
   escribir en las instrucciones globales fuera de este paso ni sin OK.
6. **Poda**: la sección «Criterio del agente» del índice se mantiene dentro
   del tope vigente (≤20 líneas por defecto; recalibrable con uso medido y
   OK del usuario, registrando el porqué — la casa de origen lo llevó a 40
   al medir ~21 lecciones distintas citadas en 9 días). Las archivadas salen
   del índice, no del disco. Las graduadas a regla dura se comprimen a una
   mención: viven en las instrucciones, no dependen del índice. Higiene
   mecánica: la sección va PRIMERO en el archivo que se carga, cierra con
   «FIN DEL ÍNDICE DE CRITERIO — N entradas» y el archivo entero queda bajo
   el límite de carga del entorno — `python3 scripts/lint_criterio.py --dir criterio --indice criterio/INDICE.md` en verde al cerrar.
7. **Mini-informe al usuario** (3-5 líneas): lecciones nuevas/consolidadas,
   reincidencias detectadas, promociones/graduaciones propuestas. Registrar
   la corrida donde el proyecto registre mantenimiento.

## Gobernanza (dura)

- Toda lección nueva o reformulación sustancial se PROPONE al usuario antes
  de fichar (gatillo + principio en 2-3 líneas); sin su OK queda `propuesta`.
- Las graduaciones a documentos compartidos SIEMPRE requieren su OK.
- Las lecciones nunca vetan decisiones del usuario: describen el criterio
  del agente, no le quitan al usuario las decisiones de riesgo/beneficio.
