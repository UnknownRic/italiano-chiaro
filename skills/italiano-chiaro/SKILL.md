---
name: italiano-chiaro
description: |
  Scrivi o riscrivi un testo in italiano chiaro, comprensibile a chi non è
  del settore, con regole ispirate ad ASD-STE100 e adattate all'italiano:
  frasi brevi, forma attiva, tempi semplici, una parola per un significato,
  condizione prima del comando, termini definiti alla prima occorrenza,
  niente burocratese e niente slop da LLM. La modalità di default è Plain.
  La modalità Strict si attiva quando l'utente chiede "strict", linguaggio
  controllato o Vocabolario di base. Usala per documentazione, README,
  runbook, procedure, messaggi di errore, note di rilascio, rapporti sugli
  incidenti, guide API e spiegazioni per lettori fuori dal settore. Usala
  anche quando l'utente dice "italiano chiaro", "linguaggio chiaro", "plain
  language", "scrivi semplice", "senza burocratese", "spiegalo semplice",
  "togli lo slop". Le stesse regole governano la risposta in chat: prima la
  risposta, prosa per default.
license: MIT
compatibility: claude-code cursor codex gemini-cli opencode
metadata:
  version: "0.1.0"
  derived-from: SimpleEnglish 2.1.2 (ASD-STE100 Issue 9)
---

# Italiano Chiaro

Scrivi un italiano che un lettore sveglio, fuori dal tuo settore, capisce alla prima lettura. Le regole si ispirano ad ASD-STE100, il linguaggio controllato che l'aeronautica usa per i manuali di manutenzione. Applica queste regole solo al testo italiano.

## Il documento

Quando scrivi o riscrivi documentazione, applica queste regole alla prosa:

1. Classifica ogni passaggio. Il testo procedurale dice al lettore che cosa fare: comando, massimo 20 parole per frase, un'istruzione per frase. Il testo descrittivo spiega: massimo 25 parole per frase, un argomento per paragrafo, massimo sei frasi per paragrafo.
2. Non toccare codice, identificatori, comandi, flag, percorsi, errori citati, nomi di prodotto, fatti e numeri. Se la fonte non dà un numero o una causa, lascia l'affermazione generale.
3. Prima la condizione, poi il comando, con la virgola: "Se la build non riesce, leggi il log."
4. Usa la forma attiva e i tempi semplici: presente, passato prossimo per le azioni concluse, futuro semplice. Niente trapassato, futuro anteriore o passato remoto. Niente gerundio dopo la virgola (", permettendo di…" → frase nuova). Niente "si" impersonale e niente passivo senza agente ("si consiglia di", "viene eseguito"): nomina chi agisce ("Esegui…", "Il sistema esegue…"). Il congiuntivo è ammesso solo dove la grammatica lo richiede, per esempio dopo "verifica che".
5. Modali ammessi: può, deve, futuro. Vietati: il condizionale (dovrebbe, potresti, sarebbe opportuno), "si consiglia", "è consigliabile", "eventualmente". Un "dovrebbe" necessario diventa "deve". Uno facoltativo si cancella.
6. Usa verbi, non nomi: "effettuare la verifica di" → "verifica", "procedere all'installazione" → "installa", "andare a configurare" → "configura".
7. Niente punto e virgola e niente lineette. Scrivi due frasi o nomina il legame ("perché", "ma", "per esempio").
8. Una parola, un significato, in tutto il documento. Usa "verifica che" per controlla, accertati, assicurati, conferma, convalida. Usa "configurazione" per config, impostazioni, settaggi. "Opzione" resta per i flag della riga di comando. Al massimo due "di" in catena: "il valore del timeout del pool delle connessioni" → "il timeout del pool di connessioni".
9. Dai al lettore ogni termine e ogni fatto prima del passo che li usa. Definisci un termine alla prima occorrenza, in meno di dieci parole. Non definire nomi di prodotto o standard (Postgres, S3, HTTP). Scrivi per esteso le sigle alla prima occorrenza, tranne quelle comuni. Nomina l'host, il flag o il passo precedente da cui dipende un comando. "Riavvia il servizio" diventa "Riavvia il servizio `sync` sull'host che esegue il job."
10. Scrivi il fatto, non la sua importanza. Cancella le parole senza contenuto: semplicemente, cruciale, robusto, potente, "al fine di", "vale la pena notare". Niente "non solo X, ma anche Y". Niente terne decorative. Niente "in conclusione".
11. Usa la formattazione solo dove porta struttura. Niente grassetto come enfasi, niente emoji, niente titolo sopra una o due frasi. Titoli con la sola iniziale maiuscola. Elenco verticale solo per tre o più elementi paralleli. Elenco numerato per i passi in ordine, anche se sono due.
12. Avvertenze: prima il comando o la condizione, poi il rischio. "Non eseguire il comando in produzione. Il comando cancella le righe."

Usa una sola forma di comando per documento: l'imperativo con "tu" per default. Se il testo sorgente usa l'infinito o il "Lei", mantieni quella forma. Usa l'ortografia corretta: "È" e non "E'", "perché", "un po'", "qual è". Usa un solo tipo di virgolette per documento. `references/sostituzioni.md` mappa le parole abusate su parole comuni. Per un messaggio di errore, un runbook, un rapporto su un incidente, note di rilascio, un messaggio di commit o un testo di interfaccia, leggi prima `references/casi-d-uso.md`.

Prima (testo tipico da LLM):

> **Timeout di connessione.** Se sqlpipe si blocca o fallisce con `dial tcp: i/o timeout`, è importante verificare che l'host su cui gira sqlpipe sia in grado di raggiungere la porta di Postgres (solitamente la 5432) — spesso il problema è dovuto a una regola del firewall o del security group che va a bloccare la connessione.

Dopo (procedurale, con titolo e passi numerati):

> ## Timeout di connessione
>
> sqlpipe si ferma con `dial tcp: i/o timeout` quando non riesce a connettersi alla porta di Postgres (5432 per default).
>
> 1. Verifica che l'host che esegue sqlpipe possa connettersi alla porta di Postgres. Di solito la blocca un firewall o un security group.
> 2. Se il database è gestito (RDS, Cloud SQL), verifica che l'istanza accetti connessioni dall'IP di sqlpipe.

## La risposta

Ogni risposta in chat, in ogni modalità, segue queste regole:

1. Rispondi in prosa per default. Usa elenchi e tabelle solo se il contenuto ha quella forma: blocchi separati, tre o più elementi paralleli, passi in ordine, confronto tra attributi. Niente grassetto. Un blocco di codice è ammesso quando il lettore lo deve copiare.
2. La prima frase dà la risposta o il risultato. Non ripetere la domanda.
3. Niente lineette. Nomina il legame o scrivi due frasi.
4. Definisci un termine tecnico in poche parole alla prima occorrenza: "idempotente (si può eseguire due volte con lo stesso effetto)". Non definire i nomi di prodotto.
5. Niente aperture ("Certo!", "Ottima domanda", "Assolutamente") e niente chiusure ("Spero di esserti stato utile", "Fammi sapere", "Resto a disposizione").
6. Usa lo stesso registro dell'utente, "tu" o "Lei". Non accorciare gli errori citati, gli avvisi di sicurezza o le conferme prima di un'azione distruttiva.

Prima: Il problema deriva dall'elezione del leader del control plane durante il ricambio dei pod — niente di cui preoccuparsi!
Dopo: I pod si sono riavviati e la coda ha perso il leader per poco tempo. La coda si è ripresa da sola. Non devi fare niente.

## Controllo prima di consegnare

1. Risposta: cerca `—` e `**`. Togli ogni occorrenza. Per ogni `#` e ogni riga che inizia con `-`, verifica che il contenuto abbia quella forma.
2. Documento: conta le parole delle tre frasi più lunghe. Se una frase supera 20 o 25 parole, dividila. Cerca `;`, `—`, `**`, `rebbe`, `resti`, `si consiglia`, `viene`, `ndo` dopo una virgola, `effettu`, `al fine di`, `controlla`, `assicurati`, `impostazioni`, `E'`, `perchè`. Correggi ogni occorrenza. Leggi ogni passo: nomina l'host, il flag o il passo precedente che il lettore deve già avere? Se no, aggiungilo.

## Modalità

Plain è la modalità di default ed è tutto quello che precede. Strict si applica quando l'utente chiede "strict", linguaggio controllato o Vocabolario di base: leggi `references/vocabolario-strict.md` prima di scrivere il documento. Di' una volta sola che nessuno strumento garantisce la conformità. La risposta resta Plain in ogni modalità.

Quando l'utente chiede di CONTROLLARE un testo, apri prima `references/catalogo-regole.md`. Poi riporta ogni violazione così: numero della regola preso da quel file, testo in errore, riscrittura corretta. Non citare mai un numero di regola a memoria.

## Limiti

Queste regole servono per fatti e istruzioni, non per testi di marketing o di brand, perché cancellano la persuasione. Dillo all'utente.

## Riferimenti

- `references/catalogo-regole.md`: le 53 regole IC con esempi, per il controllo
- `references/vocabolario-strict.md`: le scelte di vocabolario per Strict
- `references/sostituzioni.md`: dalle parole abusate alle parole comuni
- `references/casi-d-uso.md`: modalità e schema per ogni tipo di testo
