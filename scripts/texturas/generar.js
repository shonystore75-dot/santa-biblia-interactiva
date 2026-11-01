// Regenera las imagenes del carrusel "Explorar" (papiros y vara) en /texturas.
//
// Uso:  node scripts/texturas/generar.js
//
// Abre generar.html (que contiene las mismas funciones de ruido/canvas que usaba
// index.html) en Chrome o Edge sin interfaz, recoge los PNG que dibuja y los
// guarda como WebP con transparencia (usa 'sharp', ya presente en node_modules).
// Esta carpeta (scripts/) no se copia a www/, asi que no forma parte de la app.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');
const sharp = require('sharp');

const RAIZ = path.resolve(__dirname, '..', '..');
const DESTINO = path.join(RAIZ, 'texturas');
const PAGINA = path.join(__dirname, 'generar.html');

const candidatos = [
  process.env.NAVEGADOR,
  path.join(process.env['ProgramFiles'] || '', 'Google', 'Chrome', 'Application', 'chrome.exe'),
  path.join(process.env['ProgramFiles(x86)'] || '', 'Google', 'Chrome', 'Application', 'chrome.exe'),
  path.join(process.env['ProgramFiles(x86)'] || '', 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
  path.join(process.env['ProgramFiles'] || '', 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
].filter(Boolean);
const navegador = candidatos.find(p => fs.existsSync(p));
if (!navegador) { console.error('No encontre Chrome ni Edge. Define la variable NAVEGADOR con la ruta.'); process.exit(1); }

const perfil = fs.mkdtempSync(path.join(os.tmpdir(), 'texturas-'));
let dom;
try {
  dom = execFileSync(navegador, [
    '--headless', '--disable-gpu', '--no-first-run', '--user-data-dir=' + perfil,
    '--virtual-time-budget=60000', '--dump-dom', require('url').pathToFileURL(PAGINA).href,
  ], { encoding: 'utf8', maxBuffer: 256 * 1024 * 1024, timeout: 180000 });
} finally {
  fs.rmSync(perfil, { recursive: true, force: true });
}

const m = dom.match(/<pre id="salida">([\s\S]*?)<\/pre>/);
if (!m || !m[1].trim()) { console.error('La pagina no devolvio texturas.'); process.exit(1); }
const texto = m[1].replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const texturas = JSON.parse(texto);

(async () => {
  fs.mkdirSync(DESTINO, { recursive: true });
  for (const [nombre, url] of Object.entries(texturas)) {
    const png = Buffer.from(url.split(',')[1], 'base64');
    const salida = path.join(DESTINO, nombre + '.webp');
    await sharp(png).webp({ quality: 92, alphaQuality: 100, effort: 6 }).toFile(salida);
    console.log(nombre + '.webp', Math.round(fs.statSync(salida).size / 1024) + ' KB', '(PNG ' + Math.round(png.length / 1024) + ' KB)');
  }
})();
