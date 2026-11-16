const assert = require('node:assert/strict');
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const {
  FALLBACK_CONTEXT,
  MAX_CHARS,
  buildContext,
  promptCandidates,
  readFirstFile,
  stripFrontmatter,
} = require('./italiano-chiaro-activate');

const SCRIPT = path.join(__dirname, 'italiano-chiaro-activate.js');
const LAUNCHER = path.join(__dirname, 'run-python.js');
const REPO_PROMPT = path.join(__dirname, '..', '..', 'prompts', 'prompt-di-sistema.md');

function tmpRoot(promptText) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'ic-hook-'));
  fs.mkdirSync(path.join(root, 'prompts'));
  if (promptText !== undefined) {
    fs.writeFileSync(path.join(root, 'prompts', 'prompt-di-sistema.md'), promptText);
  }
  return root;
}

function runHook(env) {
  return spawnSync(process.execPath, [SCRIPT], { env: { ...process.env, PLUGIN_ROOT: '', CLAUDE_PLUGIN_ROOT: '', ...env }, encoding: 'utf8' });
}

test('preferisce il prompt sotto la radice del plugin', () => {
  const root = path.join('plugin');
  assert.equal(promptCandidates(root, path.join(root, 'src', 'hooks'))[0], path.join(root, 'prompts', 'prompt-di-sistema.md'));
});

test('senza radice del plugin usa la struttura della repo', () => {
  assert.equal(promptCandidates(undefined, path.join('repo', 'src', 'hooks'))[0], path.join('repo', 'prompts', 'prompt-di-sistema.md'));
});

test('salta un candidato illeggibile e legge il successivo', (t) => {
  if (process.platform === 'win32' || (process.getuid && process.getuid() === 0)) {
    t.skip('chmod 000 non blocca la lettura su Windows o per root');
    return;
  }
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'ic-read-'));
  const locked = path.join(dir, 'locked.md');
  const open = path.join(dir, 'open.md');
  fs.writeFileSync(locked, 'SEGRETO');
  fs.chmodSync(locked, 0o000);
  fs.writeFileSync(open, 'APERTO');
  assert.equal(readFirstFile([locked, open]), 'APERTO');
  fs.chmodSync(locked, 0o644);
});

test('salta un candidato che è una cartella', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'ic-dir-'));
  const asDir = path.join(dir, 'prompt-di-sistema.md');
  fs.mkdirSync(asDir);
  const file = path.join(dir, 'vero.md');
  fs.writeFileSync(file, 'VERO');
  assert.equal(readFirstFile([asDir, file]), 'VERO');
});

test('restituisce una stringa vuota quando ogni candidato fallisce', () => {
  assert.equal(readFirstFile(['/inesistente/a.md', '/inesistente/b.md']), '');
});

test('toglie il frontmatter YAML con fine riga LF o CRLF', () => {
  assert.equal(stripFrontmatter('---\nname: x\n---\nCorpo'), 'Corpo');
  assert.equal(stripFrontmatter('---\r\nname: x\r\n---\r\nCorpo'), 'Corpo');
});

test('usa le regole di riserva quando il prompt è vuoto', () => {
  assert.equal(buildContext(''), FALLBACK_CONTEXT);
});

test('il prompt della repo sta sotto il limite di stdout di Claude Code', () => {
  const out = buildContext(fs.readFileSync(REPO_PROMPT, 'utf8'));
  assert.ok(out.length <= MAX_CHARS, `${out.length} > ${MAX_CHARS}`);
  assert.ok(out.includes('LA RISPOSTA'));
  assert.ok(out.includes('solo al testo italiano'), 'manca il limite di lingua');
  assert.ok(!out.includes('Prompt di sistema autonomo'), 'il titolo della pagina è passato');
  assert.ok(!out.includes('Versione breve'), 'la versione breve è passata');
  assert.ok(!out.includes('incolla questo blocco'), 'il paragrafo di istruzioni è passato');
  assert.ok(out.startsWith('ITALIANO CHIARO ATTIVO IN AUTOMATICO'));
});

test('un prompt troppo lungo passa alle regole di riserva', () => {
  assert.equal(buildContext('x'.repeat(MAX_CHARS + 1)), FALLBACK_CONTEXT);
});

test('main() legge il prompt da CLAUDE_PLUGIN_ROOT', () => {
  const r = runHook({ CLAUDE_PLUGIN_ROOT: tmpRoot('COPIA-CLAUDE') });
  assert.equal(r.status, 0);
  assert.ok(r.stdout.includes('COPIA-CLAUDE'));
});

test('main() legge il prompt da PLUGIN_ROOT (Codex)', () => {
  const r = runHook({ PLUGIN_ROOT: tmpRoot('COPIA-CODEX') });
  assert.equal(r.status, 0);
  assert.ok(r.stdout.includes('COPIA-CODEX'));
});

test('main() esce con 0 e le regole di riserva quando non trova niente', () => {
  // Copia lo script lontano da ogni cartella prompts/, poi punta la radice a un albero vuoto.
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'ic-main-'));
  const script = path.join(dir, 'a', 'b', 'hook.js');
  fs.mkdirSync(path.dirname(script), { recursive: true });
  fs.copyFileSync(SCRIPT, script);
  const r = spawnSync(process.execPath, [script], { env: { ...process.env, PLUGIN_ROOT: '', CLAUDE_PLUGIN_ROOT: tmpRoot(undefined) }, encoding: 'utf8' });
  assert.equal(r.status, 0);
  assert.equal(r.stdout, FALLBACK_CONTEXT);
});

test('run-python.js passa stdin e codice di uscita a Python', () => {
  const code = 'import sys; sys.exit(3 if sys.stdin.read() == "ciao" else 1)';
  const r = spawnSync(process.execPath, [LAUNCHER, '-c', code], { input: 'ciao', encoding: 'utf8' });
  assert.equal(r.status, 3);
});
