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
- **Nombre de la app:** "Santa Biblia Reina Valera Interactiva" (dentro de
  la app se aclara que el texto usado es la versión 1909, de dominio público).
  Para la edición del texto modernizado en sí, se usará el nombre **"Santa
  Biblia 2026"** (se descartó "RV 2026" por posible conflicto de marca con
  Reina-Valera).
- **Repositorio:** https://github.com/shonystore75-dot/santa-biblia-interactiva
  — ruta local: `C:\Users\Diego\Documents\santa-biblia-interactiva`
- **Concepto/temática visual:** "Tierras bíblicas" — desierto, columnas,
  tonos cálidos (arena, ocre, terracota, dorado), sensación de inmersión
  histórica. Los avatares "viven" visualmente en ese mundo.
- **Estructura de archivos:** todo el proyecto (código, imágenes, datos JSON)
  vive en archivos sueltos en la raíz del repo, sin subcarpetas — decisión
  deliberada porque subir carpetas completas desde el navegador sin
  experiencia técnica es propenso a errores.
- **Stack confirmado:** HTML/JS/JSON puro (no React Native ni Flutter).

## 3. Modelo de monetización (definido)

- App de acceso gratis, con **publicidad intercalada** como fuente principal
  de ingresos.
- Planes de pago **simplificados en 3 niveles** (para no tener una lista
  larga de opciones), cada uno disponible en periodicidad mensual, semestral
  y anual (con descuento por compromiso más largo):
  1. **Sin publicidad** (sin acceso extra al Escriba)
  2. **Plan básico** — sin publicidad + acceso al Escriba (~3 preguntas/día,
     ≈90/mes) — nombre pendiente de definir (no "Premium", ya reservado)
  3. **Plan alto** — sin publicidad + acceso al Escriba (~8-10 preguntas/día,
     ≈250-300/mes) — nombre pendiente de definir
- Precios de referencia explorados (a validar con costo real de API antes de
  fijar definitivos): Sin publicidad ~$1.99/mes; Básico ~$2.99/mes; Alto
  ~$5.99/mes, con descuentos en semestral/anual. Investigación de mercado
  mostró que apps similares (Bible Gateway Plus, Logos, etc.) cobran entre
  $3.99 y $19.99/mes, por lo que hay margen para ajustar precios al alza si
  se desea, especialmente en el plan alto (el Escriba conversacional es un
  diferenciador que otras apps de ese rango no tienen).
- También se ofrecerán **donaciones voluntarias**, usando el mismo método de
  pago que la versión sin publicidad, para quienes quieran contribuir sin
  necesariamente pagar por quitar publicidad.
- **Prueba gratuita del Escriba:** 1 pregunta al día durante 7 días (una sola
  vez, al instalar). Al terminar la prueba, si el usuario no paga, el Escriba
  se **bloquea por completo** (no se reduce a un límite menor) — decisión
  tomada por control de costos, ya que no se puede asumir que la publicidad
  cubra el gasto de IA de usuarios sin pagar.
- Mecanismo de bloqueo requiere cuenta de usuario identificable (no basta con
  atarlo al dispositivo, se resetea desinstalando/reinstalando). La
  validación de límite debe pasar ANTES de llamar a la API de IA, para no
  gastar en usuarios bloqueados.

## 4. Diseño del asistente "Pregúntale al Escriba"

- Se mantiene el nombre **"Escriba"**.
- **Alcance de las respuestas** (importante — sin entrar en terreno
  doctrinal): puede explicar significado del texto y dar contexto
  histórico/cultural de la época, pero NO debe dar aplicación personal,
  consejo espiritual/moral, ni entrar en debates entre tradiciones o
  denominaciones. Esto es coherente con la sección de Preguntas y Respuestas
  planeada (ver punto 6), que también será exclusivamente sobre versículos,
  sin explicaciones doctrinales.
- **Control de costos en las respuestas:** deben ser breves (pensadas para
  voz, no para lectura larga), con límite duro de tokens en la llamada a la
  API, y el Escriba debe reconocer preguntas demasiado amplias (ej.
  "explícame toda la Biblia") y pedir que se acoten, en vez de intentar
  responder de forma truncada.
- **Diseño visual y animación labial:**
  - El Escriba es un hombre (ilustración estilo Medio Oriente antiguo,
    turbante, con un rollo/pergamino), imagen base 500x500px.
  - Se generaron con IA **6 variantes de expresión de boca** (mismo
    encuadre/pose) con fondo transparente, más un fondo fijo (ciudad al
    atardecer) por separado — permite animar solo la boca sin mover el
    resto de la imagen.
  - Las 6 variantes se normalizaron en color/tono con Python (estaban algo
    dispares entre generaciones) y se redimensionaron a 500x500px.
  - Se probó un demo funcional real: HTML + JS usando la Web Audio API
    (`AnalyserNode`) para medir el volumen del audio en tiempo real y
    alternar entre las 6 variantes de boca según el nivel de sonido
    ("lipsync" básico por amplitud, no por fonemas — enfoque económico
    tipo "doblaje", suficiente para el estilo de ilustración de la app).
  - **Resultado de la prueba:** funciona (audio se reproduce, boca se
    mueve), pero el efecto de "agrandarse/achicarse" de la imagen al
    cambiar de variante no se ve bien — pendiente de pulir la transición.
  - Idea de diseño complementaria: una figura con velo cubriéndose la boca
    (estilo Medio Oriente antiguo) se descartó para el Escriba (se mantiene
    como hombre que sí habla) y se reservó para el avatar de "Guía" (ver
    punto 5), donde resuelve de forma natural la necesidad de lipsync.
- **Nivel técnico pendiente de definir:** integración real de STT (voz del
  usuario a texto), motor conversacional (Claude vía API + probablemente
  RAG sobre el texto de Santa Biblia 2026, para que el Escriba no use
  conocimiento bíblico externo ni otras versiones), y TTS (texto a voz).

## 5. Diseño de la sección "Guía"

- El ícono de "Guía" ya sugiere un avatar/personaje propio (una persona),
  distinto del Escriba.
- **Diferenciación de roles:**
  - **Escriba** = conversación libre bajo demanda del usuario (reactivo).
  - **Guía** = contenido curado y propuesto proactivamente por la app, con
    personalidad de acompañamiento (no responde preguntas libres).
- **Contenido planeado dentro de Guía:**
  - Devocional diario (lectura corta + contexto, organizado por día).
  - Recorridos temáticos (pasajes agrupados por tema: paz, perdón, familia).
  - Colección de oraciones específicas de personajes bíblicos (además de
    los Salmos — ej. oración de Ana, de Salomón, de Jonás, el Padre
    Nuestro, etc.).
- **Diseño visual:** se propone una mujer con velo cubriéndose la boca
  (estética Medio Oriente antiguo) como avatar de la Guía — evita la
  necesidad de sincronización labial precisa y le da identidad visual
  propia frente al Escriba.

## 6. Estado actual de las pantallas/funcionalidades

- **Pantalla de inicio / splash screen:** existe un primer diseño (título,
  versículo del día, accesos a Leer/Historias, sección Conversar con el
  Escriba), pero falta la pantalla de inicio o splash screen propiamente
  dicha (previa a la pantalla principal).
- **"Acerca de esta versión":** pendiente de crear — debe incluir la nota de
  créditos/procedencia (basada en RV 1909, dominio público, con revisión y
  actualización de lenguaje).
- **"Pregúntale al Escriba":** aún no funciona (ver punto 4 para el diseño
  ya definido).
- **"Guía":** aún no funciona (ver punto 5 para el diseño ya definido).
- **"Versículo de hoy":** no rota automáticamente todavía, falta implementar
  la lógica de cambio diario.
- **"Historias":** tiene 12 historias escritas, todas con la misma imagen
  repetida (falta variarlas/organizar mejor visualmente); tiene un botón de
  audio que no funciona. Se quiere integrar ahí los shorts de un canal de
  YouTube que el usuario está creando, reproducidos DENTRO de la app (sin
  salir a YouTube), con opción de repetir el short o volver a la app al
  salir — falta definir cómo integrar técnicamente ese llamado a los videos.
- **Doble entrada "Leer":** hay dos accesos que dicen "Leer" y ambos llevan
  actualmente a la misma pantalla. Se quiere diferenciar: uno como el menú
  tradicional de libros/capítulos (YA ESTÁ COMPLETO Y FUNCIONANDO — tabs
  Antiguo/Nuevo Testamento, lista de libros, grid de capítulos, navegación
  Anterior/Siguiente), y otro con un **orden de lectura relacionado/
  cronológico** (ej. según qué profeta vivió en la época de qué rey), que
  guarde el avance de lectura del usuario — este segundo aún no existe.
- **Tamaño de letra ajustable:** falta como opción de accesibilidad en la
  pantalla de lectura.
- **Preguntas y respuestas:** sección pendiente de crear, basada
  exclusivamente en versículos de la Biblia, sin explicaciones doctrinales
  (mismo criterio que el Escriba).
- **Favoritos:** pendiente (guardar versículos/capítulos).

## 7. Fase actual y próximo paso concreto

**Fase 2 — Pantalla "Leer" (menú tradicional): COMPLETA Y FUNCIONANDO** ✅

**Fase 3 — En curso: diseño y prototipo del avatar "Escriba"**
- Ya resueltas: imágenes base + variantes de boca + lógica de animación
  labial por volumen de audio (demo funcional probado con éxito).
- Pendiente inmediato: pulir la transición entre variantes de boca (se ve
  como "agrandarse/achicarse" en vez de un cambio suave — hay que ajustar
  el CSS/JS de la animación).
- Pendiente después: definir e integrar STT + motor conversacional (Claude
  API, probablemente con RAG sobre el texto propio) + TTS; luego aplicar la
  lógica de límites de uso (prueba gratuita / planes pagos) definida en el
  punto 3.

**Otras pantallas pendientes de construir (sin orden definido aún):**
(a) Guía (devocional, temas, oraciones bíblicas)
(b) Historias (reorganización + integración de shorts de YouTube)
(c) Favoritos
(d) Pulir Leer: buscador de versículos, guardar último capítulo leído,
    tamaño de letra ajustable, compartir versículo
(e) Segunda modalidad de "Leer" (orden cronológico con progreso guardado)
(f) Splash screen / pantalla de inicio
(g) "Acerca de esta versión" (créditos)
(h) Preguntas y respuestas (solo texto bíblico)
(i) Sistema de monetización (publicidad, planes de pago, límites de uso)

## 8. Lecciones aprendidas (para no repetir errores)

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
- Al generar imágenes con IA para variantes de un mismo personaje (ej.
  distintas expresiones), el color/tono puede variar entre generaciones
  aunque la pose sea consistente — conviene normalizar color (histogram
  matching) antes de usarlas juntas en una animación.
- Al probar archivos HTML con audio/JavaScript localmente, abrir el
  archivo directo con doble clic (protocolo `file://`) puede causar
  bloqueos de seguridad del navegador. Es más confiable servirlo con un
  servidor local simple (`python -m http.server`) y abrirlo vía
  `http://localhost:...`.
- Antes de asumir un bug de código, descartar primero el archivo de
  audio/medio en sí (probar con un reproductor nativo simple, sin lógica
  personalizada) — un archivo de audio corrupto o silencioso puede
  parecer un error de JavaScript cuando no lo es.

## 9. Historial de sesiones

- **Sesión 1 (2026-07-06):** Definición inicial de la idea, revisión del
  tema de derechos de autor de la Biblia, decisión de usar RV Antigua 1909,
  decisión de enfoque web-primero, creación de este documento.
- **Sesión(es) posteriores (Claude Code, hasta ~2026-07-31):** Construcción
  y modernización completa del texto de los 66 libros (ver
  `NOTAS_MODERNIZACION.md` para el detalle técnico de ese sub-proyecto);
  pantalla de inicio; pantalla "Leer" (menú tradicional) completa y
  funcionando.
- **Sesión de chat (2026-08-15/16, esta sesión):** Definición de nombre
  final "Santa Biblia 2026" para la edición del texto; nota de créditos;
  decisiones de monetización (publicidad + 3 planes de pago simplificados +
  donaciones, con periodicidad mensual/semestral/anual); diseño conceptual
  completo del Escriba (alcance sin doctrina, límites de uso y costos,
  nombre mantenido); diferenciación de roles Escriba vs. Guía y contenido
  de Guía (devocional, temas, oraciones bíblicas); generación y
  normalización de 6 variantes de boca del Escriba + fondo; demo funcional
  de animación labial por audio (Web Audio API) probado con éxito, con
  transición pendiente de pulir.
