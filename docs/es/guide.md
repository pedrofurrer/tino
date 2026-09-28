# tino — guía

*Read in English: [../guide.md](../guide.md).*

tino le da a un agente de IA tres hábitos que los profesionales cuidadosos ya
tienen: llevar registro del trabajo, aprender de las correcciones y leer las
fuentes con sentido crítico. Cada hábito es un sistema de archivos Markdown
dentro de tu proyecto: lo arma una skill instaladora y lo mantiene el agente.
Tú apruebas lo que entra.

En un proyecto en español los archivos llevan nombres en español; esta guía
los nombra así, con el nombre inglés entre paréntesis la primera vez.

- [La idea](#la-idea)
- [Primeros pasos](#primeros-pasos)
- [Continuidad](#continuidad)
- [Metacognición](#metacognición)
- [Cerebro](#cerebro)
- [El día a día](#el-día-a-día)
- [Límites](#límites)
- [Actualizar desde 1.x](#actualizar-desde-1x)
- [Preguntas](#preguntas)

## La idea

- **Todo lo que importa vive en archivos que puedes leer.** No hay base de
  datos, ni servicio, ni memoria oculta: un plan, una bitácora, fichas de
  lecciones, páginas de una wiki. Viajan con el proyecto y con su control de
  versiones.
- **El agente los mantiene; tú decides qué entra.** Las lecciones y las
  páginas de la wiki primero se proponen, y se escriben solo con tu OK.
- **Las instrucciones se pagan en cada sesión.** Las reglas que el agente
  debe ver siempre caben en bloques cortos (20, 15 y 15 líneas como máximo),
  y todo lo demás se lee cuando hace falta. Cuatro scripts chicos miden
  tamaños y controlan índices, para que los archivos no crezcan sin que nadie
  lo note.
- **El material de afuera es un dato, nunca una instrucción.** Una página
  web, un correo o un documento ajeno pueden informar el trabajo, pero una
  orden dirigida al agente dentro de ese material se te informa; no se
  obedece.

Los tres sistemas funcionan solos o juntos. Cuando hay más de uno instalado,
cada uno detecta a los otros y se conecta: el ritual de cierre incluye la
retro de criterio y las operaciones grandes de la wiki quedan en la
bitácora.

## Primeros pasos

Instala el plugin una vez (ver el [README](../../README.es.md#instalación))
y, en cada proyecto, pide el sistema que quieras: «instala la continuidad»,
«instala la metacognición», «instala el cerebro». Si quieres los tres, el
orden habitual es la continuidad primero, porque los otros registran sus
decisiones en su bitácora; después la metacognición, y el cerebro al final,
cuando sus parámetros de dominio están claros.

Cada instalador:

1. lee el proyecto y explica en pocas líneas qué crearía;
2. hace las preguntas que necesita, cada una con un valor por defecto;
3. espera tu OK, y recién entonces escribe los archivos, con el estado real
   del proyecto en lugar de plantillas vacías;
4. corre su verificador y cierra con un informe corto: qué creó, qué adaptó
   y por qué, y los dos o tres gestos que vas a usar.

En Claude Code, escribir los rituales en `.claude/skills/` pide tu permiso.
Si no lo das, van a `rituales/` y el bloque de reglas los señala ahí; puedes
moverlos después.

Quitar el plugin no borra nada de tus proyectos: los archivos son tuyos y
siguen funcionando como documentos comunes.

## Continuidad

Las sesiones son efímeras: lo que se decidió desaparece al cerrarlas, y la
siguiente vuelve a explorar, pisa o rompe lo que la anterior sabía. La
continuidad lo resuelve con una regla: todo lo relevante vive en archivos del
proyecto, y el agente debe leerlos antes de actuar y actualizarlos al
cerrar.

Tiene cuatro capas:

1. **Documentos vivos** en la raíz del proyecto.
   - `PLAN.md`: la hoja de ruta, con una sección «quedamos en» arriba y
     estados de tarea (✅ hecho, 🔄 en curso, ⏳ pendiente, 💡 idea).
   - `BITACORA.md` (`LOGBOOK.md`): entradas fechadas con las decisiones y
     sus razones. Solo se agrega: una marcha atrás es una entrada nueva,
     nunca una edición.
   - `ARQUITECTURA.md` (`ARCHITECTURE.md`): un mapa del proyecto y sus
     **INVARIANTES** numerados, las reglas que no se rompen sin tu OK.
2. **Un bloque de reglas** en el archivo de instrucciones del agente
   (`CLAUDE.md`, `AGENTS.md` o equivalente), de 20 líneas como máximo, que
   le indica leer esos documentos antes de cambiar algo, y frenar y avisarte
   si un cambio contradice un invariante o una decisión registrada.
3. **Control de versiones**, si el proyecto lo tiene. El instalador ofrece
   iniciarlo y revisa qué no debe entrar en un commit.
4. **Un ritual de cierre**, que se invoca con «guarda el avance» o se corre
   después de un hito: actualiza los tres documentos dentro de sus topes,
   corre el verificador y hace el commit.

**Topes.** Cada documento tiene un tope en líneas y en kilobytes, con una
alarma al 80 %: PLAN 150 líneas y 18 KB, ARQUITECTURA 200 y 30 KB,
BITACORA 200 y 25 KB, el archivo de instrucciones completo 300 líneas y
20 KB. Viven en una línea al principio de `PLAN.md`, así que puedes
recalibrarlos. El verificador (`scripts/lint_continuidad.py`, o
`lint_continuity.py` en el juego inglés) compara cada documento y cada
bloque con su tope; con `--margen` dice cuánto cabe todavía antes de
escribir.

**Rotación.** Cuando la bitácora se llena, `scripts/rotar_bitacora.py` mueve
las entradas más viejas, textuales, a `BITACORA-archivo.md`, bajo una marca
que dice dónde viven ahora sus partes todavía vigentes. Primero muestra un
simulacro y no cambia nada hasta que corre con `--ejecutar`.

**Escala.** Un proyecto chico o corto puede usar la escala mínima: PLAN,
control de versiones y una regla corta. El instalador propone la escala y
registra por qué.

## Metacognición

Un agente no aprende entre sesiones. La memoria automática lo ayuda a
recordar hechos; la metacognición hace que cambie su forma de pensar. La
unidad es una **lección de criterio**: una ficha en `criterio/` (`lessons/`)
con

- un **Gatillo**: una situación que se reconoce antes de actuar («estoy por
  comparar períodos de una serie…»);
- el **Error original**, fechado;
- un **Principio**: la regla, como instrucción;
- la **Aplicación**: cómo se ve hacerlo bien;
- los **Casos**: líneas fechadas de origen, aplicación exitosa y
  reincidencia.

Cada ficha declara su **validación** (`propuesta` sin tu OK, `hipotesis`
con un caso, `recurrente`, `confirmada` cuando ya se aplicó con éxito,
`graduada`, `archivada`), su **evidencia** (`dato`, `fuente`, `realidad` o
solo la palabra del `usuario`; una lección que descansa solo en tu palabra no
pasa de `recurrente` hasta que algo la corrobore) y su **ámbito**: este
proyecto, o `transversal` cuando habla del método y valdría igual en otro
lado.

**Captura.** Cuando corriges al agente y la corrección muestra un patrón, o
los datos refutan una de sus predicciones, propone una lección en dos o tres
líneas: gatillo, principio y en qué se apoya. Escribe la ficha solo con tu
OK. El ritual de cierre suma un paso de retro: lecciones para proponer, o un
«sin lecciones» explícito.

**Aplicación.** Proponer lecciones es fácil; aplicarlas es donde se gana o se
pierde, por cuatro canales:

1. un **índice** con una línea por lección, que se carga en cada sesión (por
   defecto, justo debajo del bloque de reglas);
2. un **control antes de entregar**: antes de un trabajo importante (un
   informe, un plan, un texto para terceros) el agente repasa el índice y
   termina con «Criterio aplicado: <lección>» cuando alguna aplica, así ves
   que se usa;
3. la **graduación**: una lección confirmada con un gatillo frecuente puede
   pasar a regla permanente del proyecto, o de tus instrucciones globales si
   es transversal, con tu OK;
4. un **instrumento**: cuando una lección falla una y otra vez en el mismo
   momento del trabajo, la solución es un control que salte en ese momento
   (un script, un campo obligatorio, un paso del ritual), no más texto.

Para ver en qué pueden terminar las lecciones graduadas, están las
[reglas duras](principles-example.md) de un usuario.

**La introspección** consolida las lecciones: cada semana o con la revisión
periódica del proyecto, cuando la pides, y de inmediato después de un
momento de replanteo, como una premisa refutada o un error ya archivado que
se repite. Mide cuántas veces reincidió el error de cada lección, reformula
las que fallan y poda el índice. tino no lee la memoria
propia de tu agente ni conversaciones pasadas: las lecciones salen de
correcciones hechas en la sesión y viven en el proyecto.

**Gobierno.** Las lecciones describen el criterio del agente. Nunca vetan
tus decisiones ni te quitan las que son tuyas.

## Cerebro

Las fuentes se acumulan: artículos, informes, notas, fichas técnicas. El
cerebro es una wiki de tu dominio que el agente escribe y mantiene, en
`conocimiento/` (`knowledge/`), donde cada afirmación lleva un nivel de
confianza:

- 🔸 **dixit**: alguien lo dice; no hay evidencia verificable;
- 🔹 **consenso**: varias fuentes independientes coinciden, o está
  documentado oficialmente;
- ✅ **validado**: contrastado con tus propios datos; el único nivel que
  sostiene una recomendación fuerte.

Las páginas llevan además una **vigencia** (vigente, dudosa, obsoleta), con
la fecha de la fuente. A las fuentes oficiales o interesadas se les cree
sobre cómo funcionan las cosas, no sobre lo que te conviene.

**Instalarlo** es acordar cuatro parámetros: el dominio y sus tres a siete
subdominios; la fuente de validación (tus datos, tus registros); qué tan
rápido cambia el campo, que define cuándo algo queda viejo; y tu contexto,
para que cada ficha pregunte si un consejo sirve para tu caso.

**Organización.** `fuentes/` guarda el material crudo, inmutable, con una
bandeja de entrada en `fuentes/clips/` para lo que traes. `fichas/` tiene una
lectura crítica por fuente, `conceptos/` una página por concepto,
`sintesis/` «qué creemos hoy y por qué» por tema. `INDICE.md` es una portada
que apunta a un subíndice por subdominio, cada uno con un contador y una
línea de cierre, para que el verificador (`scripts/lint_indice.py`) pueda
probar que el índice y las páginas en disco coinciden. `LOG.md` registra cada
operación y `PENDIENTES.md` la cola.

**Tres rituales.**

- **Ingerir una fuente** («ingiere esto»): el agente la lee, la contrasta con
  lo archivado y con tus datos, y presenta un veredicto (fichar, descartar o
  dudoso) con las páginas que tocaría. No se escribe nada hasta tu OK. Una
  fuente descartada queda registrada con su motivo, para no evaluarla otra
  vez desde cero. Las fuentes que guardas en otra parte del proyecto se
  copian, nunca se mueven.
- **Cosechar un tema** («cosecha <tema>»): el agente define dos a cuatro
  preguntas concretas, busca, filtra por la jerarquía de fuentes y propone
  qué archivar.
- **Revisar la wiki** («revisa la wiki»): el verificador corre en cada
  ritual; una revisión de contenido (contradicciones, páginas viejas,
  huérfanas y huecos) se propone cada unas diez ingestas.

**Las fuentes son datos.** La wiki lee material de afuera, incluidas las
instrucciones escondidas en él para asistentes de IA. Esas se informan y
nunca se siguen, y bajan la confiabilidad de la fuente.

## El día a día

| Dices | Qué pasa |
|---|---|
| «guarda el avance» | El ritual de cierre: documentos, verificador, commit y un informe de 3 a 5 líneas |
| una corrección | Si muestra un patrón, una propuesta de lección |
| «corre la introspección» | Lecciones revisadas, reincidencia medida, índice podado |
| «ingiere esto» | Un veredicto crítico sobre la fuente y, con tu OK, el fichado |
| «cosecha <tema>» | Búsqueda dirigida y una propuesta de qué archivar |
| «revisa la wiki» | Revisión estructural y de contenido |

Algunos hábitos lo hacen funcionar mejor:

- **Corrige con el motivo.** «El promedio tiene que ponderar por volumen,
  porque los volúmenes cambian de semana a semana» da una lección mejor que
  «eso está mal».
- **Lee lo que propone antes de dar el OK.** La compuerta vale lo que vale
  tu revisión.
- **Di que no.** Rechazar una lección o una fuente también queda registrado,
  y sirve.
- **Edita los archivos tú mismo cuando quieras.** Son Markdown común; corre
  los verificadores después.

## Límites

- **Son instrucciones, no una obligación mecánica.** El bloque de reglas le
  dice al agente qué hacer en cada sesión; un modelo igual puede saltarse un
  paso. Los verificadores detectan la deriva estructural, y los
  [controles opcionales para Claude Code](../guardrails.md) suman controles
  mecánicos: un archivo de bitácora bloqueado, el «quedamos en» vuelto a
  mostrar al retomar y una guarda sobre las fuentes crudas de la wiki.
- **Cuesta tokens.** En los ejemplos, unos 1.750 tokens por sesión por los
  archivos instalados y unos 230 por el plugin (medido el 2026-09-28).
- **La evidencia todavía es escasa.** Las corridas de evaluación
  alientan y son chicas: ver [evals.md](../evals.md).
- **Los scripts necesitan Python 3.8 o posterior.** Sin Python, los topes se
  miden a mano, y los rituales lo dicen.

## Actualizar desde 1.x

Las versiones 1.x fueron privadas y en español. Pedirle a un instalador su
sistema en un proyecto que ya lo tiene inicia una actualización: conserva los
nombres de archivo del proyecto (un proyecto 1.x mantiene sus nombres en
español), reemplaza el contenido de los scripts y el bloque de reglas,
conserva cada entrada de la historia y muestra cada cambio para tu OK. El
`CHANGELOG.md` de cada skill lista los pasos exactos.

## Preguntas

**¿Reemplaza la memoria de mi agente?** No. La memoria automática recuerda
hechos sobre ti; tino lleva el registro del proyecto, las lecciones que
aprobaste y una wiki crítica, en archivos que son del proyecto, y no lee esa
memoria.

**¿Funciona sin Claude Code?** Las skills siguen el formato Agent Skills y
los archivos son Markdown común, así que los agentes que leen skills o un
archivo de instrucciones del proyecto pueden usarlos. El plugin y los
controles opcionales son propios de Claude Code.

**¿Se envía algo a algún lado?** No. Ver [PRIVACY.md](../../PRIVACY.md).

**¿Hay un ejemplo terminado?** Sí: [`examples/`](../../examples).

**¿Dónde están los formatos exactos?** En [format.md](../format.md). Los
tokens fijos que figuran ahí son un contrato del que dependen los scripts.
