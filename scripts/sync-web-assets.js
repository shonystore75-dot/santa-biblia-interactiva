// Capacitor's CLI copies webDir into the native project with plain fs
// recursion and has no .capacitorignore / ignore-file support, so webDir
// can't be the repo root (fs-extra refuses to copy a folder into its own
// subdirectory, and there's no way to exclude node_modules/android/etc).
// This script copies just the actual app files into www/, which is the
// webDir Capacitor uses, so the book JSON files stay single-sourced at
// the repo root and www/ is a disposable, gitignored build output.
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DEST = path.join(ROOT, 'www');

const EXCLUDE_DIRS = new Set(['node_modules', 'android', 'ios', '.git', '.github', 'www', 'scripts']);
const EXCLUDE_FILES = new Set([
  'package.json',
  'package-lock.json',
  'capacitor.config.js',
  'capacitor.config.json',
  '.gitignore',
]);
const EXCLUDE_EXT = new Set(['.py', '.md']);

fs.rmSync(DEST, { recursive: true, force: true });
fs.mkdirSync(DEST);

let copied = 0;
for (const name of fs.readdirSync(ROOT)) {
  if (name.startsWith('.')) continue;
  if (EXCLUDE_DIRS.has(name)) continue;
  if (EXCLUDE_FILES.has(name)) continue;
  if (EXCLUDE_EXT.has(path.extname(name))) continue;

  fs.cpSync(path.join(ROOT, name), path.join(DEST, name), { recursive: true });
  copied++;
}

console.log(`Copied ${copied} items to ${DEST}`);
