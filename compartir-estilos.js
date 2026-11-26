// Estilos de la imagen para compartir un versiculo.
//
// AGREGAR UN ESTILO = anadir un objeto a la lista ESTILOS_COMPARTIR (al final del archivo):
//   { id: 'pergamino',            // unico y fijo: se guarda en localStorage ('compartirEstilo')
//     nombre: 'Pergamino',        // se muestra bajo la miniatura
//     fuentes: ['400 48px "Mi Letra"'],        // opcional: fuentes a cargar antes de dibujar (declaradas en FUENTES_COMPARTIR)
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

// ---------- Estilo pergamino: sin marco, el papel ocupa toda la imagen ----------

let fondoPergamino = null; // la textura se calcula una sola vez

// Ruido suave (manchas irregulares) entre 0 y 1.
function crearRuido(azar) {
  const N = 256;
  const tabla = Float32Array.from({ length: N * N }, azar);
  const valor = (x, y) => tabla[(y & (N - 1)) * N + (x & (N - 1))];
  const suave = (t) => t * t * (3 - 2 * t);
  const capa = (x, y) => {
    const xi = Math.floor(x), yi = Math.floor(y), u = suave(x - xi), v = suave(y - yi);
    const a = valor(xi, yi) + (valor(xi + 1, yi) - valor(xi, yi)) * u;
    const b = valor(xi, yi + 1) + (valor(xi + 1, yi + 1) - valor(xi, yi + 1)) * u;
    return a + (b - a) * v;
  };
  // varias escalas sumadas
  return (x, y) => capa(x, y) * 0.54 + capa(x * 2.1 + 31, y * 2.1 + 17) * 0.28 + capa(x * 4.3 + 7, y * 4.3 + 53) * 0.18;
}

// Los tonos se mantienen claros (tambien en bordes y manchas) para que la letra mas clara conserve
// un contraste de 4,5:1 o mas en cualquier punto.
function crearPergamino() {
  const L = LADO_COMPARTIR, M = L / 2;
  const azar = LienzoTexto.azar(2026);
  const ruido = crearRuido(azar);
  const mezcla = (a, b, t) => a + (b - a) * t;
  const entre = (v, min, max) => Math.max(0, Math.min(1, (v - min) / (max - min)));

  // base: crema y ocre claro en manchas amplias, con bordes irregulares algo mas oscuros
  const base = document.createElement('canvas');
  base.width = base.height = M;
  const cb = base.getContext('2d');
  const datos = cb.createImageData(M, M);
  const CREMA = [246, 233, 200], OCRE = [232, 207, 154], BORDE = [220, 191, 135];
  for (let y = 0; y < M; y++) {
    for (let x = 0; x < M; x++) {
      const tono = entre(ruido(x / 95, y / 95), 0.28, 0.74);
      const dx = Math.abs(x / (M - 1) - 0.5) * 2, dy = Math.abs(y / (M - 1) - 0.5) * 2;
      const lejos = Math.pow(dx ** 4 + dy ** 4, 0.25); // 0 en el centro, ~1 en los lados
      const orilla = entre(lejos + (ruido(x / 38 + 90, y / 38 + 40) - 0.5) * 0.34, 0.62, 1.08);
      const i = (y * M + x) * 4;
      for (let k = 0; k < 3; k++) {
        datos.data[i + k] = mezcla(mezcla(CREMA[k], OCRE[k], tono * 0.8), BORDE[k], orilla * orilla * (3 - 2 * orilla));
      }
      datos.data[i + 3] = 255;
    }
  }
  cb.putImageData(datos, 0, 0);

  const lienzo = document.createElement('canvas');
  lienzo.width = lienzo.height = L;
  const c = lienzo.getContext('2d');
  c.imageSmoothingQuality = 'high';
  c.drawImage(base, 0, 0, L, L);

  // manchas leves de humedad, de contorno irregular y con un cerco apenas marcado
  c.save();
  c.filter = 'blur(3px)';
  for (let i = 0; i < 13; i++) {
    const x = azar() * L, y = azar() * L, r = 22 + azar() * 70;
    const radios = Array.from({ length: 14 }, () => r * (0.6 + azar() * 0.75));
    const punto = (k) => {
      const a = (k / radios.length) * Math.PI * 2;
      return [x + Math.cos(a) * radios[k % radios.length], y + Math.sin(a) * radios[k % radios.length] * 0.75];
    };
    const medio = (p, q) => [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2];
    c.beginPath();
    c.moveTo(...medio(punto(0), punto(1)));
    for (let k = 1; k <= radios.length; k++) c.quadraticCurveTo(...punto(k), ...medio(punto(k), punto(k + 1)));
    c.closePath();
    c.fillStyle = 'rgba(172,122,58,0.055)';
    c.fill();
    c.strokeStyle = 'rgba(150,104,46,0.07)';
    c.lineWidth = 3;
    c.stroke();
  }
  c.restore();
  // motas
  for (let i = 0; i < 240; i++) {
    c.fillStyle = `rgba(128,88,42,${0.05 + azar() * 0.1})`;
    c.beginPath();
    c.arc(azar() * L, azar() * L, 0.6 + azar() * 1.6, 0, Math.PI * 2);
    c.fill();
  }
  // fibras claras y oscuras
  for (let i = 0; i < 1100; i++) {
    const x = azar() * L, y = azar() * L, a = azar() * Math.PI, largo = 8 + azar() * 26;
    const curva = (azar() - 0.5) * 1.6;
    c.strokeStyle = azar() > 0.45 ? `rgba(140,100,52,${0.07 + azar() * 0.09})` : `rgba(255,248,225,${0.2 + azar() * 0.25})`;
    c.lineWidth = 0.6 + azar() * 0.8;
    c.beginPath();
    c.moveTo(x, y);
    c.quadraticCurveTo(x + Math.cos(a + curva) * largo * 0.5, y + Math.sin(a + curva) * largo * 0.5, x + Math.cos(a) * largo, y + Math.sin(a) * largo);
    c.stroke();
  }
  // grano
  const grano = document.createElement('canvas');
  grano.width = grano.height = M;
  const cg = grano.getContext('2d');
  const puntos = cg.createImageData(M, M);
  for (let i = 0; i < puntos.data.length; i += 4) {
    const claro = azar() > 0.5;
    puntos.data[i] = claro ? 255 : 120;
    puntos.data[i + 1] = claro ? 246 : 86;
    puntos.data[i + 2] = claro ? 220 : 40;
    puntos.data[i + 3] = Math.floor(azar() * 22);
  }
  cg.putImageData(puntos, 0, 0);
  c.drawImage(grano, 0, 0, L, L);
  aclararHasta(c, 0.5);
  return lienzo;
}

// Ningun punto del papel queda por debajo de esa luminancia (0 a 1): es lo que asegura el contraste de la letra.
function aclararHasta(c, minima) {
  const imagen = c.getImageData(0, 0, LADO_COMPARTIR, LADO_COMPARTIR);
  const d = imagen.data;
  const lineal = Float32Array.from({ length: 256 }, (_, v) => (v <= 10 ? v / 3294.6 : Math.pow((v / 255 + 0.055) / 1.055, 2.4)));
  for (let i = 0; i < d.length; i += 4) {
    while (0.2126 * lineal[d[i]] + 0.7152 * lineal[d[i + 1]] + 0.0722 * lineal[d[i + 2]] < minima) {
      d[i] += Math.ceil((250 - d[i]) / 12);
      d[i + 1] += Math.ceil((238 - d[i + 1]) / 12);
      d[i + 2] += Math.ceil((208 - d[i + 2]) / 12);
    }
  }
  c.putImageData(imagen, 0, 0);
}

const estiloPergamino = {
  id: 'pergamino',
  nombre: 'Pergamino',
  fuentes: [`400 48px ${FUENTE_LECTURA}`, `600 40px ${FUENTE_LECTURA}`],
  dibujar(ctx, verso) {
    const L = LADO_COMPARTIR, centro = L / 2;
    const caja = { arriba: 110, abajo: 922, ancho: 840 };
    const altoCita = 134; // filete + cita

    const bloque = LienzoTexto.ajustar(ctx, verso.palabras, {
      ancho: caja.ancho, alto: caja.abajo - caja.arriba - altoCita,
      max: 76, min: 40, interlinea: 1.38,
      fuente: (t) => `400 ${t}px ${FUENTE_LECTURA}`,
    });
    if (!bloque) return false;

    if (!fondoPergamino) fondoPergamino = crearPergamino();
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
    ctx.fillText(verso.pie, centro, 984);
    ctx.restore();
    return true;
  },
};

const ESTILOS_COMPARTIR = [
  estiloClasico,
  estiloPergamino,
];
