# Versione v1.1.2

## 📅 Data di pubblicazione

27 novembre 2026

## 🚀 Miglioramenti

- L'indice locale conserva i dati usati dalla tabella e rilegge solo i JSON nuovi o modificati. L'indice si aggiorna anche quando un utensile viene eliminato.
- La ricerca, i filtri e la selezione degli utensili restano disponibili durante il rilevamento dei database.

## 📦 Download

- `EDGECAM-Tool-v1.1.2-windows-x64.zip` contiene la GUI V41 portatile.

# Versione v1.1.1

## 📅 Data di pubblicazione

25 novembre 2026

## ⚙️ Modifiche tecniche

- Rimossi i tre script di analisi di esempio e le versioni della GUI dalla V30 alla V40. La V41 resta l'unica GUI nel progetto e comprende importazione ed esportazione.

## 📦 Download

- `EDGECAM-Tool-v1.1.1-windows-x64.zip` contiene la GUI V41 portatile.

# Versione v1.1.0

## 📅 Data di pubblicazione

25 novembre 2026

## ✨ Nuove funzionalità

- Esportazione V2 integrata nella finestra principale. Il pannello **Esporta utensili** consente di scegliere un ToolStore sorgente e le famiglie di tornitura, fresatura e foratura.
- I JSON esportati sono disponibili nella stessa libreria usata dall'importazione. La tabella viene aggiornata al termine dell'operazione.

## ⚙️ Modifiche tecniche

- Il codice V2 continua a gestire il formato JSON, i montaggi e il controllo dei duplicati. L'esportazione usa connessioni SQL in sola lettura operativa, con query di selezione.

## 📦 Download

- `EDGECAM-Tool-v1.1.0-windows-x64.zip` contiene la GUI portatile con importazione ed esportazione.

# Versione v1.0.1

## 📅 Data di pubblicazione

25 novembre 2026

## ⚙️ Modifiche tecniche

- `esportatori/edgecam_esporta_utensili_v2.py` è l'unico esportatore incluso nei sorgenti della versione corrente.
- Rimossi i quattro script di esportazione obsoleti dalla cartella di lavoro e dal ramo `main`. Le copie precedenti restano nella cronologia Git.

## 📦 Download

- `EDGECAM-Tool-v1.0.1-windows-x64.zip` contiene la GUI di importazione portatile. L'esportatore V2 è disponibile nell'archivio dei sorgenti della release.

# Versione v1.0.0

## 📅 Data di pubblicazione

25 novembre 2026

## ✨ Funzionalità incluse

- Importazione di utensili di tornitura, fresatura e foratura con selezione multipla, controllo dei duplicati e gestione dei backup.
- Associazione di grafiche STL e MEG agli utensili, sei lingue e temi Originale e Nero.

## 🐛 Bug corretti nella GUI V41 e nelle revisioni precedenti

- La ricerca per nome trova gli utensili anche digitando il nome senza spazi o trattini.

## 🎨 Modifiche grafiche

- La tabella mostra Categoria, Utensile e Graphic. La colonna Utensile è larga 300 pixel.
- Il selettore Destination Database e i pulsanti Aggiorna database e Ripristina backup occupano una sola riga.

## ⚙️ Modifiche tecniche

- Prima versione distribuita con Semantic Versioning e con compilazione Windows automatica al caricamento del tag.
- La versione portatile cerca librerie, grafiche, impostazioni e backup accanto all'eseguibile.

## 📦 Download

- `EDGECAM-Tool-v1.0.0-windows-x64.zip` contiene l'eseguibile portatile e i file necessari per avviarlo.

## 📥 Installazione e aggiornamento

Estrai l'archivio in una cartella scrivibile, copia le tue librerie e grafiche accanto all'eseguibile e avvia `EDGECAM-Tool.exe`. Il collegamento a EDGECAM richiede SQL Server Native Client 11.0 e i permessi Windows sul database.
