# Italiano Chiaro

Italiano Chiaro è una skill per agenti di programmazione come Claude Code e Codex. La skill fa scrivere all'agente un italiano che un lettore fuori dal settore capisce alla prima lettura. Le regole vengono da ASD-STE100, il linguaggio controllato dei manuali di manutenzione aeronautica, e sono adattate all'italiano.

Le regole coprono due registri. Il documento è il testo che resta: README, runbook, messaggi di errore, note di rilascio, rapporti sugli incidenti, commit. La risposta è il messaggio in chat. Le regole valgono solo per il testo italiano, quindi il plugin può stare insieme a un plugin per un'altra lingua.

Italiano Chiaro deriva da [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) di AminBlg. La licenza è MIT.

## Installazione

Plugin per Claude Code, con l'hook di avvio, i controlli di scrittura e lo stile di output:

```bash
claude plugin marketplace add UnknownRic/italiano-chiaro
```

```bash
claude plugin install italiano-chiaro@italiano-chiaro
```

Lo stile di output si chiama `italiano-chiaro:italiano-chiaro`. Il nome breve non funziona. Per attivarlo, scrivi `{"outputStyle": "italiano-chiaro:italiano-chiaro"}` in `~/.claude/settings.json`.

Plugin per Codex, con l'hook di avvio:

```bash
codex plugin marketplace add UnknownRic/italiano-chiaro
```

```bash
codex plugin add italiano-chiaro@italiano-chiaro
```

Codex chiede di approvare l'hook prima della prima esecuzione. Gli hook richiedono Node.js. I controlli di scrittura richiedono anche Python 3. I dettagli sono in [`src/hooks/README.md`](src/hooks/README.md).

Per un agente senza skill, copia il blocco delle regole di [`prompts/prompt-di-sistema.md`](prompts/prompt-di-sistema.md) nel prompt di sistema, in `AGENTS.md` o in `.cursorrules`. In fondo alla pagina c'è una versione breve per i contesti piccoli.

## Uso

Con il plugin, le regole sono attive da quando la sessione parte. Non devi nominare la skill. Chiedi un testo tecnico e l'agente lo scrive con le regole. Per un testo che esiste già, chiedi "riscrivi questo in italiano chiaro".

Un esempio. Il testo tipico di un modello linguistico:

> Se sqlpipe si blocca con `dial tcp: i/o timeout`, è importante andare a verificare che l'host sia in grado di raggiungere la porta di Postgres.

Lo stesso testo con le regole:

> 1. Verifica che l'host che esegue sqlpipe possa connettersi alla porta di Postgres (5432 per default).
> 2. Se la porta è chiusa, controlla il firewall o il security group.

Altri esempi sono in [`examples/prima-dopo.md`](examples/prima-dopo.md).

## Le regole principali

Il catalogo di tutte le regole è in [`skills/italiano-chiaro/references/catalogo-regole.md`](skills/italiano-chiaro/references/catalogo-regole.md). Queste sono le regole che cambiano di più un testo:

- Al massimo 20 parole per frase nel testo procedurale e 25 nel testo descrittivo.
- Prima la condizione, poi il comando: "Se la build non riesce, leggi il log."
- Forma attiva e tempi semplici. Chi agisce ha un nome.
- Niente condizionale, niente gerundio dopo la virgola, niente "si" impersonale.
- Verbi al posto dei nomi: `installa` e non `procedi all'installazione`.
- Una parola per un significato: `verifica che` per ogni controllo, `configurazione` al posto di `impostazioni` e `config`.
- Niente burocratese e niente parole vuote da modello linguistico.
- Niente punto e virgola, niente lineette, niente grassetto come enfasi.

Nella risposta in chat, la prima frase dà la risposta. La forma di default è la prosa. Un elenco o una tabella servono solo quando il contenuto ha quella forma.

Le regole non toccano il codice, i comandi, i percorsi, gli errori citati, i nomi di prodotto e i fatti.

## Modalità Plain e Strict

Plain è la modalità di default. Applica le regole del catalogo.

Strict aggiunge un vocabolario controllato: una sola parola per ogni azione comune. Per attivarla, chiedi "strict", linguaggio controllato o Vocabolario di base. Le scelte sono in [`vocabolario-strict.md`](skills/italiano-chiaro/references/vocabolario-strict.md). La risposta in chat resta Plain in ogni modalità.

Nessuno strumento garantisce la conformità ad ASD-STE100. Lo standard è per l'inglese e non ha una versione italiana.

## Il linter

`lint/chiaro_lint.py` cerca nel testo le violazioni più facili da trovare con le espressioni regolari. Richiede solo Python 3, senza librerie esterne.

```bash
python3 lint/chiaro_lint.py --type procedural runbook.md
```

Il tipo può essere `procedural`, `descriptive` o `reply`. Il linter divide i risultati in due livelli. Un errore è quasi sempre una violazione. Un avviso chiede una persona che decida, per esempio un titolo con due maiuscole che contiene un nome proprio.

Altre opzioni:

- `--gate` esce con 1 se trova almeno un errore. Serve nella CI.
- `--detail` mostra la riga e il testo di ogni risultato.
- `-` legge il testo da standard input.
- `--self-test` esegue i test interni.

Su Windows usa `python` al posto di `python3`.

Il plugin per Claude Code usa lo stesso linter in due hook. Dopo ogni scrittura di un file Markdown, l'agente vede gli errori del file. Alla fine di ogni risposta, l'agente riceve un messaggio se la risposta contiene lineette, grassetto, parole vuote o formule di cortesia. Gli hook non bloccano mai la sessione.

## Limiti

- Il linter trova le violazioni di forma, non quelle di senso. Un testo può passare il linter ed essere poco chiaro.
- Il linter segnala anche una parola vietata dentro una citazione. Per evitarlo, metti la parola tra apici inversi.
- Il filtro per la lingua conta alcune parole comuni dell'italiano. Un file con metà testo in un'altra lingua passa dal linter per intero.
- Nessuna metrica è stata misurata su questa versione. Le metriche di SimpleEnglish valgono per l'inglese e non sono riportate qui.
- Le regole sono pensate per la documentazione tecnica. Non sono adatte a un testo di marketing o a un testo letterario.

## Struttura della repo

| Percorso | Contenuto |
|---|---|
| `skills/italiano-chiaro/` | La skill e i riferimenti |
| `prompts/` | Il blocco delle regole per un prompt di sistema |
| `output-styles/` | Lo stile di output per Claude Code |
| `src/hooks/` | Gli hook e i loro test |
| `lint/` | Il linter, le liste di parole e il controllo dei testi duplicati |
| `examples/` | Coppie di testi prima e dopo |

Prima di ogni push, esegui `python3 lint/check_numbers.py`. Lo script verifica che i testi duplicati e le versioni siano allineati.

## Crediti

Italiano Chiaro deriva da [SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) di AminBlg, versione 2.1.2, con licenza MIT. La struttura del plugin, gli hook e il linter vengono da quel progetto. Le regole per l'italiano usano anche le indicazioni dell'Accademia della Crusca e della norma ISO 24495-1 sul linguaggio chiaro.

ASD-STE100 è un marchio di ASD. Questo progetto non ha legami con ASD. La specifica ufficiale è gratuita su [asd-ste100.org](https://www.asd-ste100.org).

## Licenza

MIT. Il testo è in [`LICENSE`](LICENSE).
