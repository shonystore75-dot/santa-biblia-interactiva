# Notas del proyecto — Santa Biblia Reina Valera Interactiva

Este archivo es el punto de verdad compartido entre distintas sesiones de trabajo
(chat con Claude, Claude Code, etc.) para el sub-proyecto de **modernización del
texto RV 1909**. Actualizar aquí cada vez que se tome una decisión de estilo
importante o se resuelva un bug grande, para que cualquier sesión nueva pueda
retomar el trabajo sin perder contexto.

---

## 🎉 Estado actual: PROYECTO COMPLETO

Los **66 libros** de la Biblia (Antiguo Testamento + Nuevo Testamento) ya pasaron
por el proceso completo de modernización y relectura fina, y están subidos a GitHub.

- **Antiguo Testamento**: 35 libros ✅
- **Nuevo Testamento**: 27 libros (Mateo a Apocalipsis) ✅

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

