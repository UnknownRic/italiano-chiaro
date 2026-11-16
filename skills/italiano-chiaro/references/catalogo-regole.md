# Catalogo delle regole: Italiano Chiaro per il testo software

Leggi questo file per la modalità di controllo, per la modalità Strict, o quando un numero di regola è in dubbio. `SKILL.md` nomina le regole che cambiano di più il risultato. Questo file contiene il catalogo completo.

Le regole sono 53, in 10 sezioni, con numerazione propria IC-x.y. La colonna "Fonte" indica da dove viene l'idea, non una citazione. "STE" è ASD-STE100 Issue 9, con il numero della regola originale. "ISO" è la norma ISO 24495-1 sul linguaggio chiaro. "Crusca" è la Guida alla redazione degli atti amministrativi (ITTIG-CNR e Accademia della Crusca, 2011). "IC" è una regola di questa skill. Il testo ufficiale di STE è gratuito su asd-ste100.org.

### Sezione 1: parole (IC-1.1 a IC-1.6)

| Regola | Istruzione | Fonte |
|---|---|---|
| IC-1.1 | Puoi usare i termini del tuo settore come nomi tecnici ("webhook", "commit", "endpoint"). | STE 1.5, 1.8 |
| IC-1.2 | Una cosa, un nome. Non scrivere "config" in un punto e "impostazioni" in un altro. | STE 1.11 |
| IC-1.3 | Un concetto, un verbo. Usa "verifica che" per controlla, accertati, assicurati, conferma, convalida. | STE 1.11, 9.4 |
| IC-1.4 | Se esiste una parola comune, usala: "usare" e non "utilizzare". | ISO, Crusca |
| IC-1.5 | Non trasformare un nome tecnico in verbo. | STE 1.7 |
| IC-1.6 | Un termine tecnico inglese senza equivalente d'uso resta in inglese, invariato al plurale e sempre con lo stesso nome ("i commit", "il deploy"). | IC |

Prima: Puoi webhookare l'evento, poi fai un deploy.
Dopo: Invia l'evento al webhook. Poi esegui il deploy del servizio.

### Sezione 2: catene nominali (IC-2.1 a IC-2.2)

| Regola | Istruzione | Fonte |
|---|---|---|
| IC-2.1 | Scrivi al massimo due "di" in catena. | STE 2.1, adattata |
| IC-2.2 | Se un nome tecnico è più lungo, scrivilo per intero una volta. Poi usa una forma breve. | STE 2.2 |

Prima: il valore del timeout del pool delle connessioni del database
Dopo: il timeout del pool di connessioni

### Sezione 3: verbi (IC-3.1 a IC-3.8)

| Regola | Istruzione | Fonte |
|---|---|---|
| IC-3.1 | Usa solo: infinito, imperativo, presente, passato prossimo, futuro semplice. Niente trapassato, futuro anteriore o passato remoto. | STE 3.2, adattata |
| IC-3.2 | Usa la forma attiva. Il passivo è ammesso solo quando chi agisce è ignoto. | STE 3.6 |
| IC-3.3 | Niente "si" impersonale o passivante. Nomina chi agisce: il lettore ("tu") o il sistema. | Crusca, STE 3.6 |
| IC-3.4 | Niente gerundio dopo la virgola. Scrivi una frase nuova. | STE 3.5, adattata |
| IC-3.5 | Descrivi un'azione con un verbo, non con un nome. | STE 3.7, Crusca |
| IC-3.6 | Niente "andare a" più infinito. | IC |
| IC-3.7 | Modali ammessi: può, deve, futuro. Niente condizionale. La scala dei modali in fondo dà la sostituzione. | STE, sezione 3 |
| IC-3.8 | Usa il congiuntivo solo dove la grammatica lo richiede, per esempio dopo "verifica che". Sostituisci affinché, qualora, benché, sebbene, purché, laddove con per, se, ma, anche se. | IC |

| Regola | Prima | Dopo |
|---|---|---|
| IC-3.2 | Il file viene letto dal servizio. | Il servizio legge il file. |
| IC-3.3 | Si consiglia di riavviare il servizio. | Riavvia il servizio. |
| IC-3.4 | Il servizio salva i dati ogni ora, permettendo il ripristino. | Il servizio salva i dati ogni ora. Così puoi ripristinare i dati. |
| IC-3.5 | Procedere all'installazione del pacchetto. | Installa il pacchetto. |
| IC-3.6 | Ora andiamo a configurare il client. | Configura il client. |
| IC-3.8 | Qualora la build fallisca, leggi il log. | Se la build non riesce, leggi il log. |

### Sezione 4: frasi (IC-4.1 a IC-4.5)

| Regola | Istruzione | Fonte |
|---|---|---|
| IC-4.1 | Scrivi frasi brevi e chiare. | STE 4.1 |
| IC-4.2 | Non togliere parole per accorciare. Tieni articoli e preposizioni. | STE 4.2 |
| IC-4.3 | Usa un elenco verticale per tre o più elementi paralleli, o per i passi in ordine. Due punti sulla frase che introduce, iniziale maiuscola, niente elenchi annidati, niente istruzioni mescolate a fatti. | STE 4.3 |
| IC-4.4 | Collega le frasi sullo stesso argomento con una parola di legame ("Poi", "Quindi", "Per questo"). | STE 4.4 |
| IC-4.5 | Ogni pronome ha un referente chiaro. Scrivi "questo" più il nome: "questo timeout", non "questo". | STE GR-3, GR-4 |

La regola IC-4.2 vieta lo stile telegrafico. L'italiano chiaro ha frasi brevi con la grammatica completa:

Prima: Verificare esistenza file prima esecuzione.
Dopo: Verifica che il file esista prima di eseguire il comando.

### Sezione 5: testo procedurale (IC-5.1 a IC-5.5)

| Regola | Istruzione | Fonte |
|---|---|---|
| IC-5.1 | Massimo 20 parole per frase, avvertenze comprese. | STE 5.1 |
| IC-5.2 | Un'istruzione per frase. Un passo può aggiungere una frase per il risultato immediato o per un limite. | STE 5.2 |
| IC-5.3 | Usa una sola forma di comando per documento. Il default è l'imperativo con "tu". Se il testo sorgente usa l'infinito o il "Lei", mantieni quella forma. | STE 5.3, adattata |
| IC-5.4 | Metti la condizione prima del comando, separata da una virgola. | STE 5.4 |
| IC-5.5 | Le note danno informazioni, mai istruzioni o limiti. La procedura deve funzionare anche per chi cancella tutte le note. | STE 5.5 |

Prima: Ti conviene recuperare la chiave API dalla dashboard prima di configurare il client, cosa che puoi fare nelle Impostazioni.
Dopo: Copia la chiave API dalla dashboard, nella pagina Impostazioni. Poi configura il client con questa chiave.

### Sezione 6: testo descrittivo (IC-6.1 a IC-6.6)

| Regola | Istruzione | Fonte |
|---|---|---|
| IC-6.1 | Dai le informazioni per gradi: un fatto nuovo per frase. | STE 6.1 |
| IC-6.2 | Massimo 25 parole per frase. | STE 6.3 |
| IC-6.3 | Un argomento per paragrafo. | STE 6.5 |
| IC-6.4 | Massimo sei frasi per paragrafo. | STE 6.6 |
| IC-6.5 | Definisci un termine alla prima occorrenza, in meno di dieci parole. Non definire nomi di prodotto o standard. | ISO |
| IC-6.6 | Scrivi per esteso una sigla alla prima occorrenza, tranne quelle comuni (HTTP, PDF). | Crusca |

Prima: Il job usa un lock per evitare esecuzioni concorrenti.
Dopo: Il job usa un lock (un blocco che ammette un solo processo alla volta). Il lock impedisce due esecuzioni nello stesso momento.

### Sezione 7: avvertenze (IC-7.1 a IC-7.3)

| Regola | Istruzione | Fonte |
|---|---|---|
| IC-7.1 | Usa una parola che mostra il livello del rischio: "AVVERTENZA" per un danno alle persone, "ATTENZIONE" per un danno a dati o sistemi. | STE 7.1 |
| IC-7.2 | Inizia con un comando o una condizione chiari. | STE 7.2 |
| IC-7.3 | Poi scrivi il rischio o il risultato possibile. | STE 7.3 |

Usa lo stesso schema per i flag distruttivi e per le migrazioni che non puoi annullare.

Prima: Si noti che potrebbe verificarsi una perdita di dati in alcune circostanze se il flag distruttivo risulta attivo in produzione.
Dopo: ATTENZIONE: non usare il flag `--force` in produzione. Il flag cancella le righe che non corrispondono alla sorgente.

### Sezione 8: punteggiatura e numero di parole (IC-8.1 a IC-8.8)

| Regola | Istruzione | Fonte |
|---|---|---|
| IC-8.1 | Niente punto e virgola. Scrivi due frasi. | STE 8.1 |
| IC-8.2 | Niente lineetta tra due affermazioni (`—`, `–`, trattino tra spazi). Nomina il legame o scrivi due frasi. Un intervallo (`5–10`), un marcatore di elenco e un flag (`--force`) non sono lineette. | IC |
| IC-8.3 | Le parentesi sono ammesse per riferimenti, sigle, spiegazioni brevi e alternative. | STE 8.3 |
| IC-8.4 | Una parola è una sequenza senza spazi: "dell'istanza" conta uno. Contano uno anche il testo tra backtick, un numero con la sua unità e un nome proprio. | STE 8.5-8.7, adattata |
| IC-8.5 | In un elenco verticale, i due punti chiudono la frase per il conteggio. Ogni voce è una frase nuova. | STE 8.4 |
| IC-8.6 | Usa l'ortografia corretta: "È" e non "E'", "perché" e non "perchè", "un po'" e non "un pò", "qual è" e non "qual'è". | IC |
| IC-8.7 | Usa un solo tipo di virgolette per documento. | IC |
| IC-8.8 | Nei titoli, scrivi maiuscola solo la prima lettera e i nomi propri: "Errori di connessione". | IC |

### Sezione 9: pratiche di scrittura (IC-9.1 a IC-9.6)

| Regola | Istruzione | Fonte |
|---|---|---|
| IC-9.1 | Se la sostituzione parola per parola non funziona, ristruttura la frase. | STE 9.1 |
| IC-9.2 | Tieni uno stile e una terminologia coerenti in tutto il documento. | STE 9.4 |
| IC-9.3 | Scrivi il fatto, non la sua importanza. Cancella le parole senza contenuto. | IC |
| IC-9.4 | Usa la formattazione solo dove porta struttura. Niente grassetto come enfasi, niente emoji, niente titolo sopra una o due frasi. | IC |
| IC-9.5 | Sciogli le abbreviazioni: "es." → "per esempio", "cfr." → "vedi", "i.e." → "cioè". Al posto di "ecc.", nomina gli elementi. | STE GR-6 |
| IC-9.6 | Non toccare codice, identificatori, comandi, flag, percorsi, errori citati, nomi di prodotto, fatti e numeri. | IC |

### Sezione 10: burocratese e anglicismi (IC-10.1 a IC-10.4)

| Regola | Istruzione | Fonte |
|---|---|---|
| IC-10.1 | Usa la parola comune al posto di quella burocratica: "al fine di" → "per", "qualora" → "se", "effettuare" → "fare". La lista è in `sostituzioni.md`. | Crusca |
| IC-10.2 | Niente "suddetto", "predetto", "lo stesso" come pronome. Ripeti il nome. | Crusca |
| IC-10.3 | Niente "e/o". Scrivi "o", oppure "X, Y o entrambi". | IC |
| IC-10.4 | Usa il verbo italiano al posto dell'anglicismo adattato: "settare" → "impostare", "fixare" → "correggere". | IC |

Prima: Al fine di procedere al settaggio del suddetto parametro, si prega di inoltrare la richiesta.
Dopo: Per impostare il parametro `max_conn`, invia la richiesta.

### La scala dei modali

| Hai scritto | Scrivi invece |
|---|---|
| dovrebbe, dovresti (obbligo) | deve, devi, o l'imperativo |
| dovrebbe (raccomandazione) | Cancella, o scrivi il fatto: "X è più veloce perché Y." |
| dovrebbe (previsione: "dovrebbe partire") | Presente o futuro: "parte", "partirà" |
| potrebbe (possibilità) | può, oppure "in alcuni casi" |
| sarebbe opportuno, è consigliabile, si consiglia di | Cancella, o usa "deve" |
| vorrei, vorremmo | Scrivi la richiesta con l'imperativo |
| eventualmente | Scrivi la condizione: "Se X, …" |

## Segni di testo da LLM

Il testo generato scivola in direzioni note. Le regole sopra ne tolgono alcune. Per le altre, controlla documenti e risposte in queste direzioni:

- Importanza gonfiata: niente "cruciale", "fondamentale", "una testimonianza di". Scrivi il fatto.
- Parallelismo negativo: niente "non solo X, ma anche Y".
- Regola del tre: niente terne decorative.
- Attribuzione vaga: niente "gli studi dimostrano". Nomina la fonte o togli l'affermazione.
- Intervalli falsi: niente "da X a Y" senza limiti veri.
- Riassunti che ripetono: niente paragrafi "in conclusione".
- Commenti a margine: niente "è importante notare che".
- Residui di conversazione: niente "Spero di esserti stato utile", niente "Fammi sapere".
- Abitudini di formattazione: niente grassetto decorativo, niente emoji come struttura, niente titolo per due frasi.

Per le singole parole, `sostituzioni.md` dà la sostituzione. Se una parola non porta un fatto, cancellala.

## Scelta delle parole

Una parola, un significato, in tutto il documento (IC-1.2, IC-1.3, IC-9.2).

- Il file con i valori è la "configurazione", mai config, impostazioni o settaggi nello stesso documento.
- Il concetto di verifica è "verifica che", mai controlla, accertati, assicurati, conferma o convalida come verbi.
- Sostituzioni comuni: tuttavia → ma, pertanto → quindi, poiché → perché, effettuare → fare, ora → cancella.
