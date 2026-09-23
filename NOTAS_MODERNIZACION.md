# Notas del proyecto — Santa Biblia Reina Valera Interactiva

Este archivo es el punto de verdad compartido entre distintas sesiones de trabajo
(chat con Claude, Claude Code, etc.) para el sub-proyecto de **modernización del
texto RV 1909**. Actualizar aquí cada vez que se tome una decisión de estilo
importante o se resuelva un bug grande, para que cualquier sesión nueva pueda
retomar el trabajo sin perder contexto.

---

## 🎉 Estado actual: PROYECTO COMPLETO (66/66 libros)

Los **66 libros** de la Biblia (Antiguo Testamento + Nuevo Testamento) ya pasaron
por el proceso completo de modernización y relectura fina, y están subidos a GitHub.

- **Antiguo Testamento**: 35 libros ✅
- **Nuevo Testamento**: 27 libros (Mateo a Apocalipsis) ✅

> **Nota (2026-09-22):** una revisión de Esdras detectó que **Esdras, Ester y
> Nehemías** habían quedado sin modernizar (texto 1909 crudo casi completo,
> no solo las mayúsculas de inicio de capítulo), y que **1 Crónicas 14, 2
> Crónicas 13, Isaías 55 y Job 37** tenían el bug puntual de mayúscula fija de
> inicio de capítulo sin corregir (el resto de esos 4 libros sí estaba bien).
> Los 7 libros ya fueron corregidos esta sesión (ver entrada en el historial
> de sesiones más abajo). Causa probable: un lote de libros que no completó su
> pasada de modernización en su momento y quedó marcado como terminado por
> error.

---

## Estructura del proyecto

- **Repositorio:** `shonystore75-dot/santa-biblia-interactiva`
- **Ruta local:** `C:\Users\Diego\Documents\santa-biblia-interactiva`
- **Formato de archivo por libro:** `libro-XX.json` (ej. `libro-gn.json`, `libro-mt.json`, `libro-ap.json`)
- **Formato interno del JSON:** lista de capítulos, cada uno `{'c': número_capítulo, 'v': [[número_verso, texto], ...]}`

### El motor de modernización: `modernizar.py`
Un solo script con dos partes:

1. **Reglas generales** — funciones y regex que se aplican automáticamente a
   cualquier texto: ortografía arcaica, reordenamiento de pronombres pegados a
   verbos, conjugaciones arcaicas, vocabulario anticuado, capitalización de
   nombres propios al inicio de capítulo, etc.
2. **`FRASES_POR_VERSO`** — diccionario de excepciones puntuales por
   `(libro, capítulo, verso)`, para casos que las reglas generales no cubren
   o que necesitan una redacción especial.

---

## Metodología de trabajo (seguir siempre)

1. **Nunca regenerar un libro ya trabajado desde el original 1909** si ya tiene
   excepciones puntuales aplicadas — se pierde el trabajo. Usar siempre
   `modernizar_verso(libro, capítulo, verso, texto)` sobre el archivo actual,
   nunca `modernizar_texto(texto)` solo (este último NO aplica `FRASES_POR_VERSO`).
2. Al descubrir un patrón/bug nuevo, buscarlo en **toda la Biblia** (los 66
   libros) antes de decidir si conviene regla general o caso puntual, y aplicar
   retroactivamente a los libros ya procesados si corresponde.
3. Proceso por libro: (a) verificar versos vacíos o sospechosamente largos
   contra el conteo estándar conocido, (b) aplicar todas las reglas generales
   por primera vez, (c) revisar patrones ya conocidos con regex de barrido,
   (d) hacer "lectura fina" capítulo por capítulo buscando lo que se haya
   escapado, (e) revisión final exhaustiva antes de dar el libro por terminado.
4. Antes de escribir una excepción puntual nueva, **revisar el texto actual**
   del verso (puede que otra regla ya lo haya transformado parcialmente) — el
   regex de la excepción debe coincidir con el texto *tal como está*, no con
   el original crudo.
5. Verificar siempre que el script cargue sin errores de sintaxis y sin claves
   duplicadas en `FRASES_POR_VERSO` (Python se queda con la última si hay
   duplicado, sin avisar) antes de regenerar cualquier libro.
6. Trabajar autónomo sin pausar a preguntar; solo detenerse cuando el usuario
   escriba. Ante un cambio puntual señalado por el usuario, evaluar si conviene
   regla general revisando TODO lo ya hecho.

### Reestructuraciones especiales de versículos (NO perder al regenerar)
Estos libros tienen capítulos donde el original 1909 tenía versos fusionados,
vacíos o desplazados, ya corregidos a mano comparando contra RV1960/Wikisource:
- **Job** caps 38–41
- **Números** caps 12–13
- **2 Samuel** cap 20
- **Oseas** caps 11–12
- **Jonás** caps 1–2

Huecos genuinos confirmados que **no** deben tocarse: 1 Sam 23:29, 2Cr 33:25,
Job 35:16. Hueco genuino de tradición en español (no llenar): 2 Corintios 13:14.

---

## Correcciones sistémicas grandes ya resueltas

- Gentilicios mayúscula→minúscula salvo inicio de oración
- `:` a mitad/final de verso → `;` salvo verbo de habla cerca
- Nombres "ph"→"f", "th"→"t" (excepciones: Joseph→José, Bethlehem→Belén)
- Mayúscula de capítulo: reconoce "¿"/"¡" antes de la palabra en mayúsculas y
  vocales con circunflejo (`NOMBRES_PROPIOS` se sigue ampliando si aparece un
  nombre nuevo como primera palabra de capítulo — ya incluye todos los nombres
  principales del NT)
- Reglas de reordenamiento verbo+pronombre completas para todas las personas y
  tiempos (pretérito, futuro simple, futuro perifrástico arcaico "amarte
  he"→"te amaré", imperfecto, "dícele"→"le dice", etc.)
- "si" + subjuntivo futuro arcaico → indicativo presente (ej. "si dijereis"→"si decís")
- "cuando" + subjuntivo futuro arcaico → subjuntivo presente (ej. "cuando
  vinieren"→"cuando vengan") — **distinto** al tratamiento de "si"
- (2026-09-22) Extensión del caso anterior: "que"/"donde" + subjuntivo futuro en
  cláusula relativa también → subjuntivo presente, por analogía (ej. "todo lo
  que fuere necesario"→"todo lo que sea necesario", "donde peregrinare"→"donde
  peregrine"). No estaba documentado explícitamente antes de esta sesión;
  queda registrado aquí como regla general confirmada.
- (2026-09-22) La forma irregular **"fuere"** (de ser/ir, no de "hallar") con
  "si" también se resuelve, pero al indicativo presente del verbo real, no a
  una forma de "fuere" en sí (ej. "Si fuere vuestro lanzamiento"→"Si va vuestro
  lanzamiento"). El barrido original de 57 casos con endings -are/-iere no
  cubría esta forma irregular; revisar libros ya "completos" si aparece algún
  caso suelto de "fuere" que se haya escapado.
- (2026-09-22) "[Nombre] sacerdote/profeta/profetisa/escriba" → "el/la
  [título] [Nombre]": al reordenar, si el nombre iba precedido de "a"/"de" hay
  que fusionar la contracción (a+el→al, de+el→del), no dejar "a el"/"de el"
  sueltos. Bug real encontrado y corregido en Nehemías 13:13.
- Apócope "grande"→"gran" con lista de exclusión para uso predicativo
- "la mar"(femenino arcaico)→"el mar", con contracciones correctas del/al
- "Fue palabra de Jehová"→"Vino palabra de Jehová" (fórmula fija)
- Vocabulario: Jerusalem→Jerusalén, mocedad→juventud, saco(luto)→cilicio,
  ciento/mil y X→ciento/mil X, soy contigo→estoy contigo, Heme+participio→Me
  he+participio, y muchos más (ver historial de commits para el detalle completo)

## Bugs de coincidencia de letras (vigilar siempre en libros nuevos)
El patrón de letras de una regla general a veces coincide por casualidad con
una palabra que NO es lo que la regla busca. Ya encontrados y protegidos:
`case/clase/Vase`, `tóme+pron`, `parábola/diáconos/óbolos`, `córtase/échase/
hágase/levántase/quítase/Apártase/Ensúciese` (presente+se confundido con
subjuntivo -ase→-ara), `"muerte he"/"parte ha"` (sustantivo confundido con
infinitivo), `"si pare"/"cuando pare"/"cuando hiere"` (indicativo de
parir/herir confundido con subjuntivo).
- (2026-09-22) `oíase` (imperfecto "oía"+se, = "se oía") confundido con
  subjuntivo -ase→-ara; `hágase/escríbase/concédase(le)` (imperativo usted+se,
  ya en forma moderna correcta) también coincidían por casualidad con el
  patrón -ase y se protegieron en un set de excepciones.
- (2026-09-22) `constriñese` (imperfecto de subjuntivo de un verbo en -ñir) no
  coincide con el patrón general `-iese→-iera` porque la ñ absorbe la "i";
  necesita una regla propia `(\w+ñ)ese→\1era`.
- (2026-09-22) `Hízose`/`púsose` (verbo irregular+"se" reflexivo) no coinciden
  con el patrón general de pronombre pegado porque el acento no queda pegado
  justo antes del pronombre; se resuelven como vocabulario irregular puntual,
  igual que `díjole/hízole/trájolo(s)/trájola(s)`.
- (2026-09-22) `callárame` (forma arcaica "-ara"+pronombre pegado, ej. Ester
  7:4) no la cubre ninguna regla de pronombre pegado (esas solo cubren
  pretérito/futuro, no esta forma); solo apareció 1 vez en toda la Biblia —
  tratado como caso puntual.

## Ambigüedades que NUNCA deben ser regla general
- "tornar" (volver / girar-doblar / convertir) — evaluar caso por caso
- "Ammón" (hijo de David vs nación amonita) — evaluar caso por caso
- Nombre compartido entre persona/nación/lugar — nunca regla general automática

## Decisiones de estilo de Diego
- No quitar la mayúscula reverencial de "Yo"/"Él" refiriéndose a Dios
- Preferir ortografía estándar española moderna para nombres propios, no la
  que más se repita en el propio 1909
- RV1960 sirve de referencia para claridad/estructura, nunca para adoptar su
  interpretación si cambia el sentido del 1909 original

## Limitaciones pendientes de revisar (declaradas, no resueltas)
- (2026-09-22) En las listas genealógicas muy extensas de Esdras/Nehemías
  (cap. 2, 7, 8, 10, 11, 12 — repatriados, porteros, levitas) se aplicó solo
  la normalización mecánica de vocales con circunflejo (â→á, etc.) y el sufijo
  "-chías", SIN verificar cada nombre uno por uno contra una Biblia de
  referencia moderna (a diferencia del resto del proyecto, hecho verso por
  verso). Son ~20+ nombres muy secundarios; bajo riesgo pero no verificado al
  mismo estándar que el resto.
- "Sesbassar" (gobernador, Esdras 1 y 5) se dejó con su doble-s del 1909 sin
  normalizar — no había precedente ni certeza de si el estándar moderno usa
  "Sesbasar" o "Sasabasar" según la tradición.

---

## Flujo de trabajo con GitHub

1. Terminar de trabajar uno o varios libros (relectura fina completa)
2. Compartir los archivos `libro-XX.json` actualizados + `modernizar.py`
3. En PowerShell: `Copy-Item` de cada archivo desde Descargas a la carpeta del
   repo, reemplazando `libro-XX-moderno.json` por `libro-XX.json`
4. `git add` de los archivos tocados, `git commit -m "..."`, `git push`
5. Si sale error de "Unlink of file... failed": escribir "n" y cerrar/reabrir
   la terminal — ya se sabe que esto lo resuelve

---

## Cómo retomar el trabajo en una sesión nueva

1. Clonar (o verificar que ya esté clonado) el repo
   `github.com/BibleAquifer/ReinaValera1909` si se necesita reconstruir el
   texto fuente original en bruto (archivos USFM con ortografía arcaica
   genuina) — el repo del proyecto ya tiene los 66 libros *modernizados*, pero
   no guarda el original 1909 crudo por separado.
2. Leer este archivo completo antes de tocar nada.
3. Si el usuario reporta un caso que "no le cuadra": revisar el contexto
   completo del verso contra el original, decidir si es corrección puntual o
   patrón general, buscar el patrón en toda la Biblia antes de aplicar, y
   documentar la decisión aquí mismo si es una regla nueva o un cambio de
   criterio.

