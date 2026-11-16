# Casi d'uso oltre la documentazione

STE è nato per i manuali di manutenzione degli aerei. Le stesse proprietà servono in ogni testo dove un errore di lettura ha un costo: un significato per parola, frasi brevi, condizione prima del comando. Ogni caso sotto indica la modalità e gli adattamenti.

## Messaggi di errore e output da riga di comando

Modalità: procedurale. Un messaggio di errore è un'istruzione per un lettore che ha un guasto in corso.

Schema: scrivi che cosa è successo (passato prossimo), scrivi la causa se la conosci, dai il comando o la condizione che risolve.

> Prima: Ops! Qualcosa è andato storto durante il tentativo di stabilire una connessione. Si prega di assicurarsi che le credenziali siano configurate correttamente e di riprovare.
> Dopo: La connessione al database non è riuscita. La password dell'utente `app` è sbagliata. Imposta `DB_PASSWORD` e riprova.

## Runbook e procedure operative

Modalità: procedurale. Un runbook per chi è di turno è un manuale di manutenzione, cioè il tipo di testo per cui STE è nato.

- Ogni passo è un comando, con un'istruzione per passo e la condizione all'inizio.
- Un'avvertenza sta prima del suo passo: prima il comando, poi il rischio.
- Nessuna frase supera 20 parole.

## Rapporti sugli incidenti

Modalità: descrittiva, solo passato prossimo e orari precisi. Una frase come "abbiamo riscontrato delle problematiche" nasconde quando sono successe le cose.

> Prima: Abbiamo identificato una problematica che potrebbe aver impattato la possibilità di alcuni utenti di accedere al servizio.
> Dopo: Tra le 14:02 e le 14:31 UTC, il 12% delle richieste è fallito. Un deploy delle 14:00 ha tolto il passo che riempie la cache.

Le regole vietano le attenuazioni come "potrebbe aver impattato". Il rapporto scrive quello che si sa e scrive "causa ignota" per il resto.

## Messaggi di commit e descrizioni di pull request

Modalità: oggetto come comando, corpo descrittivo. Scegli una forma per l'oggetto, imperativo o infinito, e usala in tutta la repo. Applica al corpo le sostituzioni e il limite di 25 parole. Cancella "questa PR ha l'obiettivo di".

## Changelog e note di rilascio

Modalità: descrittiva. Una voce, una modifica, una frase dove è possibile. Una voce "Incompatibile:" segue lo schema delle avvertenze, con il comando all'inizio: "Aggiorna le chiamate a `v2/users`. Il campo `name` è diviso in `first_name` e `last_name`."

## Istruzioni per agenti AI (prompt, AGENTS.md, skill)

Modalità: procedurale. Un prompt di sistema è una procedura per un lettore che non può fare domande.

- Un'istruzione per frase rende ogni regola facile da citare e difficile da seguire a metà.
- Una parola per un significato impedisce al modello di trattare "controlla", "verifica" e "convalida" come tre operazioni.
- Una condizione all'inizio ("Se la build non riesce, fermati") funziona meglio di una condizione in coda, che i modelli perdono.
- Niente "dovrebbe". Un modello legge "dovrebbe" come facoltativo. Scrivi "deve" o cancella la regola.

## Risposte dell'assistenza e pagine di stato

Modalità: descrittiva, limite di 25 parole. Usa il registro del servizio, "tu" o "Lei", in tutto il messaggio.

> Prima: Ci scusiamo sinceramente per gli eventuali disagi che ciò potrebbe aver arrecato.
> Dopo: L'API non ha risposto per 18 minuti. I file caricati in quel periodo sono salvi. Il sistema li elabora oggi.

## Mail tecniche

Modalità: descrittiva. La prima frase dice che cosa chiedi o che cosa comunichi. Poi dai i fatti che servono per decidere, uno per frase. Chiudi con l'azione richiesta e la data.

> Prima: Con la presente si comunica che, a seguito delle verifiche effettuate, si renderebbe necessario procedere all'aggiornamento del certificato.
> Dopo: Il certificato di `api.example.com` scade il 3 marzo. Aggiorna il certificato entro il 28 febbraio.

## Preparazione alla traduzione

Modalità: Strict. Un significato per parola e la grammatica completa tolgono molte ambiguità che un traduttore, umano o automatico, deve altrimenti indovinare. Sciogli i soggetti sottintesi quando il soggetto cambia.

## Testi di interfaccia e stati vuoti

Modalità: procedurale, con limiti di lunghezza rigidi. Pulsanti ed etichette sono nomi tecnici e sono esenti. Il testo segue le regole: "Nessun progetto. Crea un progetto per iniziare."

## Dove queste regole non servono

Non usare queste regole per pagine di marketing, annunci di lancio, articoli di blog o testi di brand. Le regole tolgono la persuasione. Scrivi quei testi con la tua voce e usa le regole per la documentazione a cui rimandano.
