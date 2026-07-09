# PROJECT STATUS — App Bíblica Interactiva con Avatares IA

> Este documento se actualiza en cada sesión. Al iniciar una conversación nueva
> con Claude, pega el contenido de este archivo (o el link del repo de GitHub)
> para retomar el proyecto exactamente donde quedó.

---

## 1. Qué es el proyecto

App móvil (iOS/Android) basada en la Biblia, planteada como una "Biblia
interactiva": el usuario puede leer el texto bíblico y también conversar con
avatares con IA que responden preguntas, todo dentro de un ambiente visual
temático que la diferencie claramente de apps como YouVersion o Bible.is.

## 2. Decisiones ya tomadas

- **Texto bíblico:** Reina Valera Antigua (1909) — dominio público, sin
  restricciones de licencia. (Nota: la RV1960 es la más popular pero tiene
  copyright de Sociedades Bíblicas Unidas; se evaluará migrar a esa versión
  más adelante, negociando licencia comercial, una vez la app genere ingresos.)
- **Nivel técnico del usuario:** cero experiencia en programación. Claude
  construye todo el código; el usuario toma decisiones de producto y ejecuta
  pasos que Claude no puede hacer directamente (crear cuentas, subir archivos,
  probar la app en su teléfono, etc.).
- **Estrategia de plataforma:** empezar como **app web** (HTML/CSS/JS) y
  luego empacarla para móvil con **Capacitor** (permite convertir la misma
  app web en app instalable de iOS/Android sin reescribir todo desde cero).
- **Editor recomendado:** Visual Studio Code (gratuito), solo para ver
  archivos y ejecutar la app localmente — el usuario no necesita escribir código.
- **Almacenamiento persistente del proyecto:** GitHub (repositorio gratuito)
  como "caja fuerte" del proyecto, ya que las sesiones de chat no retienen
  archivos entre conversaciones distintas.

## 3. Pendiente de decidir

- [x] Crear cuenta de GitHub y repositorio: **LISTO** —
      https://github.com/shonystore75-punto/santa-biblia-interactiva
- [x] Nombre de la app: **"Santa Biblia Reina Valera Interactiva"** (se
      aclarará dentro de la app que el texto usado es la versión 1909,
      de dominio público).
- [x] Concepto/temática visual: **"Tierras bíblicas"** — desierto, columnas,
      tonos cálidos (arena, ocre, terracota, dorado), sensación de
      inmersión histórica. Los avatares "viven" visualmente en ese mundo.
- [ ] Cuánto tiempo semanal puede dedicar el usuario (para calibrar ritmo).
- [ ] Modelo de monetización a explorar primero (suscripción, freemium,
      donaciones, licencias a iglesias, etc.) — se decidirá con más detalle
      una vez haya un prototipo funcional.
- [ ] Retroalimentación del usuario sobre el primer prototipo visual
      (colores, nombre del avatar "Escriba", etc.)

## 4. Fase actual

**Fase 2 — Pantalla "Leer": COMPLETA Y FUNCIONANDO** ✅

- Texto completo de la Reina Valera 1909 (66 libros, dominio público) obtenido
  del repositorio open-source `scrollmapper/bible_databases` (licencia MIT),
  convertido a JSON propio: `indice.json` (metadata de los 66 libros) +
  `libro-xx.json` por cada libro (nombres cortos: gn, ex, lv... ap).
- Pantalla `leer.html`: tabs Antiguo/Nuevo Testamento → lista de libros →
  grid de capítulos → texto del capítulo con navegación Anterior/Siguiente.
  Mismo estilo visual que la pantalla de inicio (Cinzel, paleta dorado/
  terracota/ciruela).
- Botón "Leer" del menú inferior y la tarjeta "Leer" de inicio ya enlazan
  correctamente a esta pantalla.
- Bug corregido: el botón "atrás" no reseteaba el capítulo activo y se
  quedaba trabado; ya funciona la navegación completa (capítulo → lista de
  capítulos → lista de libros).
- Todos los archivos son sueltos en la raíz del repo (sin subcarpetas),
  por la limitación de subida vía navegador del usuario.

**Fase 1 — Pantalla de inicio:** completa (ver historial de sesiones
anteriores).

## 5. Próximo paso concreto

Definir cuál construir a continuación:
(a) Pantalla del "Escriba" (chat con IA sobre pasajes bíblicos) — es el
    diferenciador principal de la app, aún no se ha empezado.
(b) Pantalla "Historias" (relatos ilustrados).
(c) Pantalla "Favoritos" (guardar versículos/capítulos).
(d) Pulir "Leer": buscador de versículos, guardar último capítulo leído,
    tamaño de letra ajustable, compartir versículo.

## 6. Lecciones aprendidas (para no repetir errores)

- Las imágenes deben comprimirse SIEMPRE antes de incrustarlas (usar
  JPEG calidad ~70-75 y redimensionar a un ancho máximo razonable según
  el uso: ~900px fondos, ~500px tarjetas/avatar, ~150px iconos). Nunca
  incrustar imágenes originales sin comprimir en base64: el archivo
  puede pesar decenas de MB y no cargar bien.
- Al subir a GitHub desde el navegador, es más confiable subir archivos
  sueltos (sin subcarpetas) que arrastrar carpetas completas, porque el
  usuario no tiene experiencia técnica y es fácil que la carpeta no se
  suba con su estructura interna correctamente. Por eso TODO el proyecto
  (código, imágenes, datos JSON) vive en archivos sueltos en la raíz.
- El diseño debe pensarse desde el inicio como "app real de celular"
  (usando vh/dvh/clamp, layout que llena la pantalla real) y NO como una
  "maqueta de teléfono dentro de una página de escritorio" (con tamaños
  fijos en píxeles) — esto último se ve mal y de forma inconsistente al
  abrir en un celular real.
- Antes de dar por buena una función de navegación (botones atrás,
  cambios de vista), revisar mentalmente TODOS los estados posibles
  (no solo el primer clic) — el bug del botón atrás pasó por no resetear
  una variable de estado al cambiar de vista.

## 6. Historial de sesiones

- **Sesión 1 (2026-07-06):** Definición inicial de la idea, revisión del
  tema de derechos de autor de la Biblia, decisión de usar RV Antigua 1909,
  decisión de enfoque web-primero, creación de este documento.
