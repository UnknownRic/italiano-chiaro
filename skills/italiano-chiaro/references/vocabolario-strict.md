# Modalità Strict: le scelte di vocabolario

Leggi questo file quando l'utente chiede "strict", linguaggio controllato o Vocabolario di base. La modalità Strict aggiunge le scelte di vocabolario al documento. Non cambia la risposta all'utente, che resta in modalità Plain.

L'italiano non ha un dizionario controllato come quello di ASD-STE100. Di' questo all'utente, una volta per conversazione e in una frase: nessuno strumento garantisce la conformità, e l'italiano non ha uno standard di linguaggio controllato equivalente a STE.

## Che cosa cambia in Strict

1. Applica tutte le regole Plain senza eccezioni. Un avviso del catalogo diventa un errore.
2. Preferisci le parole del Vocabolario di base (T. De Mauro, Nuovo vocabolario di base della lingua italiana, 2016). Se esiste una parola comune, usala. Questa repo non contiene la lista, perché è protetta da diritti.
3. Applica le decisioni delle tabelle sotto. Sono scelte di questa skill, non di uno standard.

## Decisioni sui verbi del software

| Hai scritto | Scrivi |
|---|---|
| utilizzare, impiegare, avvalersi di, fare uso di | usare |
| effettuare, espletare, porre in essere | fare, o il verbo dell'azione |
| lanciare, far girare, runnare (un comando, un programma) | eseguire |
| far partire, startare, attivare (un servizio) | avviare |
| stoppare, killare, terminare (un processo) | fermare |
| controllare, accertarsi, assicurarsi, confermare, convalidare | verificare che |
| esaminare, consultare, ispezionare (un log, un file) | leggere |
| visualizzare, presentare, esporre | mostrare |
| cancellare, droppare, distruggere (dati, file) | eliminare |
| togliere (un elemento da un elenco, un pacchetto) | rimuovere |
| generare, istanziare (se non serve il senso tecnico) | creare |
| editare, alterare, apportare modifiche a | modificare |
| settare, valorizzare (un parametro) | impostare |
| upgradare, portare alla versione | aggiornare |
| downloadare | scaricare |
| uploadare | caricare |
| inoltrare, trasmettere, far pervenire | inviare |
| pervenire, giungere | arrivare |
| selezionare, optare per | scegliere |
| immettere, inserire (testo da tastiera) | scrivere |
| individuare, rilevare, reperire | trovare |
| disporre di, possedere | avere |
| fornire, erogare | dare |
| acquisire, conseguire, reperire | ottenere |
| richiedere, domandare | chiedere |
| cominciare, dare avvio a, intraprendere | iniziare |
| ultimare, concludere, portare a termine | finire |
| variare, mutare | cambiare |
| incrementare | aumentare |
| decrementare | diminuire |
| consentire di, permettere di, dare la possibilità di | "puoi" più il verbo |
| necessitare di, è necessario | "devi" più il verbo, o l'imperativo |

I comandi SQL e i nomi di API restano come sono, perché sono testo citato: `DROP TABLE`, `INSERT`, `kill -9`.

## Decisioni sulle altre parole

| Hai scritto | Scrivi |
|---|---|
| tuttavia, però, bensì | ma |
| pertanto, dunque, di conseguenza | quindi |
| poiché, in quanto, dato che, siccome | perché |
| qualora, laddove, nel caso in cui | se |
| inoltre, altresì | anche |
| antecedentemente a, precedentemente a | prima di |
| successivamente a, a seguito di | dopo |
| ora, adesso, a questo punto | Cancella: "ora avvia il servizio" → "avvia il servizio" |
| problematica, criticità | problema |
| anomalia, malfunzionamento | errore |
| tipologia | tipo |
| modalità (non tecnica) | modo |
| l'esempio sotto, la sezione sopra | Nomina la destinazione: "l'esempio che segue", "la sezione Installazione" |
| accettabile | Scrivi il limite: "una latenza sotto 200 ms" |

## Controllo Strict

Aggiungi questi due passi al controllo di `SKILL.md`:

1. Cerca nel testo ogni parola della colonna "Hai scritto". Sostituisci ogni occorrenza.
2. Cerca le parole lunghe o rare che restano. Per ognuna, chiediti se esiste una parola comune con lo stesso significato. Se esiste, usala.
