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

- [ ] Crear cuenta de GitHub (usuario) y repositorio para el proyecto (en
      proceso — se le dieron instrucciones paso a paso).
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

## 4. Fase actual

**Fase 1 — Esqueleto de la app y primer prototipo visual** (en curso)

## 5. Próximo paso concreto

Definir nombre de la app, y construir el primer prototipo visual (pantalla
de inicio + navegación de libros/capítulos) con la temática de tierras
bíblicas, mientras el usuario termina de crear su cuenta de GitHub.

## 6. Historial de sesiones

- **Sesión 1 (2026-07-06):** Definición inicial de la idea, revisión del
  tema de derechos de autor de la Biblia, decisión de usar RV Antigua 1909,
  decisión de enfoque web-primero, creación de este documento.
