#!/usr/bin/env node
// Esegue uno script Python con il primo interprete che funziona.
// Su Windows "python3" di solito è un alias che apre lo Store, quindi una
// prova con --version decide quale comando usare. Stdin e codice di uscita
// passano invariati. Senza Python l'hook esce con 0: è solo un avviso.

const { spawnSync } = require('node:child_process');

for (const command of ['python3', 'python', 'py']) {
  const probe = spawnSync(command, ['--version'], { stdio: 'ignore' });
  if (!probe.error && probe.status === 0) {
    const run = spawnSync(command, process.argv.slice(2), { stdio: 'inherit' });
    process.exit(run.status ?? 0);
  }
}
process.exit(0);
