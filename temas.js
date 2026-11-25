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

  // Precarga de los dibujos de la barra inferior de la paleta actual.
  ['inicio', 'leer', 'guia', 'favoritos'].forEach(function (n) {
    var l = document.createElement('link');
    l.rel = 'preload'; l.as = 'image'; l.href = 'nav-' + n + '-' + (inicial === 'marfil' ? 'bronce' : 'oro') + '.webp';
    document.head.appendChild(l);
  });

  // Transiciones sin parpadeo: al cambiar de pantalla la parte nativa deja a la vista la pantalla anterior
  // hasta que esta avisa de que esta completa (contenido, fuentes e imagenes visibles ya decodificadas).
  // Una pantalla puede retrasar el aviso asignando una promesa a window.esperaPantalla.
  var ESPERA_MAXIMA_MS = 1200;

  function sinCargando(vencido) {
    return new Promise(function (listo) {
      (function mirar() { if (!vencido() && document.querySelector('.cargando')) requestAnimationFrame(mirar); else listo(); })();
    });
  }

  // decodifica las imagenes de lo que esta a la vista: <img> y fondos CSS (barra, texturas, rollos...)
  function imagenesVisibles() {
    var urls = {};
    function anotar(valor) {
      var re = /url\("([^"]+)"\)/g, m;
      while ((m = re.exec(valor))) if (m[1].indexOf(location.origin) === 0 || m[1].indexOf('data:') === 0) urls[m[1]] = true;
    }
    var todos = document.body.getElementsByTagName('*');
    for (var i = 0; i < todos.length; i++) {
      var el = todos[i], r = el.getBoundingClientRect();
      if (!r.width || !r.height || r.bottom < 0 || r.top > innerHeight || r.right < 0 || r.left > innerWidth) continue;
      if (el.tagName === 'IMG' && el.currentSrc) anotar('url("' + el.currentSrc + '")');
      anotar(getComputedStyle(el).backgroundImage);
      anotar(getComputedStyle(el, '::before').backgroundImage);
      anotar(getComputedStyle(el, '::after').backgroundImage);
    }
    return Promise.all(Object.keys(urls).map(function (u) {
      var img = new Image(); img.src = u;
      return img.decode ? img.decode().catch(function () {}) : null;
    }));
  }

  document.addEventListener('DOMContentLoaded', function () {
    var avisado = false;
    function avisar() {
      if (avisado) return;
      avisado = true;
      if (window.performance && performance.mark) performance.mark('pantalla-lista');
      requestAnimationFrame(function () { requestAnimationFrame(function () {
        try { if (window.AndroidTema && window.AndroidTema.pantallaLista) window.AndroidTema.pantallaLista(); } catch (e) {}
      }); });
    }
    setTimeout(avisar, ESPERA_MAXIMA_MS);
    Promise.resolve(window.esperaPantalla)
      .then(function () { return sinCargando(function () { return avisado; }); })
      .then(function () { var imagenes = imagenesVisibles(); return Promise.all([imagenes, document.fonts && document.fonts.ready]); })
      .then(avisar, avisar);
  });
})();
