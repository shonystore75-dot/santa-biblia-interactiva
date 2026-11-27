// Estilos de la imagen para compartir un versiculo.
//
// AGREGAR UN ESTILO = anadir un objeto a la lista ESTILOS_COMPARTIR (al final del archivo):
//   { id: 'pergamino',            // unico y fijo: se guarda en localStorage ('compartirEstilo')
//     nombre: 'Pergamino',        // se muestra bajo la miniatura
//     fuentes: ['400 48px "Mi Letra"'],        // opcional: fuentes a cargar antes de dibujar (declaradas en FUENTES_COMPARTIR)
//     preparar() { return promesa; },          // opcional: trabajo pesado (el fondo); se adelanta al abrir Leer
//     dibujar(ctx, verso) { ... return true; } // pinta 1080x1080; devuelve false si el texto no cabe con letra legible
//   }
// `verso` trae { palabras, cita, pie }. Los colores, el marco y la posicion de cada cosa son de cada estilo
// (no dependen de la paleta activa). Para el texto estan las herramientas de LienzoTexto (ajustar y dibujar).

const LADO_COMPARTIR = 1080;
const FUENTE_LECTURA = '"Source Serif Compartir"';

// Fuentes incluidas en la app (funcionan sin internet).
const FUENTES_COMPARTIR = [
  { familia: 'Source Serif Compartir', archivo: 'fuentes/source-serif-4-latin.woff2', descriptores: { weight: '400 600' } },
];

const LienzoTexto = {
  // Reparte las palabras en lineas de ancho maximo `ancho` con la fuente ya puesta en ctx.
  repartir(ctx, palabras, ancho) {
    const espacio = ctx.measureText(' ').width;
    const lineas = [];
    let linea = null;
    for (const palabra of palabras) {
      const anchoPalabra = palabra.reduce((s, t) => s + ctx.measureText(t.texto).width, 0);
      if (anchoPalabra > ancho) return null;
      if (linea && linea.ancho + espacio + anchoPalabra <= ancho) {
        linea.palabras.push(palabra);
        linea.ancho += espacio + anchoPalabra;
      } else {
        linea = { palabras: [palabra], ancho: anchoPalabra };
        lineas.push(linea);
      }
    }
    return lineas;
  },

  // Busca la letra mas grande (entre max y min) con la que el texto cabe en la caja. null = no cabe.
  ajustar(ctx, palabras, { ancho, alto, max, min, interlinea, fuente }) {
    for (let tamano = max; tamano >= min; tamano -= 1) {
      ctx.font = fuente(tamano);
      let lineas = this.repartir(ctx, palabras, ancho);
      if (!lineas || lineas.length * tamano * interlinea > alto) continue;
      // Equilibra las lineas: el menor ancho que conserva el mismo numero de renglones (evita una palabra suelta al final).
      let bajo = ancho * 0.55, alta = ancho;
      while (alta - bajo > 4) {
        const medio = (bajo + alta) / 2;
        const prueba = this.repartir(ctx, palabras, medio);
        if (prueba && prueba.length === lineas.length) alta = medio; else bajo = medio;
      }
      lineas = this.repartir(ctx, palabras, alta);
      return { tamano, lineas, altoLinea: tamano * interlinea, alto: lineas.length * tamano * interlinea, fuente: fuente(tamano) };
    }
    return null;
  },

  // Dibuja el bloque centrado en x, empezando en y. colorDe(tramo) elige el color (p. ej. palabras de Jesus).
  dibujar(ctx, bloque, x, y, colorDe) {
    ctx.save();
    ctx.font = bloque.fuente;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    const espacio = ctx.measureText(' ').width;
    bloque.lineas.forEach((linea, i) => {
      let cursor = x - linea.ancho / 2;
      const medio = y + bloque.altoLinea * (i + 0.5);
      for (const palabra of linea.palabras) {
        for (const tramo of palabra) {
          ctx.fillStyle = colorDe(tramo);
          ctx.fillText(tramo.texto, cursor, medio);
          cursor += ctx.measureText(tramo.texto).width;
        }
        cursor += espacio;
      }
    });
    ctx.restore();
  },

  // Numeros al azar repetibles: la textura sale igual en la miniatura y en la imagen enviada.
  azar(semilla) {
    let a = semilla >>> 0;
    return () => {
      a = (a + 0x6D2B79F5) >>> 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  },
};

// ---------- Estilo clasico: papel marfil, marco dorado doble con esquinas ----------

let papelClasico = null; // la textura se calcula una sola vez

function crearPapelClasico() {
  const L = LADO_COMPARTIR;
  const lienzo = document.createElement('canvas');
  lienzo.width = lienzo.height = L;
  const c = lienzo.getContext('2d');
  const azar = LienzoTexto.azar(1909);

  c.fillStyle = '#F7EFDD';
  c.fillRect(0, 0, L, L);

  // manchas amplias y tenues del papel
  for (let i = 0; i < 70; i++) {
    const x = azar() * L, y = azar() * L, r = 80 + azar() * 220;
    const clara = azar() > 0.5;
    const g = c.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, clara ? 'rgba(255,252,240,0.22)' : 'rgba(196,160,104,0.07)');
    g.addColorStop(1, clara ? 'rgba(255,252,240,0)' : 'rgba(196,160,104,0)');
    c.fillStyle = g;
    c.fillRect(x - r, y - r, r * 2, r * 2);
  }
  // grano
  const grano = document.createElement('canvas');
  grano.width = grano.height = L / 2;
  const cg = grano.getContext('2d');
  const datos = cg.createImageData(grano.width, grano.height);
  for (let i = 0; i < datos.data.length; i += 4) {
    const claro = azar() > 0.5;
    datos.data[i] = claro ? 255 : 120;
    datos.data[i + 1] = claro ? 250 : 92;
    datos.data[i + 2] = claro ? 235 : 52;
    datos.data[i + 3] = Math.floor(azar() * 20);
  }
  cg.putImageData(datos, 0, 0);
  c.drawImage(grano, 0, 0, L, L);
  // fibras
  c.lineWidth = 1;
  for (let i = 0; i < 520; i++) {
    const x = azar() * L, y = azar() * L, a = azar() * Math.PI, largo = 6 + azar() * 18;
    c.strokeStyle = `rgba(139,105,60,${0.05 + azar() * 0.07})`;
    c.beginPath();
    c.moveTo(x, y);
    c.quadraticCurveTo(x + Math.cos(a + 0.6) * largo * 0.5, y + Math.sin(a + 0.6) * largo * 0.5, x + Math.cos(a) * largo, y + Math.sin(a) * largo);
    c.stroke();
  }
  // bordes apenas envejecidos
  const v = c.createRadialGradient(L / 2, L / 2, L * 0.36, L / 2, L / 2, L * 0.74);
  v.addColorStop(0, 'rgba(160,118,62,0)');
  v.addColorStop(1, 'rgba(160,118,62,0.22)');
  c.fillStyle = v;
  c.fillRect(0, 0, L, L);
  return lienzo;
}

function oroClasico(ctx) {
  const g = ctx.createLinearGradient(0, 0, LADO_COMPARTIR, LADO_COMPARTIR);
  ['#8A6420', '#C9A24A', '#9A7226', '#D4B15C', '#8F6A22', '#BE963F', '#86611F'].forEach((color, i, a) => g.addColorStop(i / (a.length - 1), color));
  return g;
}

function rombo(ctx, x, y, r) {
  ctx.beginPath();
  ctx.moveTo(x, y - r);
  ctx.lineTo(x + r, y);
  ctx.lineTo(x, y + r);
  ctx.lineTo(x - r, y);
  ctx.closePath();
  ctx.fill();
}

// Adorno de la esquina superior izquierda; las otras tres son su reflejo.
function esquinaClasica(ctx) {
  const punto = (x, y, r) => { ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); };
  ctx.lineCap = 'round';
  // cuadro con rombo donde se cruzan las dos lineas
  ctx.lineWidth = 3;
  ctx.strokeRect(46, 46, 38, 38);
  rombo(ctx, 65, 65, 12);
  // volutas a lo largo de cada lado
  for (const girar of [false, true]) {
    ctx.save();
    if (girar) ctx.transform(0, 1, 1, 0, 0, 0); // refleja sobre la diagonal
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(84, 78);
    ctx.bezierCurveTo(124, 82, 148, 74, 178, 68);
    ctx.bezierCurveTo(194, 65, 200, 80, 189, 86);
    ctx.bezierCurveTo(181, 90, 174, 83, 179, 78);
    ctx.stroke();
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(108, 79);
    ctx.bezierCurveTo(118, 98, 134, 104, 146, 96);
    ctx.bezierCurveTo(152, 90, 144, 84, 139, 89);
    ctx.stroke();
    punto(204, 69, 3.5);
    punto(218, 69, 2.2);
    ctx.restore();
  }
  // hoja diagonal hacia el centro
  ctx.beginPath();
  ctx.moveTo(86, 86);
  ctx.quadraticCurveTo(116, 94, 124, 124);
  ctx.quadraticCurveTo(94, 116, 86, 86);
  ctx.fill();
  punto(134, 134, 3.5);
}

const estiloClasico = {
  id: 'clasico',
  nombre: 'Clásico',
  fuentes: [`400 48px ${FUENTE_LECTURA}`, `600 40px ${FUENTE_LECTURA}`],
  dibujar(ctx, verso) {
    const L = LADO_COMPARTIR, centro = L / 2;
    const caja = { arriba: 150, abajo: 915, ancho: 810 };
    const altoCita = 134; // adorno + cita

    const bloque = LienzoTexto.ajustar(ctx, verso.palabras, {
      ancho: caja.ancho, alto: caja.abajo - caja.arriba - altoCita,
      max: 76, min: 40, interlinea: 1.38,
      fuente: (t) => `400 ${t}px ${FUENTE_LECTURA}`,
    });
    if (!bloque) return false;

    if (!papelClasico) papelClasico = crearPapelClasico();
    ctx.drawImage(papelClasico, 0, 0);

    // marco doble
    const oro = oroClasico(ctx);
    ctx.save();
    ctx.strokeStyle = ctx.fillStyle = oro;
    ctx.lineWidth = 7;
    ctx.strokeRect(40, 40, L - 80, L - 80);
    ctx.lineWidth = 2.5;
    ctx.strokeRect(60, 60, L - 120, L - 120);
    for (const [sx, sy] of [[1, 1], [-1, 1], [1, -1], [-1, -1]]) {
      ctx.save();
      ctx.translate(sx > 0 ? 0 : L, sy > 0 ? 0 : L);
      ctx.scale(sx, sy);
      esquinaClasica(ctx);
      ctx.restore();
    }
    ctx.restore();

    // texto y cita, centrados como un solo grupo
    const y = caja.arriba + (caja.abajo - caja.arriba - bloque.alto - altoCita) / 2;
    LienzoTexto.dibujar(ctx, bloque, centro, y, (t) => (t.jesus ? '#8C2318' : '#33241A'));

    const yAdorno = y + bloque.alto + 42;
    ctx.save();
    ctx.strokeStyle = ctx.fillStyle = oro;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(centro - 110, yAdorno); ctx.lineTo(centro - 22, yAdorno);
    ctx.moveTo(centro + 22, yAdorno); ctx.lineTo(centro + 110, yAdorno);
    ctx.stroke();
    rombo(ctx, centro, yAdorno, 9);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#A4492A';
    ctx.font = `600 44px ${FUENTE_LECTURA}`;
    ctx.fillText(verso.cita, centro, yAdorno + 58);

    ctx.fillStyle = '#6F5836';
    ctx.font = `600 27px ${FUENTE_LECTURA}`;
    if ('letterSpacing' in ctx) ctx.letterSpacing = '2px';
    ctx.fillText(verso.pie, centro, 962);
    ctx.restore();
    return true;
  },
};

// ---------- Estilo pergamino: hoja de bordes rasgados, como los rollos del carrusel de Inicio ----------

let fondoPergamino = null; // la hoja se calcula una sola vez
let tareaPergamino = null;

// Dibuja la hoja completa. Usa las formulas y los colores de scripts/texturas/generar.html (papiros del
// carrusel), con el rasgado y el tostado en los CUATRO lados y el centro aclarado para la letra.
// Es autonoma a proposito: se copia tal cual a un hilo aparte (Worker). crear(w, h) devuelve un lienzo.
function pintarPergamino(crear) {
  const L = 1080;
  const mulberry = (a) => () => {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
  const crearRuido = (semilla) => {
    const r = mulberry(semilla), T = new Float32Array(65536);
    for (let i = 0; i < 65536; i++) T[i] = r();
    const n = (x, y) => {
      const ix = Math.floor(x), iy = Math.floor(y);
      let fx = x - ix, fy = y - iy;
      fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy);
      const f0 = (iy & 255) << 8, f1 = ((iy + 1) & 255) << 8, c0 = ix & 255, c1 = (ix + 1) & 255;
      const sup = T[f0 | c0] + (T[f0 | c1] - T[f0 | c0]) * fx;
      return sup + (T[f1 | c0] + (T[f1 | c1] - T[f1 | c0]) * fx - sup) * fy;
    };
    // tres escalas sumadas
    const fbm = (x, y) => (n(x, y) * 0.5 + n(x * 2.03, y * 2.03) * 0.25 + n(x * 4.12, y * 4.12) * 0.125) / 0.875;
    return { n, fbm };
  };
  const N = crearRuido(205), R = mulberry(36);

  // Perfil del rasgado: los puntos del carrusel (posicion a lo largo del lado en %, profundidad).
  const SUP = [[0, 2.5], [5.8, 1.8], [10.9, 4.1], [18, 0.4], [22.8, 3.6], [29.4, 1.4], [35.4, 0.8], [40.1, 0.7], [46.6, 1.4], [51.2, 3.5], [57.4, 0.9], [62.2, 2.5], [67.1, 2.8], [73.3, 1.7], [81.1, 2.4], [86.1, 0.5], [91.5, 0.4], [98.5, 1], [100, 2.9]];
  const INF = [[0, 3.2], [6.2, 0.8], [12, 2.2], [18.8, 0.4], [25.1, 2.9], [30.8, 3.3], [38.5, 2.5], [45.8, 3.7], [51.3, 1.5], [58.1, 3], [64.7, 2.6], [72.7, 2.5], [80.1, 2], [85.8, 3.6], [94.2, 4], [99.2, 2.1], [100, 3.2]];
  // profundidad del borde en cada pixel de un lado: margen + perfil quebrado + ondas pequenas + mellas
  const lado = (puntos, desfase, espejo, semilla) => {
    const salida = new Float32Array(L);
    for (let p = 0; p < L; p++) {
      let u = (p / L + desfase) % 1;
      if (espejo) u = 1 - u;
      u *= 100;
      let base = puntos[puntos.length - 1][1];
      for (let j = 1; j < puntos.length; j++) {
        if (u <= puntos[j][0]) {
          const a = puntos[j - 1], b = puntos[j];
          base = a[1] + (b[1] - a[1]) * ((u - a[0]) / (b[0] - a[0] || 1));
          break;
        }
      }
      const q = N.n(p * 0.022 + semilla * 13, 20 + semilla);
      salida[p] = 13 + base * 8.4 + 6 * N.fbm(p * 0.042 + semilla * 9, 7.7) + (q > 0.82 ? 11 * (q - 0.82) / 0.18 : 0);
    }
    return salida;
  };
  const arriba = lado(SUP, 0.13, false, 1), abajo = lado(INF, 0.31, true, 2);
  const izquierda = lado(INF, 0.57, false, 3), derecha = lado(SUP, 0.74, true, 4);
  // distancia hacia dentro desde el borde rasgado mas cercano (negativa = fuera de la hoja)
  const distHoja = (x, y) => Math.min(y - arriba[x], L - 1 - abajo[x] - y, x - izquierda[y], L - 1 - derecha[y] - x);
  const suave = (v) => { v = v < 0 ? 0 : v > 1 ? 1 : v; return v * v * (3 - 2 * v); };

  // grandes manchas de tono: se calculan cada 6 px y se interpolan
  const P = 6, M = Math.ceil(L / P) + 2, grandes = new Float32Array(M * M);
  for (let j = 0; j < M; j++) for (let i = 0; i < M; i++) grandes[j * M + i] = N.fbm(i * P * 0.0052 + 7, j * P * 0.0065 + 3);
  const tira = 128;
  const tonos = Array.from({ length: Math.ceil(L / tira) }, () => (R() - 0.5) * 0.12);

  const hoja = crear(L, L);
  const g = hoja.getContext('2d', { willReadFrequently: true });
  const imagen = g.createImageData(L, L), d = imagen.data;
  for (let y = 0; y < L; y++) {
    const gy = y / P, j = gy | 0, fy = gy - j;
    for (let x = 0; x < L; x++) {
      let dist = distHoja(x, y);
      if (dist < 90) dist += (N.n(x * 0.22, y * 0.22) - 0.5) * 6 + (N.n(x * 0.72, y * 0.72) - 0.5) * 2.4; // deshilachado
      let rr = 246, gg = 238, bb = 220; // marfil de fuera
      const al = dist <= -2 ? 0 : dist >= 4 ? 1 : (dist + 2) / 6;
      if (al < 1) {
        // sombra suave que separa la hoja del fondo
        const a = 0.34 * suave((distHoja(x, y > 9 ? y - 9 : 0) + 20) / 24);
        rr += (70 - rr) * a; gg += (44 - gg) * a; bb += (24 - bb) * a;
      }
      if (al > 0) {
        const gx = x / P, k = gx | 0, fx = gx - k, b = j * M + k;
        const g0 = grandes[b] + (grandes[b + 1] - grandes[b]) * fx;
        const grande = g0 + (grandes[b + M] + (grandes[b + M + 1] - grandes[b + M]) * fx - g0) * fy;
        const fib = N.fbm(x * 0.0066, y * 0.36), fino = N.n(x * 0.6, y * 0.146), vert = N.fbm(x * 0.36 + 40, y * 0.0092);
        const franja = (x / tira) | 0, sx = x - franja * tira;
        let t = 0.34 + grande * 0.6 + (fib - 0.5) * 0.46 + (vert - 0.5) * 0.2 + tonos[franja] + (fino - 0.5) * 0.12;
        if (sx < 3) t -= 0.12 * (1 - sx / 3); else if (sx < 7) t += 0.035; // costuras
        t = t < 0 ? 0 : t > 1 ? 1 : t;
        t *= 1 - 0.62 * suave((dist - 14) / 62); // hacia dentro el papel se aclara, para la letra
        let pr = 246 - 44 * t, pg = 226 - 64 * t, pb = 176 - 82 * t;
        let e = 1 - dist / 56; e = e < 0 ? 0 : e > 1 ? 1 : e; e *= e; // tostado
        pr = pr * (1 - 0.3 * e) - 18 * e; pg = pg * (1 - 0.46 * e) - 14 * e; pb = pb * (1 - 0.66 * e) - 8 * e;
        if (dist < 9) { const q = (9 - (dist < 0 ? 0 : dist)) / 12; pr *= 1 - 0.34 * q; pg *= 1 - 0.46 * q; pb *= 1 - 0.55 * q; } // orilla
        rr += (pr - rr) * al; gg += (pg - gg) * al; bb += (pb - bb) * al;
      }
      const i = (y * L + x) * 4;
      d[i] = rr; d[i + 1] = gg; d[i + 2] = bb; d[i + 3] = 255;
    }
  }
  g.putImageData(imagen, 0, 0);

  // manchas de edad y motas, lejos del borde para que no manchen el marfil de fuera
  for (let m = 0; m < 8; m++) {
    const radio = 50 + R() * 70;
    const px = 60 + radio + R() * (L - 120 - radio * 2), py = 60 + radio + R() * (L - 120 - radio * 2);
    const mancha = g.createRadialGradient(px, py, 0, px, py, radio);
    mancha.addColorStop(0, `rgba(120,78,32,${0.07 + R() * 0.09})`);
    mancha.addColorStop(1, 'rgba(120,78,32,0)');
    g.fillStyle = mancha;
    g.fillRect(px - radio, py - radio, radio * 2, radio * 2);
  }
  for (let m = 0; m < 190; m++) {
    g.fillStyle = `rgba(70,40,15,${0.2 + R() * 0.35})`;
    const t = 1.2 + R() * 2;
    g.fillRect(62 + R() * (L - 124), 62 + R() * (L - 124), t, t);
  }

  // Donde va la letra ningun punto baja de la luminancia 0,5 (asegura el contraste). El limite se desvanece
  // alrededor de esa zona para que no se note ningun recuadro.
  const todo = g.getImageData(0, 0, L, L), z = todo.data;
  const lineal = Float32Array.from({ length: 256 }, (_, v) => (v <= 10 ? v / 3294.6 : Math.pow((v / 255 + 0.055) / 1.055, 2.4)));
  for (let y = 80; y < 1010; y++) {
    const fy = Math.max(112 - y, y - 970, 0);
    for (let x = 80; x < 1000; x++) {
      const fuera = Math.max(116 - x, x - 964, fy, 0);
      const minima = 0.5 - fuera * 0.004;
      const i = (y * L + x) * 4;
      while (0.2126 * lineal[z[i]] + 0.7152 * lineal[z[i + 1]] + 0.0722 * lineal[z[i + 2]] < minima) {
        z[i] += Math.ceil((250 - z[i]) / 40);
        z[i + 1] += Math.ceil((238 - z[i + 1]) / 40);
        z[i + 2] += Math.ceil((208 - z[i + 2]) / 40);
      }
    }
  }
  g.putImageData(todo, 0, 0);
  return hoja;
}

const lienzoPergamino = (w, h) => Object.assign(document.createElement('canvas'), { width: w, height: h });

// Calcula la hoja en un hilo aparte para no frenar la pantalla; si el telefono no puede, en el principal.
function prepararPergamino() {
  if (!tareaPergamino) {
    tareaPergamino = new Promise((resolver, fallar) => {
      const sinHilo = () => setTimeout(() => {
        try { resolver(pintarPergamino(lienzoPergamino)); } catch (e) { fallar(e); }
      }, 0);
      try {
        const codigo = `${pintarPergamino.toString()}
onmessage = () => { const b = pintarPergamino((w, h) => new OffscreenCanvas(w, h)).transferToImageBitmap(); postMessage(b, [b]); };`;
        const url = URL.createObjectURL(new Blob([codigo], { type: 'text/javascript' }));
        const hilo = new Worker(url);
        const terminar = () => { hilo.terminate(); URL.revokeObjectURL(url); };
        hilo.onmessage = (e) => { terminar(); resolver(e.data); };
        hilo.onerror = (e) => { e.preventDefault(); terminar(); sinHilo(); };
        hilo.postMessage(0);
      } catch (e) {
        sinHilo();
      }
    }).then((hoja) => { fondoPergamino = hoja; })
      .catch((e) => { tareaPergamino = null; throw e; });
  }
  return tareaPergamino;
}

const estiloPergamino = {
  id: 'pergamino',
  nombre: 'Pergamino',
  fuentes: [`400 48px ${FUENTE_LECTURA}`, `600 40px ${FUENTE_LECTURA}`],
  preparar: prepararPergamino,
  dibujar(ctx, verso) {
    const L = LADO_COMPARTIR, centro = L / 2;
    const caja = { arriba: 118, abajo: 908, ancho: 836 };
    const altoCita = 134; // filete + cita

    const bloque = LienzoTexto.ajustar(ctx, verso.palabras, {
      ancho: caja.ancho, alto: caja.abajo - caja.arriba - altoCita,
      max: 76, min: 40, interlinea: 1.38,
      fuente: (t) => `400 ${t}px ${FUENTE_LECTURA}`,
    });
    if (!bloque) return false;

    if (!fondoPergamino) fondoPergamino = pintarPergamino(lienzoPergamino);
    ctx.drawImage(fondoPergamino, 0, 0);

    // texto y cita, centrados como un solo grupo
    const y = caja.arriba + (caja.abajo - caja.arriba - bloque.alto - altoCita) / 2;
    LienzoTexto.dibujar(ctx, bloque, centro, y, (t) => (t.jesus ? '#7E1C12' : '#3B2414'));

    ctx.save();
    // filete fino que se desvanece en las puntas
    const yFilete = y + bloque.alto + 44;
    const filete = ctx.createLinearGradient(centro - 170, 0, centro + 170, 0);
    filete.addColorStop(0, 'rgba(122,78,36,0)');
    filete.addColorStop(0.5, 'rgba(122,78,36,0.85)');
    filete.addColorStop(1, 'rgba(122,78,36,0)');
    ctx.fillStyle = filete;
    ctx.fillRect(centro - 170, yFilete, 340, 2);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = '#7C321A';
    ctx.font = `600 44px ${FUENTE_LECTURA}`;
    ctx.fillText(verso.cita, centro, yFilete + 58);

    ctx.fillStyle = '#5E4526';
    ctx.font = `400 26px ${FUENTE_LECTURA}`;
    if ('letterSpacing' in ctx) ctx.letterSpacing = '1.5px';
    ctx.fillText(verso.pie, centro, 950);
    ctx.restore();
    return true;
  },
};

const ESTILOS_COMPARTIR = [
  estiloClasico,
  estiloPergamino,
];
