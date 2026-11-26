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
- **Sesión de chat (2026-09-22, esta sesión):** Diego detectó mayúsculas fijas
  al inicio de los capítulos de Esdras; al revisar se encontró que Esdras,
  Ester y Nehemías habían quedado sin modernizar (texto 1909 casi crudo), y
  que 1 Crónicas 14, 2 Crónicas 13, Isaías 55 y Job 37 tenían el mismo bug
  puntual de mayúscula fija en un solo capítulo cada uno (el resto de esos 4
  libros ya estaba bien). Se reconstruyó el motor de modernización desde cero
  (el `modernizar.py` avanzado de sesiones anteriores se había perdido; solo
  quedaba en GitHub una versión básica de 148 líneas) aplicando todas las
  reglas documentadas en `NOTAS_MODERNIZACION.md`, más varias reglas y bugs
  nuevos encontrados y corregidos en el proceso (ver ese archivo para el
  detalle técnico completo). Los 7 libros quedaron modernizados y verificados
  con lectura completa; cambios subidos a GitHub.

## PALETAS DE COLOR (2026-11-22)
- 9 paletas en `temas.css` (variables CSS), generado por `python scripts/generar-temas.py` (ahí están los colores base, los derivados y la tabla de contraste). NO editar `temas.css` a mano.
- `temas.js` (cargado en el `<head>` de cada pantalla) valida la paleta guardada (`localStorage.temaApp`); por defecto `turquesa` (`PALETA_POR_DEFECTO` en el generador); las antiguas (clásica/esmeralda/zafiro) pasan a Púrpura.
- Marfil clásico usa la textura `marmol_marfil_2026-11-22_2110.webp` (variable `--textura`; `none` en las demás). Iconos de la barra inferior (2026-11-25): `nav-<inicio|leer|guia|favoritos>-<oro|bronce>.webp`, recortados y recoloreados por `scripts/generar-iconos-barra.py` desde `resources/iconos/iconos-dorados-fuente.png` (bronce solo en Marfil; el engranaje queda en `resources/iconos/`, fuera de la app). Variante con placa detrás de cada icono: `MARCO_BARRA` en `temas.js`. Segunda pasada (mismo día): archivos de 512 px, rampa con más relieve y resplandor solo en la pestaña activa (en las inactivas difuminaba los bordes); los `nav-*.png` antiguos se borraron. Tercera pasada (mismo día): la placa es la variante definitiva (`MARCO_BARRA = true`), 54x36 px con el dibujo a 28 px; ningún resplandor sobre el dibujo: la pestaña activa se distingue por el borde grueso y luminoso, el halo de la placa y la etiqueta (variables `--marco-*` en `generar-temas.py`). Los estilos antiguos de `.icono-nav` se quitaron de las páginas. **Parpadeo entre pantallas (2026-11-25):** cada pantalla se pintaba antes que sus imágenes, fuentes y datos (ya ocurría antes de los íconos nuevos). `MainActivity` deja una copia de la pantalla anterior (PixelCopy, Android 8+) y la funde en 90 ms cuando `temas.js` llama a `AndroidTema.pantallaLista()` (tope 1,2 s en JS y 1,5 s nativo). Se avisa con fondo, encabezado y barra decodificados; fuentes, contenido (`.cargando`, que muestra siluetas de tarjetas) y `window.esperaPantalla` solo se esperan hasta `LIMITE_MS` (150 ms desde la carga). Durante el cambio, el último toque en la barra inferior se guarda en `MainActivity` y se aplica al terminar (la WebView lo descartaría). Mediana medida toque → fundido: ~250–290 ms (antes ~355). Cada HTML lleva un `<style id="critico">` generado por `generar-temas.py` (un HTML nuevo lo recibe al ejecutarlo). Íconos de la barra ahora de 192 px (~81 KB los 8).
- **Pulsación de botones (2026-11-25):** la «sombra cuadrada» era el resaltado de toque de Android (`-webkit-tap-highlight-color`). Se quita en toda la app desde la sección «Pulsacion de botones» de `generar-temas.py`, que también da el efecto propio: redondos con escala 0,95, brillo 0,9 y halo dorado; rectangulares y tarjetas, oscurecimiento leve. Un botón nuevo debe añadirse a esas listas; no usar `background` en `:active` (borra la textura).
- **Glosario y publicidad (2026-11-26):** en el Glosario la lista (`#lista-glosario`) se desplaza por debajo del buscador y el contador, así que nada pasa por detrás (reglas en `generar-temas.py`; si algún código necesita la posición de la lista, ya no es `main`). El recuadro de publicidad de Glosario y Favoritos usaba reglas antiguas con letra monoespaciada: ahora la hoja compartida lo iguala al de Leer.
- **Título del encabezado (2026-11-26):** en Tierra el bloque título/subtítulo sube 18 px (12 + 6 pedidos después; variable `--subir-extra` para los títulos largos). En las pantallas con botones A−/A+ (Leer, Glosario), `temas.js` mantiene en una línea los títulos largos: si no caben, suben lo justo para pasar por encima de los botones y, si llegarían al menú, reduce la letra (mínimo 13 px).
- **Números de versículo (2026-11-26):** serif en negrita (0,86 del texto, escalan con A−/A+) con subrayado dorado, en las 9 paletas (Leer y Oraciones); reglas en `generar-temas.py`. Sustituyen al número monoespaciado en superíndice.
- **Recuadro de publicidad (2026-11-26):** etiqueta «Publicidad» montada sobre el borde superior y texto debajo con separación, igual en todas las pantallas (reglas en `generar-temas.py`).
- **Velo tras el título (Tierra y Olivo):** oscurecimiento difuso sin contorno (color e intensidad en `velo_texto`, función `mascara` de `generar-temas.py`); los títulos largos llevan además su propio velo. En Tierra el velo es claro (0,40, pedido de Diego) y la legibilidad la completan las sombras de letra (`sombra_titulo`, `sombra_sub`) y un dorado más claro en el subtítulo.
- **Mantener presionado (2026-11-25):** el aviso con la dirección era la sombra de arrastre de un `<a href>`. `temas.js` anula `dragstart` en enlaces e imágenes y `contextmenu` en navegación, botones y tarjetas (lista `SIN_MENU`); `temas.css` quita arrastre y selección en enlaces, encabezado, barra y tarjetas del Glosario. El texto de lectura sigue siendo seleccionable. Un botón nuevo que no sea `<button>` ni `<a>` debe añadirse a `SIN_MENU`.
- **Franja inferior de Tierra bíblica (2026-11-26, aprobada por Diego):** una sola piedra (`texturas/piedra_tierra_franja.webp`, de `scripts/generar-franja-tierra.py`) cubre la barra y la zona de Android, con marco dorado redondeado, separadores, iconos sin placa y luz cálida en la pestaña activa. Los estilos están en `FRANJA` de `generar-temas.py` (clave `franja=True`); sustituyen a `barra_tierra.webp` y `piedra_tierra_android.webp`. Sin laureles (el instructivo solo pedía conservarlos si existían).
- Android: `MainActivity` expone `AndroidTema.barraNavegacionClara(boolean)`; Marfil pone iconos oscuros en la barra de navegación del sistema.

## PENDIENTE DE QUITAR ANTES DE PUBLICAR
- `historias.html`: opción de menú "Ver la guía de nuevo (prueba)" y su manejador. Buscar los comentarios `PRUEBA_TEMPORAL_INICIO` / `PRUEBA_TEMPORAL_FIN` (2 bloques: HTML del menú y JS) y borrarlos. También el modo `?guia=1` en `prepararAyudasDetalle()` (opcional).
- `historias.html`: opción de menú "Reiniciar la mano (prueba)" (borra `manoSuscribirVeces` y `manoSuscribirToco`). Está dentro de los mismos bloques `PRUEBA_TEMPORAL_INICIO` / `PRUEBA_TEMPORAL_FIN` (HTML del menú y JS): se quita junto con "Ver la guía de nuevo (prueba)".

## ESTADO DEL SISTEMA DE TEXTURAS Y ÚLTIMAS ENTREGAS (2026-11-23)
**Hecho**
- Texturas reales (mismo método: desplazamiento aditivo del color medio, una sola imagen sin mosaico, WebP optimizado) en tres paletas, todo generado desde `scripts/generar-temas.py` (`REAL` para Turquesa y Borgoña; Azul tiene su propio bloque):
  - **Azul clásico:** cuero (`texturas/cuero_azul_realista.webp`, `scripts/generar-cuero-realista.py`), papel y algodón en tarjetas, sombras suaves.
  - **Fondo (corregido):** cada paleta debe definir `--repeticion-fondo` y `--posicion-fondo`; si faltan se heredan las de Turquesa (`:root`) y el mosaico se dibuja una sola vez (rectángulo gris en Azul, mármol cortado en Marfil, desde `5cfd4c1`). El fondo de Azul usa `texturas/papel_azul_fondo.webp` (opaco, media #F7F5F0, grano x3; `scripts/generar-papel-azul.py`).
  - **Turquesa renovación:** cuero fino en encabezado y barra, papel tenue en fondo y tarjetas, cuero oscuro en los botones redondos del encabezado y el botón flotante de Leer (`scripts/generar-texturas-turquesa.py`).
  - **Borgoña real:** piedra con vetas en encabezado y barra (la barra usa la franja `right 50%`), papel tenue, piedra oscura en los botones (`scripts/generar-texturas-borgona.py`, las genera con PIL; las del zip eran un espejo simétrico y se descartaron).
  - **Verde olivo** (2026-11-24): paisaje con olivo y pradera en el encabezado (anclado a la derecha, oscurecimiento solo detrás del título), barra inferior con relieve de piedra (media #354609), piedra verde detrás de los botones de Android, papel marfil tenue, textura oscura en los botones (`scripts/generar-texturas-olivo.py <carpeta extraída del zip>`; usa recortes sin espejo para barra y botones). Colores nuevos: fondo #FEF1D6, tarjeta #FFFDF2, tinta #202815, principal #354609, dorado #D9A62C. Sin añadir aún: rama de olivo, barra redondeada, placas de versículo, rombo, paisaje en publicidad, curva del encabezado.
  - **Tierra bíblica** (2026-11-24): mismo tratamiento que Verde olivo (`scripts/generar-texturas-tierra.py <carpeta extraída del zip>`). El encabezado se recompone desde `fondo_reconstruido` (árbol + valle + casa; empedrado de la parte baja derecha dibujado por el script); papel marfil tenue, botones con piedra oscura, y empedrado de arenisca (dibujado por el script) en la barra inferior y tras los botones de Android; la madera se descartó. Colores: fondo #FAF1E3, tarjeta #FFFAF0, tinta #392419, principal #482B1D, dorado #D4A650. Sin añadir: ramas doradas, paisaje de publicidad, barra redondeada, curva del encabezado, rombo.
- Velo del hero de Inicio a 0,85 (`--velo-hero-intensidad`, tintado con el color de cada paleta).
- Glosario: botones A−/A+ con la misma clave `escalaTexto` y límites que Leer; términos y definiciones con la misma tipografía, tamaño base e interlineado que los versículos.
- Video corto de "Jacob y Esaú" (`DqGUEMvtCSY`) añadido a `historias.json`.
- Las otras paletas no se tocaron (se verificó que sus bloques de `temas.css` son idénticos).

**Paletas pendientes del sistema de texturas:** Púrpura espiritual, Nocturna, Ámbar inspirador y Marfil clásico (Marfil conserva el mármol).

**Pendientes**
- Decidir el morado de Púrpura: #49325F o #5B2C6F.
- Elementos de diseño de la referencia de Borgoña que NO se han añadido: placas de los números de versículo, rombo central, separadores de la barra inferior, borde del recuadro de publicidad (y el aro dorado más brillante de los botones).
- Esquinas ornamentales.
- Probar el video de Jacob y Esaú en el teléfono (reproducción, pantalla completa, guía de la primera vez, Suscribirse).
- Quitar los ítems de prueba del menú ("Ver la guía de nuevo (prueba)" y "Reiniciar la mano (prueba)") antes de publicar (ver la sección anterior).

## COMPARTIR VERSÍCULO COMO IMAGEN (2026-11-26)
- Al tocar compartir en un versículo de Leer se abre una hoja con las miniaturas de los estilos y «Solo texto» (`compartir.js`); el último elegido se guarda en `compartirEstilo`.
- Estilos en `compartir-estilos.js` (1080×1080: «Clásico», con marco, y «Pergamino», sin marco). **Agregar uno = añadir un objeto a `ESTILOS_COMPARTIR`**: `id`, `nombre`, `fuentes` (opcional) y `dibujar(ctx, {palabras, cita, pie})`, que devuelve `false` si el texto no cabe (usar `LienzoTexto.ajustar` / `dibujar`). Una letra nueva se declara en `FUENTES_COMPARTIR` y se guarda en `fuentes/`.
- Letra Source Serif 4 incluida en `fuentes/` (OFL). Plugin nuevo: `@capacitor/filesystem` (temporales en la caché, carpeta `compartir`). La imagen se envía en JPEG 95 %.
- Al publicar la app: rellenar `ENLACE_INSTALACION` en `compartir.js`.
- Probado en el Xiaomi: la imagen llega al menú y al selector de WhatsApp, cancelar no deja archivos y Leer va a 60 fps. Falta confirmar un envío completo.
