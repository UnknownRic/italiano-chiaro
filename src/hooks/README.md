# Hook di Italiano Chiaro

I plugin per Claude Code e Codex includono un hook `SessionStart`. L'hook carica le regole di Italiano Chiaro quando una sessione inizia, riprende, si svuota o si compatta. Non devi nominare la skill.

Gli hook richiedono Node.js. I controlli di scrittura richiedono anche Python 3.

## Che cosa invia l'hook di avvio

`italiano-chiaro-activate.js` scrive su standard output il blocco delle regole di `prompts/prompt-di-sistema.md`. Il titolo della pagina, le istruzioni e la versione breve restano fuori. Claude Code limita l'output di un hook a 10.000 caratteri, e il blocco condensato sta sotto questo limite. L'hook nomina il percorso della skill completa, così il modello può leggerla per un controllo o per la modalità Strict.

Il blocco dice al modello di applicare le regole solo al testo italiano. Per questo il plugin può stare insieme a un plugin per un'altra lingua.

Se l'hook non riesce a leggere il file del prompt, prova il percorso successivo. Se ogni percorso fallisce, l'hook scrive un blocco di riserva ed esce con 0. La sessione parte comunque.

## Dove ogni strumento carica l'hook

- Claude Code: il campo `hooks` in `.claude-plugin/plugin.json`.
- Codex: `.codex-plugin/hooks.json`, indicato dal campo `hooks` in `.codex-plugin/plugin.json`. Il catalogo è `.agents/plugins/marketplace.json`.

## Controlli di scrittura (solo Claude Code)

Altri due hook girano in Claude Code. Sono avvisi e non bloccano mai.

- `PostToolUse` su `Write` e `Edit`: quando il file è Markdown, `lint_hook.py` lo passa a `lint/chiaro_lint.py` e mostra al modello gli errori con riga e testo.
- `Stop`: lo stesso script legge l'ultima risposta e aggiunge un messaggio di sistema quando la risposta viola il registro. Le violazioni sono: lineetta, grassetto, parola slop, apertura di cortesia, chiusura di cortesia.

I due controlli saltano il testo che non è italiano. Lo script conta alcune parole comuni dell'italiano: sotto il 6% delle parole, non segnala niente.

`run-python.js` avvia `lint_hook.py`. Prova `python3`, poi `python`, poi `py`, perché su Windows `python3` di solito non esiste. Senza Python, il controllo non fa niente.

## Che cosa salta il controllo dei file

Le regole coprono i documenti che scrivi per un lettore. Non coprono i file che l'agente tiene per sé, come i file di memoria. Il controllo `PostToolUse` salta tre gruppi di percorsi:

- Ogni percorso nella cartella di configurazione di Claude. Il controllo legge `CLAUDE_CONFIG_DIR` e, se manca, usa `~/.claude`.
- Ogni percorso con una cartella `.claude`, per esempio `progetto/.claude/agent-memory/MEMORY.md`.
- Ogni percorso che corrisponde a un glob in `ITALIANO_CHIARO_LINT_EXCLUDE`.

`ITALIANO_CHIARO_LINT_EXCLUDE` contiene i glob, divisi dal separatore di percorso del sistema (`:` su Linux e macOS, `;` su Windows). In un glob, `*` vale anche per `/`.

```bash
export ITALIANO_CHIARO_LINT_EXCLUDE="$HOME/note/*:*/CHANGELOG.md"
```

Per spegnere il controllo dei file, imposta la variabile a `*`. Il controllo `Stop` resta attivo.

## Test

Dalla radice della repo:

```bash
node --test src/hooks/italiano-chiaro-activate.test.js
python3 src/hooks/test_lint_hook.py
```

Su Windows usa `python` al posto di `python3`.
