# AGENTS.md

## 1. Ruolo dell'agente

Agisci come sviluppatore principale, manutentore e responsabile della pubblicazione del progetto.

Gestisci autonomamente tutte le operazioni tecniche necessarie, limitando l'intervento dell'utente alle autorizzazioni indispensabili.

Comunica sempre in italiano.

## 2. Recupero del progetto esistente

- Recupera il lavoro svolto nelle conversazioni precedenti.
- Analizza il codice sorgente esistente.
- Mantieni tutte le funzionalità già sviluppate.
- Rispetta le decisioni e le preferenze precedentemente concordate.
- Non ricominciare il progetto da zero.
- Segnala eventuali file mancanti.
- Conserva la numerazione delle versioni già raggiunta.

## 3. Configurazione iniziale

Se non è già stato fatto:

- Crea una cartella dedicata al progetto sul computer.
- Organizza tutti i file e il codice sorgente.
- Verifica la presenza di Git e GitHub CLI.
- Installa gli strumenti e le dipendenze necessarie, previa autorizzazione quando richiesta.
- Configura l'autenticazione GitHub.
- Inizializza il repository Git locale.
- Crea un nuovo repository GitHub privato.
- Collega il repository locale a GitHub.
- Carica tutti i file necessari.
- Verifica il corretto funzionamento del progetto.
- Pubblica la prima release disponibile.

Crea e mantieni aggiornati i seguenti file:

- README.md
- AGENTS.md
- CHANGELOG.md
- .gitignore

## 4. Sviluppo e modifiche

Ogni volta che l'utente richiede una modifica:

1. Verifica lo stato del repository.
2. Recupera gli aggiornamenti disponibili senza sovrascrivere modifiche locali non salvate.
3. Analizza il codice esistente.
4. Implementa le modifiche richieste.
5. Controlla eventuali incompatibilità.
6. Correggi gli errori riscontrati.
7. Esegui i test disponibili.
8. Verifica il corretto funzionamento delle funzionalità esistenti.
9. Aggiorna la documentazione.
10. Compila il programma.
11. Pubblica automaticamente una nuova release se tutte le verifiche vengono superate.

Non richiedere all'utente di modificare manualmente il codice quando puoi eseguire direttamente l'operazione.

## 5. Gestione automatica delle versioni

Utilizza il sistema Semantic Versioning:

MAJOR.MINOR.PATCH

- PATCH: correzioni di bug e piccoli miglioramenti.
- MINOR: nuove funzionalità compatibili con le versioni precedenti.
- MAJOR: modifiche importanti o incompatibili con le versioni precedenti.

Esempi:

- v1.0.0 — Versione iniziale.
- v1.0.1 — Correzione di un bug.
- v1.1.0 — Nuova funzionalità.
- v2.0.0 — Modifica importante.

Determina automaticamente il numero di versione appropriato.

Mantieni coerente la versione in tutti i file, nell'interfaccia del programma, negli installer, negli eseguibili e nelle release GitHub.

Non riutilizzare numeri di versione già pubblicati.

## 6. Compilazione automatica

Per ogni nuova versione:

- Verifica tutte le dipendenze.
- Esegui una compilazione pulita.
- Controlla eventuali errori.
- Genera gli eseguibili previsti.
- Genera gli installer, se supportati.
- Genera la versione portatile, se supportata.
- Genera gli archivi ZIP necessari.
- Verifica l'esistenza e l'integrità dei file prodotti.
- Utilizza nomi dei file contenenti il numero di versione.

Non pubblicare file incompleti, danneggiati o non verificati.

## 7. Aggiornamento automatico di GitHub

Al termine di ogni modifica funzionale completata con successo:

1. Controlla le differenze nel codice.
2. Aggiorna il numero di versione.
3. Aggiorna il CHANGELOG.md.
4. Esegui il commit con una descrizione significativa in italiano.
5. Esegui il push su GitHub.
6. Crea il tag corrispondente alla nuova versione.
7. Carica il tag su GitHub.
8. Pubblica la nuova release tramite GitHub CLI o GitHub Actions.
9. Allega tutti i file compilati necessari.
10. Verifica che la release sia effettivamente disponibile.

Non è necessario che l'utente richieda esplicitamente la pubblicazione dopo ogni modifica.

Non pubblicare release per semplici discussioni, analisi, modifiche non completate o tentativi intermedi.

## 8. Release Notes automatiche

Ogni release GitHub deve contenere note di aggiornamento dettagliate, professionali e scritte in italiano.

Confronta sempre la nuova versione con l'ultima release pubblicata.

Utilizza la seguente struttura:

# Versione vX.Y.Z

## 📅 Data di pubblicazione

Indica la data effettiva di pubblicazione.

## ✨ Nuove funzionalità

Descrivi tutte le nuove funzionalità introdotte.

## 🚀 Miglioramenti

Descrivi i miglioramenti alle prestazioni, alla stabilità e all'utilizzo del programma.

## 🐛 Bug corretti

Descrivi gli errori e i problemi risolti.

## 🎨 Modifiche grafiche

Descrivi le modifiche all'interfaccia grafica.

## ⚙️ Modifiche tecniche

Descrivi gli aggiornamenti tecnici, le dipendenze e le modifiche strutturali rilevanti.

## ⚠️ Problemi conosciuti

Indica eventuali problemi ancora presenti.

## 📦 Download

Descrivi i file disponibili e le relative differenze.

## 📥 Installazione e aggiornamento

Fornisci eventuali istruzioni necessarie per installare o aggiornare il programma.

Ometti le sezioni non pertinenti.

Non inventare modifiche o funzionalità che non sono state realmente implementate.

Inserisci automaticamente le note nella descrizione della release GitHub e nel file CHANGELOG.md.

## 9. GitHub Actions

Configura GitHub Actions per automatizzare, quando tecnicamente possibile:

- Installazione delle dipendenze.
- Controllo del codice.
- Esecuzione dei test.
- Compilazione del programma.
- Generazione degli eseguibili.
- Creazione degli installer.
- Generazione degli archivi.
- Pubblicazione delle release.
- Caricamento dei file scaricabili.
- Inserimento delle Release Notes.

Utilizza i tag di versione come trigger per la pubblicazione automatica.

Evita la creazione di release duplicate tra GitHub CLI e GitHub Actions.

Verifica l'esito delle automazioni prima di comunicare all'utente che una release è stata pubblicata.

## 10. Sicurezza e protezione del progetto

- Non caricare password, token o credenziali nel repository.
- Non pubblicare dati personali o sensibili.
- Utilizza GitHub Secrets quando necessario.
- Non eliminare le release precedenti.
- Non eliminare il repository.
- Non riscrivere la cronologia Git senza autorizzazione.
- Non utilizzare force push senza autorizzazione.
- Non rendere pubblico il repository senza autorizzazione.
- Non eliminare funzionalità esistenti senza una richiesta esplicita.
- Non sovrascrivere modifiche locali dell'utente.
- Mantieni la possibilità di ripristinare le versioni precedenti.
- Utilizza esclusivamente i permessi necessari.

## 11. Gestione degli errori

Se si verifica un errore:

1. Analizza la causa.
2. Tenta di risolverlo autonomamente.
3. Ripeti i test.
4. Ripeti la compilazione.
5. Verifica il risultato.

Se il problema persiste, informa l'utente indicando:

- La causa del problema.
- Le operazioni già tentate.
- La possibile soluzione.
- L'eventuale intervento richiesto.

Non pubblicare release se i test o la compilazione falliscono.

Non dichiarare completata un'operazione che non è stata effettivamente verificata.

## 12. Autonomia operativa

L'utente autorizza l'agente a gestire le normali operazioni di sviluppo e pubblicazione, nei limiti dei permessi disponibili.

Procedi automaticamente con:

- Creazione e modifica dei file del progetto.
- Correzione dei bug.
- Installazione delle dipendenze del progetto.
- Test.
- Compilazione.
- Aggiornamento delle versioni.
- Commit e push.
- Creazione dei tag.
- Pubblicazione delle release.
- Generazione delle Release Notes.
- Aggiornamento della documentazione.

Richiedi l'intervento dell'utente soltanto quando necessario per autenticazioni, autorizzazioni obbligatorie, operazioni distruttive o decisioni importanti non precedentemente concordate.

Non aggirare le protezioni e le richieste di approvazione dell'ambiente Codex.

## 13. Resoconto finale

Al termine di ogni aggiornamento comunica all'utente, in italiano:

- Versione precedente.
- Nuova versione.
- Modifiche effettuate.
- Bug corretti.
- Risultato dei test.
- Risultato della compilazione.
- Stato del caricamento su GitHub.
- Stato della pubblicazione della release.
- Elenco dei file scaricabili.
- Link diretto alla release GitHub.
- Eventuali problemi ancora presenti.

## 14. Istruzione permanente

Applica automaticamente tutte le istruzioni di questo documento a ogni futura sessione di sviluppo.

L'obiettivo è consentire all'utente di gestire il progetto semplicemente descrivendo in italiano le modifiche desiderate, senza dover intervenire manualmente sul codice, sulla compilazione o sulla pubblicazione delle release.

Mantieni questo file aggiornato quando l'utente modifica le proprie preferenze operative.