# Prima e dopo

Ogni coppia mostra un testo tipico di un modello linguistico e lo stesso testo con le regole di Italiano Chiaro. Il testo "prima" viola le regole di proposito, quindi questo file non passa il linter. Nei testi "dopo", i nomi e i numeri vengono dalla fonte che l'autore ha davanti: il ticket, il log, la modifica.

## 1. Messaggio di errore della riga di comando

Prima:

```text
Errore: non è stato possibile procedere al caricamento del file di configurazione. Si consiglia di verificare che il percorso sia corretto ed eventualmente riprovare.
```

Dopo:

```text
Errore: impossibile leggere config.yaml. Il file non esiste in /etc/sqlpipe/.
Crea il file o indica un altro percorso con --config.
```

Che cosa cambia: il messaggio nomina il file e la causa. Il secondo rigo dice che cosa fare. Spariscono la nominalizzazione, il "si" impersonale e "eventualmente".

## 2. Runbook

Prima:

> **Riavvio del servizio.** Qualora il servizio dovesse risultare non raggiungibile, sarebbe opportuno andare a effettuare un riavvio dello stesso, avendo cura di verificare preventivamente che non vi siano job in esecuzione — in caso contrario si rischia di perdere i dati.

Dopo:

> ## Riavvio del servizio
>
> Se il servizio `sync` non risponde, riavvialo sull'host `app-01`.
>
> 1. Esegui `sync status` e verifica che nessun job sia in esecuzione. Se un job è in esecuzione, aspetta che finisca. Un riavvio durante un job perde i dati del job.
> 2. Esegui `sudo systemctl restart sync`.
> 3. Esegui `sync status` e verifica che lo stato sia `running`.

Che cosa cambia: la condizione viene prima del comando. Il condizionale e "andare a effettuare" diventano un imperativo. L'avvertenza dice prima che cosa fare, poi il rischio. Il testo nomina il servizio e l'host.

## 3. Note di rilascio

Prima:

> 🚀 La versione 2.4 introduce un potente e robusto sistema di cache che rende l'esperienza più fluida, veloce e affidabile, permettendo agli utenti di lavorare in modo semplicemente più efficiente!

Dopo:

> ## 2.4
>
> - Nuova cache delle query. Una query ripetuta entro 60 secondi legge il risultato dalla cache.
> - Il tempo medio di risposta della pagina Report scende da 1,8 a 0,4 secondi nei nostri test.
> - Per spegnere la cache, imposta `cache.enabled: false`.

Che cosa cambia: ogni voce dice un fatto che il lettore può verificare. Spariscono l'emoji, la terna di aggettivi, il gerundio dopo la virgola e le parole vuote. Se la fonte non dà i numeri, la voce resta generale.

## 4. Mail tecnica

Prima:

> Gentile team, con la presente si comunica che in data odierna è stata effettuata la migrazione del database di produzione. Si fa presente che, a seguito di tale intervento, potrebbero verificarsi dei rallentamenti. Restiamo a disposizione per qualsiasi chiarimento.

Dopo:

> Oggi alle 14:00 abbiamo migrato il database di produzione a Postgres 16. Fino a domani le query sulla tabella `ordini` possono essere più lente, perché il database ricostruisce gli indici. Se una query supera 30 secondi, scrivi a Marco.

Che cosa cambia: il testo dice chi ha fatto che cosa e quando. "Potrebbero verificarsi" diventa un fatto con la causa e la durata. La chiusura di cortesia diventa un'istruzione con un nome.

## 5. Risposta in chat

Domanda: "Perché la build non parte?"

Prima:

> Ottima domanda! Ci sono diversi motivi per cui la build potrebbe non partire:
>
> - **Dipendenze**: potrebbero mancare alcune dipendenze.
> - **Configurazione**: la configurazione potrebbe essere errata.
> - **Spazio su disco**: il disco potrebbe essere pieno.
>
> Spero di esserti stato utile! Fammi sapere se hai altre domande.

Dopo:

> La build non parte perché il disco dell'agente CI è pieno: il log dice `No space left on device` al passo `npm ci`. Libera spazio con `docker system prune` sull'agente e rilancia la build.

Che cosa cambia: la prima frase dà la risposta. La risposta usa il log e non elenca cause possibili. Spariscono l'apertura, la chiusura, il grassetto e l'elenco.
