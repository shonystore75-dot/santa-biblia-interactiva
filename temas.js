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
  // hasta que esta avisa. Se avisa en cuanto lo imprescindible esta listo (fondo, encabezado y barra con sus
  // iconos, ya decodificados). Las fuentes y el contenido solo se esperan hasta LIMITE_MS desde que empezo la
  // carga, y las imagenes secundarias no se esperan: lo que falte aparece despues (el contenido, sobre las
  // siluetas de .cargando). Una pantalla puede retrasar el aviso (dentro de ese limite) con window.esperaPantalla.
  var LIMITE_MS = 150;
  var ESPERA_MAXIMA_MS = 1200;   // tope si algo falla

  function sinCargando(vencido) {
    return new Promise(function (listo) {
      (function mirar() { if (!vencido() && document.querySelector('.cargando')) requestAnimationFrame(mirar); else listo(); })();
    });
  }

  // decodifica los fondos de lo imprescindible: pantalla, encabezado, barra inferior e iconos
  function imagenesPrincipales() {
    var urls = {};
    function anotar(valor) {
      var re = /url\("([^"]+)"\)/g, m;
      while ((m = re.exec(valor))) if (m[1].indexOf(location.origin) === 0 || m[1].indexOf('data:') === 0) urls[m[1]] = true;
    }
    Array.prototype.forEach.call(document.querySelectorAll('.phone, header, nav, .icono-nav'), function (el) {
      anotar(getComputedStyle(el).backgroundImage);
      anotar(getComputedStyle(el, '::before').backgroundImage);
      anotar(getComputedStyle(el, '::after').backgroundImage);
    });
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
      // un fotograma para que lo ultimo se aplique; la parte nativa ademas espera a que este dibujado
      requestAnimationFrame(function () {
        try { if (window.AndroidTema && window.AndroidTema.pantallaLista) window.AndroidTema.pantallaLista(); } catch (e) {}
      });
    }
    setTimeout(avisar, ESPERA_MAXIMA_MS);
    var vencido = false;
    var limite = new Promise(function (listo) {
      setTimeout(function () { vencido = true; listo(); }, Math.max(0, LIMITE_MS - performance.now()));
    });
    var contenido = Promise.resolve(window.esperaPantalla)
      .then(function () { return sinCargando(function () { return vencido || avisado; }); });
    var resto = Promise.all([contenido, document.fonts && document.fonts.ready]);
    Promise.all([imagenesPrincipales(), Promise.race([resto, limite])]).then(avisar, avisar);
  });
})();
