#!/usr/bin/env node
// Deriva da src/hooks/simple-english-activate.js di SimpleEnglish (AminBlg, MIT).

const fs = require('node:fs');
const path = require('node:path');

// Claude Code limita lo stdout di un hook a 10.000 caratteri. Oltre il limite
// scrive il testo in un file e passa al modello solo un'anteprima.
const MAX_CHARS = 9500;

const FALLBACK_CONTEXT = `ITALIANO CHIARO ATTIVO IN AUTOMATICO

Applica le regole di Italiano Chiaro solo al testo italiano. Usa frasi brevi, forma attiva, un termine per un significato e la condizione prima del comando. Non cambiare codice, identificatori, comandi o errori citati. Non toccare il testo in altre lingue.`;

const HEADER = [
  'ITALIANO CHIARO ATTIVO IN AUTOMATICO',
  '',
  "Segui queste regole di scrittura senza aspettare che l'utente nomini la skill. Applica le regole solo al testo italiano e non toccare il testo in altre lingue. La skill completa, con il catalogo delle regole e la modalità di controllo, è in skills/italiano-chiaro/SKILL.md in questo plugin. Leggila per un controllo o per la modalità Strict.",
  '',
].join('\n');

function candidates(pluginRoot, hookDirectory, relative) {
  const roots = [];
  if (pluginRoot) {
    roots.push(pluginRoot);
  }
  roots.push(path.join(hookDirectory, '..', '..'), path.join(hookDirectory, '..'));
  return roots.map((root) => path.join(root, ...relative));
}

function promptCandidates(pluginRoot, hookDirectory) {
  return candidates(pluginRoot, hookDirectory, ['prompts', 'prompt-di-sistema.md']);
}

function readFirstFile(list) {
  for (const candidate of list) {
    try {
      return fs.readFileSync(candidate, 'utf8');
    } catch (error) {
      // Mancante, illeggibile o una cartella: prova il candidato successivo.
    }
  }
  return '';
}

function stripFrontmatter(content) {
  return content.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, '');
}

// prompts/prompt-di-sistema.md è una pagina per le persone: un titolo, un
// paragrafo che dice dove incollare il blocco, il blocco tra due righe "---",
// poi la versione breve. Il modello riceve solo il blocco.
function ruleBlock(content) {
  const fence = /^---[ \t]*\r?$/m;
  const first = content.search(fence);
  if (first === -1) {
    return content;
  }
  const rest = content.slice(first).replace(fence, '');
  const second = rest.search(fence);
  return second === -1 ? rest : rest.slice(0, second);
}

function buildContext(promptText) {
  if (!promptText) {
    return FALLBACK_CONTEXT;
  }
  const out = HEADER + ruleBlock(stripFrontmatter(promptText)).trim();
  if (out.length > MAX_CHARS) {
    process.stderr.write(`hook italiano-chiaro: il testo è di ${out.length} caratteri, oltre il limite di ${MAX_CHARS}. Invio le regole di riserva\n`);
    return FALLBACK_CONTEXT;
  }
  return out;
}

function main() {
  const pluginRoot = process.env.PLUGIN_ROOT || process.env.CLAUDE_PLUGIN_ROOT;
  process.stdout.write(buildContext(readFirstFile(promptCandidates(pluginRoot, __dirname))));
}

if (require.main === module) {
  main();
}

module.exports = {
  FALLBACK_CONTEXT,
  MAX_CHARS,
  buildContext,
  promptCandidates,
  readFirstFile,
  ruleBlock,
  stripFrontmatter,
};
