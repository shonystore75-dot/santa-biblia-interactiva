// Paletas de color de la app. Se carga en el <head> de cada pantalla (antes de pintar).
// - La paleta por defecto es "turquesa" (Turquesa renovación); quien eligió Púrpura la conserva.
// - Si hay guardada una paleta antigua (clásica, esmeralda, zafiro) o desconocida, se descarta y se usa la de por defecto.
(function () {
  var VALIDOS = ['azul', 'borgona', 'olivo', 'tierra', 'purpura', 'turquesa', 'nocturna', 'marfil', 'ambar'];
  var DEFECTO = 'turquesa';
  // Barra inferior: true = cada icono sobre una placa con borde dorado (la definitiva); false = iconos sin marco.
  var MARCO_BARRA = true;
  if (MARCO_BARRA) document.documentElement.setAttribute('data-marco', 'si');

  function leerGuardada() {
    try {
      var t = localStorage.getItem('temaApp');
      if (t && VALIDOS.indexOf(t) > -1) return t;
      if (t) localStorage.removeItem('temaApp');
    } catch (e) {}
    return DEFECTO;
  }

  // Avisa a la parte nativa (Android) para que los iconos de la barra del sistema sean oscuros en Marfil.
  function avisarSistema(nombre) {
    try {
      if (window.AndroidTema && window.AndroidTema.barraNavegacionClara) {
        window.AndroidTema.barraNavegacionClara(nombre === 'marfil');
      }
    } catch (e) {}
  }

  window.temaActual = function () {
    return document.documentElement.getAttribute('data-tema') || DEFECTO;
  };

  window.aplicarTema = function (nombre) {
    if (VALIDOS.indexOf(nombre) < 0) nombre = DEFECTO;
    document.documentElement.setAttribute('data-tema', nombre);
    try { localStorage.setItem('temaApp', nombre); } catch (e) {}
    avisarSistema(nombre);
  };

  var inicial = leerGuardada();
  document.documentElement.setAttribute('data-tema', inicial);
  avisarSistema(inicial);
  document.addEventListener('DOMContentLoaded', function () { avisarSistema(window.temaActual()); });
})();
