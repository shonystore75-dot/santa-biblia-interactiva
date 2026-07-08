PROJECT STATUS — App Bíblica Interactiva con Avatares IA
> Este documento se actualiza en cada sesión. Al iniciar una conversación nueva
> con Claude, pega el contenido de este archivo (o el link del repo de GitHub)
> para retomar el proyecto exactamente donde quedó.
---
1. Qué es el proyecto
App móvil (iOS/Android) basada en la Biblia, planteada como una "Biblia
interactiva": el usuario puede leer el texto bíblico y también conversar con
avatares con IA que responden preguntas, todo dentro de un ambiente visual
temático que la diferencie claramente de apps como YouVersion o Bible.is.
2. Decisiones ya tomadas
Texto bíblico: Reina Valera Antigua (1909) — dominio público, sin
restricciones de licencia. (Nota: la RV1960 es la más popular pero tiene
copyright de Sociedades Bíblicas Unidas; se evaluará migrar a esa versión
más adelante, negociando licencia comercial, una vez la app genere ingresos.)
Nivel técnico del usuario: cero experiencia en programación. Claude
construye todo el código; el usuario toma decisiones de producto y ejecuta
pasos que Claude no puede hacer directamente (crear cuentas, subir archivos,
probar la app en su teléfono, etc.).
Estrategia de plataforma: empezar como app web (HTML/CSS/JS) y
luego empacarla para móvil con Capacitor (permite convertir la misma
app web en app instalable de iOS/Android sin reescribir todo desde cero).
Editor recomendado: Visual Studio Code (gratuito), solo para ver
archivos y ejecutar la app localmente — el usuario no necesita escribir código.
Almacenamiento persistente del proyecto: GitHub (repositorio gratuito)
como "caja fuerte" del proyecto, ya que las sesiones de chat no retienen
archivos entre conversaciones distintas.
3. Pendiente de decidir
[x] Crear cuenta de GitHub y repositorio: LISTO —
https://github.com/shonystore75-punto/santa-biblia-interactiva
[x] Nombre de la app: "Santa Biblia Reina Valera Interactiva" (se
aclarará dentro de la app que el texto usado es la versión 1909,
de dominio público).
[x] Concepto/temática visual: "Tierras bíblicas" — desierto, columnas,
tonos cálidos (arena, ocre, terracota, dorado), sensación de
inmersión histórica. Los avatares "viven" visualmente en ese mundo.
[ ] Cuánto tiempo semanal puede dedicar el usuario (para calibrar ritmo).
[ ] Modelo de monetización a explorar primero (suscripción, freemium,
donaciones, licencias a iglesias, etc.) — se decidirá con más detalle
una vez haya un prototipo funcional.
[ ] Retroalimentación del usuario sobre el primer prototipo visual
(colores, nombre del avatar "Escriba", etc.)
4. Fase actual
Fase 1 — Pantalla de inicio: COMPLETA (pendiente de subir última versión)
La pantalla de inicio quedó terminada con:
Fondo con ilustración propia del usuario (templo/atardecer)
Avatar del "Escriba" con foto propia del usuario, bien encuadrada
Tarjetas "Leer" (pergamino propio) e "Historias" (holograma de Moisés
propio, formato panorámico tipo cover)
Menú inferior con 4 iconos holográficos dorados propios del usuario
(efecto `mix-blend-mode: screen` para quitar el fondo negro), tipografía
Cinzel en las etiquetas, con estado "activo" resaltado en dorado
Layout responsivo real de app nativa: todo el contenido (header +
contenido + menú) se ajusta a la altura exacta de cualquier celular
usando unidades relativas (vh, clamp, dvh) — NUNCA requiere scroll, se
ve completo en una sola pantalla en cualquier dispositivo. En
computador se sigue viendo como maqueta de teléfono con bordes
redondeados (media query >=500px).
Archivo actual y correcto: `index.html` (versión con layout fluido
sin scroll). Las 8 imágenes están en la raíz del repo (sin subcarpetas,
por facilidad de carga vía navegador): `escriba.jpg`, `fondo-inicio.jpg`,
`historias.jpg`, `nav-favoritos.png`, `nav-guia.png`, `nav-inicio.png`,
`nav-leer.png`, `pergamino.jpg`.
⚠️ PENDIENTE CRÍTICO: confirmar que la ÚLTIMA versión de `index.html`
(la del layout sin scroll, con `clamp()` y `dvh`) ya fue subida a GitHub
reemplazando la anterior. Si al retomar el proyecto no se ve el efecto de
"todo cabe en pantalla sin scroll", es porque esa versión no se subió y
hay que volver a generarla.
GitHub Pages: activado. URL pública:
https://shonystore75-dot.github.io/santa-biblia-interactiva/
(nota: puede tardar 1-2 min en reflejar cambios nuevos tras cada commit;
si no se ven cambios, probar en ventana de incógnito).
5. Próximo paso concreto
Confirmar que el índex.html final quedó subido y se ve bien en el
celular real del usuario.
Definir si seguimos afinando la pantalla de inicio o pasamos a
construir la siguiente pantalla real: navegación de libros/capítulos
con el texto de la RV Antigua 1909 (aún no se ha empezado a trabajar
el contenido bíblico en sí, todo lo hecho hasta ahora es la pantalla
de inicio/portada).
6. Lecciones aprendidas (para no repetir errores)
Las imágenes deben comprimirse SIEMPRE antes de incrustarlas (usar
JPEG calidad ~70-75 y redimensionar a un ancho máximo razonable según
el uso: ~900px fondos, ~500px tarjetas/avatar, ~150px iconos). Nunca
incrustar imágenes originales sin comprimir en base64: el archivo
puede pesar decenas de MB y no cargar bien.
Al subir a GitHub desde el navegador, es más confiable subir archivos
sueltos (sin subcarpetas) que arrastrar carpetas completas, porque el
usuario no tiene experiencia técnica y es fácil que la carpeta no se
suba con su estructura interna correctamente.
El diseño debe pensarse desde el inicio como "app real de celular"
(usando vh/dvh/clamp, layout que llena la pantalla real) y NO como una
"maqueta de teléfono dentro de una página de escritorio" (con tamaños
fijos en píxeles) — esto último se ve mal y de forma inconsistente al
abrir en un celular real.
6. Historial de sesiones
Sesión 1 (2026-07-06): Definición inicial de la idea, revisión del
tema de derechos de autor de la Biblia, decisión de usar RV Antigua 1909,
decisión de enfoque web-primero, creación de este documento.
