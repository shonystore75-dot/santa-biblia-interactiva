// Hoja "Compartir versículo": miniaturas de los estilos (compartir-estilos.js) y "Solo texto".
// Cada pagina que la use necesita: compartir-estilos.js, este archivo, los estilos .hoja-compartir y mostrarToast().

const NOMBRE_APP = 'Santa Biblia 2026';
const ENLACE_INSTALACION = ''; // rellenar cuando la app este publicada: se anade al mensaje que acompaña lo compartido

const Compartir = (() => {
  const CLAVE_ESTILO = 'compartirEstilo';
  const CARPETA = 'compartir'; // dentro de la cache de la app
  const TIPO = 'image/jpeg', CALIDAD = 0.95; // en el telefono: 6 veces mas ligero y cerca de 1 s mas rapido que PNG
  let enCurso = false;
  let fuentesListas = null;

  const plugins = () => (window.Capacitor && window.Capacitor.Plugins) || {};
  const esNativo = () => !!(window.Capacitor && window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform());

  // ---------- texto ----------

  // Palabras del versiculo (tal como estan en los datos) sin etiquetas ni saltos. Cada palabra es una lista de
  // tramos {texto, jesus}. El encabezado en cursiva del principio (titulo del salmo, letra hebrea) no es parte
  // del versiculo: la lectura lo muestra aparte y aqui se omite.
  function palabrasDe(html) {
    const sinEncabezado = html.replace(/^\s*<em>[\s\S]*?<\/em>\s*/i, '');
    const cuerpo = sinEncabezado.replace(/<[^>]+>/g, '').trim() ? sinEncabezado : html;
    const palabras = [];
    let actual = [];
    let jesus = false;
    const cerrar = () => { if (actual.length) palabras.push(actual); actual = []; };
    for (const pieza of cuerpo.split(/(<[^>]+>)/)) {
      if (pieza.startsWith('<')) {
        if (/^<span[^>]*palabras-jesus/i.test(pieza)) jesus = true;
        else if (/^<\/span/i.test(pieza)) jesus = false;
        else if (/^<br/i.test(pieza)) cerrar();
        continue;
      }
      pieza.split(/(\s+)/).forEach(trozo => {
        if (!trozo) return;
        if (/^\s+$/.test(trozo)) cerrar();
        else actual.push({ texto: trozo, jesus });
      });
    }
    cerrar();
    return palabras;
  }

  const unir = (palabras) => palabras.map(p => p.map(t => t.texto).join('')).join(' ');

  // Corta en dos por la puntuacion mas cercana a la mitad (si no hay, entre dos palabras).
  function partirEnDos(palabras) {
    const largos = palabras.map(p => unir([p]).length + 1);
    const total = largos.reduce((a, b) => a + b, 0);
    let mejor = null, acumulado = 0;
    for (let i = 0; i < palabras.length - 1; i++) {
      acumulado += largos[i];
      const final = unir([palabras[i]]).slice(-1);
      const castigo = '.;:?!'.includes(final) ? 0 : final === ',' ? 0.06 : 0.2;
      const nota = Math.abs(acumulado / total - 0.5) + castigo;
      if (!mejor || nota < mejor.nota) mejor = { nota, corte: i + 1 };
    }
    return mejor ? [palabras.slice(0, mejor.corte), palabras.slice(mejor.corte)] : [palabras];
  }

  // ---------- dibujo ----------

  function cargarFuentes() {
    if (!fuentesListas) {
      fuentesListas = Promise.all(FUENTES_COMPARTIR.map(async f => {
        const fuente = new FontFace(f.familia, `url('${f.archivo}')`, f.descriptores);
        await fuente.load();
        document.fonts.add(fuente);
      })).catch(e => { fuentesListas = null; throw e; });
    }
    return fuentesListas;
  }

  function dibujarUna(estilo, palabras, cita) {
    const lienzo = document.createElement('canvas');
    lienzo.width = lienzo.height = LADO_COMPARTIR;
    const ctx = lienzo.getContext('2d');
    return estilo.dibujar(ctx, { palabras, cita, pie: NOMBRE_APP }) ? lienzo : null;
  }

  // -> { lienzos: [canvas] } , { lienzos: [c1, c2], dividido: true } o null si ni en dos imagenes se lee bien
  async function generar(estilo, verso) {
    await cargarFuentes();
    await Promise.all((estilo.fuentes || []).map(f => document.fonts.load(f)));
    if (estilo.preparar) await estilo.preparar();
    const palabras = palabrasDe(verso.html);
    const una = dibujarUna(estilo, palabras, verso.referencia);
    if (una) return { lienzos: [una], dividido: false };
    const partes = partirEnDos(palabras);
    if (partes.length < 2) return null;
    const dos = partes.map((p, i) => dibujarUna(estilo, p, `${verso.referencia} (${i + 1}/2)`));
    return dos.every(Boolean) ? { lienzos: dos, dividido: true } : null;
  }

  // ---------- envio ----------

  // Convierte los lienzos a JPEG (base64); se adelanta mientras la hoja esta abierta, despues de pintar la pantalla.
  // Con toDataURL (unas decimas como mucho): en la WebView de Android, toBlob llega a tardar mas de 10 segundos.
  function codificar(resultado) {
    if (!resultado.datos) {
      resultado.datos = new Promise((resolver, fallar) => setTimeout(() => {
        try { resolver(resultado.lienzos.map(lienzo => lienzo.toDataURL(TIPO, CALIDAD).split(',')[1])); } catch (e) { fallar(e); }
      }, 0));
      resultado.datos.catch(() => { resultado.datos = null; });
    }
    return resultado.datos;
  }

  const conEnlace = (mensaje) => (ENLACE_INSTALACION ? `${mensaje}\n${ENLACE_INSTALACION}` : mensaje);

  function compartirTexto(verso) {
    const mensaje = conEnlace(`"${unir(palabrasDe(verso.html))}"\n${verso.referencia} (${NOMBRE_APP})`);
    const plugin = plugins().Share;
    if (plugin) {
      plugin.share({ text: mensaje, title: verso.referencia, dialogTitle: verso.referencia }).catch(() => {});
      return;
    }
    if (navigator.share) {
      navigator.share({ text: mensaje, title: verso.referencia }).catch(() => {});
      return;
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(mensaje)
        .then(() => mostrarToast('Versículo copiado'))
        .catch(() => mostrarToast('No se pudo copiar'));
    } else {
      mostrarToast('No se pudo copiar');
    }
  }

  function borrarTemporales() {
    const archivos = plugins().Filesystem;
    if (!esNativo() || !archivos) return Promise.resolve();
    return archivos.rmdir({ path: CARPETA, directory: 'CACHE', recursive: true }).catch(() => {});
  }

  async function compartirImagenes(resultado, verso) {
    const lienzos = resultado.lienzos;
    const base = verso.referencia.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^A-Za-z0-9]+/g, '-');
    const nombres = lienzos.map((_, i) => `${base}${lienzos.length > 1 ? `-${i + 1}` : ''}.jpg`);
    const mensaje = conEnlace(NOMBRE_APP);

    if (esNativo()) {
      const { Filesystem, Share } = plugins();
      if (!Filesystem || !Share) throw new Error('faltan plugins');
      // La app que recibe la imagen puede leerla despues de cerrarse el menu: los temporales de un envio terminado
      // se borran antes del siguiente (y al volver a abrir Leer); los de un menu cancelado, en el momento.
      const datos = await codificar(resultado);
      await borrarTemporales();
      const rutas = [];
      try {
        for (let i = 0; i < lienzos.length; i++) {
          const { uri } = await Filesystem.writeFile({ path: `${CARPETA}/${nombres[i]}`, data: datos[i], directory: 'CACHE', recursive: true });
          rutas.push(uri);
        }
      } catch (e) {
        await borrarTemporales();
        throw e;
      }
      try {
        await Share.share({ files: rutas, text: mensaje, title: verso.referencia, dialogTitle: verso.referencia });
      } catch (e) {
        await borrarTemporales();
        if (!/cancel/i.test((e && e.message) || '')) throw e;
      }
      return;
    }

    // Navegador (pruebas): comparte el archivo si puede; si no, lo descarga.
    const ficheros = await Promise.all(lienzos.map((l, i) => new Promise(res => l.toBlob(b => res(new File([b], nombres[i], { type: TIPO })), TIPO, CALIDAD))));
    if (navigator.canShare && navigator.canShare({ files: ficheros })) {
      await navigator.share({ files: ficheros, text: mensaje }).catch(() => {});
      return;
    }
    ficheros.forEach(f => {
      const enlace = document.createElement('a');
      enlace.href = URL.createObjectURL(f);
      enlace.download = f.name;
      enlace.click();
      setTimeout(() => URL.revokeObjectURL(enlace.href), 4000);
    });
  }

  // ---------- hoja inferior ----------

  const estiloGuardado = () => { try { return localStorage.getItem(CLAVE_ESTILO); } catch (e) { return null; } };
  const guardarEstilo = (id) => { try { localStorage.setItem(CLAVE_ESTILO, id); } catch (e) {} };

  function boton(clase, texto, alTocar) {
    const b = document.createElement('button');
    b.type = 'button';
    b.className = clase;
    if (texto) b.textContent = texto;
    b.addEventListener('click', alTocar);
    return b;
  }

  // verso = { html, referencia }
  function abrir(verso) {
    const previo = document.querySelector('.overlay-pantalla');
    if (previo) previo.remove();

    // Es un .overlay-pantalla: el boton Atras de Android la cierra igual que las demas ventanas.
    const fondo = document.createElement('div');
    fondo.className = 'overlay-pantalla visible fondo-compartir';
    const hoja = document.createElement('div');
    hoja.className = 'hoja-compartir';
    hoja.setAttribute('role', 'dialog');
    const titulo = document.createElement('div');
    titulo.className = 'titulo-compartir';
    titulo.textContent = `Compartir ${verso.referencia}`;
    const fila = document.createElement('div');
    fila.className = 'fila-estilos';
    const cerrar = () => fondo.remove();
    const cancelar = boton('btn-cerrar-overlay', 'Cancelar', cerrar);
    hoja.append(titulo, fila, cancelar);
    fondo.appendChild(hoja);
    fondo.addEventListener('click', (e) => { e.stopPropagation(); if (e.target === fondo) cerrar(); });

    const ultimo = estiloGuardado() || ESTILOS_COMPARTIR[0].id;

    async function enviar(resultado) {
      if (enCurso) return;
      enCurso = true;
      cerrar();
      mostrarToast('Preparando…'); // respuesta inmediata: el menu de Android tarda un momento en salir
      try {
        await compartirImagenes(resultado, verso);
      } catch (e) {
        mostrarToast('No se pudo compartir la imagen');
      } finally {
        enCurso = false;
      }
    }

    // Versiculo demasiado largo para una sola imagen: se pregunta que hacer.
    function preguntarLargo(resultado) {
      const aviso = document.createElement('div');
      aviso.className = 'aviso-compartir';
      aviso.textContent = resultado
        ? 'Este versículo es muy largo para leerse bien en una sola imagen.'
        : 'Este versículo es demasiado largo para compartirlo como imagen.';
      const botones = document.createElement('div');
      botones.className = 'botones-overlay';
      botones.appendChild(boton('btn-overlay cancelar', 'Solo texto', () => { cerrar(); compartirTexto(verso); }));
      if (resultado) botones.appendChild(boton('btn-overlay guardar', 'Dos imágenes', () => enviar(resultado)));
      fila.replaceWith(aviso);
      aviso.after(botones);
    }

    let pedido = false;
    const marcar = (elegido) => fila.querySelectorAll('.opcion-compartir').forEach(o => o.classList.toggle('elegida', o === elegido));

    const pendientes = ESTILOS_COMPARTIR.map(estilo => {
      let resultado; // undefined = generandose; false = fallo
      let entregar;
      const listo = new Promise(r => { entregar = r; });
      const b = boton('opcion-compartir', '', async () => {
        if (pedido) return; // ya se toco una miniatura que aun se esta preparando
        if (resultado === undefined) {
          pedido = true;
          marcar(b);
          b.querySelector('span').textContent = 'Preparando…';
          await listo;
          pedido = false;
          if (!fondo.isConnected) return; // cancelado mientras se preparaba
        }
        if (resultado === false) {
          b.querySelector('span').textContent = estilo.nombre;
          mostrarToast('No se pudo crear la imagen');
          return;
        }
        guardarEstilo(estilo.id);
        if (!resultado || resultado.dividido) preguntarLargo(resultado);
        else enviar(resultado);
      });
      b.dataset.estilo = estilo.id;
      b.classList.toggle('elegida', estilo.id === ultimo);
      const mini = document.createElement('canvas');
      mini.className = 'miniatura-compartir';
      mini.width = mini.height = 360;
      const nombre = document.createElement('span');
      nombre.textContent = estilo.nombre;
      b.append(mini, nombre);
      fila.appendChild(b);
      return async () => {
        try {
          resultado = await generar(estilo, verso);
        } catch (e) {
          resultado = false;
        }
        if (resultado) {
          const c = mini.getContext('2d');
          c.imageSmoothingQuality = 'high';
          c.drawImage(resultado.lienzos[0], 0, 0, mini.width, mini.height);
          if (resultado.dividido) nombre.textContent = `${estilo.nombre} · 2 imágenes`;
        }
        b.classList.add('lista');
        entregar();
        return resultado;
      };
    });

    const soloTexto = boton('opcion-compartir opcion-texto', '', () => {
      guardarEstilo('texto');
      cerrar();
      compartirTexto(verso);
    });
    soloTexto.classList.toggle('elegida', ultimo === 'texto');
    soloTexto.innerHTML = '<span class="miniatura-compartir" aria-hidden="true">Aa</span><span>Solo texto</span>';
    fila.appendChild(soloTexto);

    document.body.appendChild(fondo);
    const elegida = fila.querySelector('.elegida');
    if (elegida) fila.scrollLeft = elegida.offsetLeft - fila.offsetLeft - (fila.clientWidth - elegida.offsetWidth) / 2;

    // Primero se ve la hoja; las miniaturas se dibujan despues, una por cuadro y sin esperarse entre si.
    // Con todas a la vista, se adelantan los JPEG (uno cada vez) para que el menu de Android salga antes.
    const cuadro = (espera) => new Promise(r => requestAnimationFrame(() => setTimeout(r, espera)));
    (async () => {
      const hechas = [];
      for (const dibujar of pendientes) {
        await cuadro(0);
        if (!fondo.isConnected) return;
        hechas.push(dibujar());
      }
      for (const resultado of await Promise.all(hechas)) {
        await cuadro(80);
        if (!fondo.isConnected) return;
        if (resultado) codificar(resultado).catch(() => {});
      }
    })();
  }

  borrarTemporales();
  cargarFuentes().catch(() => {});
  // Los fondos se calculan al abrir la pagina, para que esten listos al tocar compartir.
  setTimeout(() => ESTILOS_COMPARTIR.forEach(e => { if (e.preparar) e.preparar().catch(() => {}); }), 300);

  return { abrir, generar, palabrasDe };
})();
