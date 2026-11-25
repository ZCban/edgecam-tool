# EDGECAM Tool

Utilità Windows per importare gli utensili di tornitura, fresatura e foratura da librerie JSON nel database EDGECAM. La GUI V41 è distribuita a partire dalla release `v1.0.0`. Le versioni precedenti della GUI sono conservate nel repository.

## Avvio

Estrai l'intero archivio portatile in una cartella scrivibile e avvia `EDGECAM-Tool.exe`. Copia `LIBRERIA_UTENSILI` e `GRAFICHE` dalla tua installazione accanto all'eseguibile. Puoi copiare anche `EDGECAM_OPTIONS.json` e `BACKUP_DATABASE` per riutilizzare impostazioni e backup esistenti. L'archivio contiene il programma e le sue dipendenze Python. Per collegarsi al database serve SQL Server Native Client 11.0 e l'accesso all'istanza EDGECAM tramite autenticazione Windows.

## Sviluppo

Da PowerShell con Python 3.14 su Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe edgecam_gui_v41.py
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm --windowed --name EDGECAM-Tool edgecam_gui_v41.py
```

La compilazione genera la cartella portatile `dist/EDGECAM-Tool`. GitHub Actions la genera, la verifica e la pubblica in formato ZIP quando viene caricato un tag di versione.

## Esportazione utensili

Nella finestra principale, apri **Esporta utensili**, scegli il **Database sorgente** e spunta le famiglie da esportare. Premi **Avvia esportazione** e conferma. Il programma legge gli utensili e i montaggi dal database e salva i JSON in `LIBRERIA_UTENSILI`, la stessa cartella usata dall'importazione. I duplicati per nome vengono saltati. Avanzamento, esito e nuovi utensili vengono mostrati nella finestra principale.

Se hai già esportato utensili con la versione separata, i relativi JSON si trovano in `esportatori/LIBRERIA_UTENSILI`. Puoi copiarli nelle corrispondenti sottocartelle di `LIBRERIA_UTENSILI` evitando di sovrascrivere file esistenti.
