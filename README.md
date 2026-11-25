# EDGECAM Tool

A Windows utility for importing and exporting turning, milling, and holemaking tools between JSON libraries and EDGECAM databases. `edgecam_gui_v41.py` is the entry point for both operations.

## Getting started

Extract the entire portable archive to a writable folder and run `EDGECAM-Tool.exe`. Copy `LIBRERIA_UTENSILI` and `GRAFICHE` from your existing installation into the same folder as the executable. You can also copy `EDGECAM_OPTIONS.json` and `BACKUP_DATABASE` to reuse your settings and backups. The archive includes the application and its Python dependencies. Database access requires SQL Server Native Client 11.0 and permission to connect to the EDGECAM instance using Windows Authentication.

## Development

Run the following commands in PowerShell with Python 3.14 on Windows.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe edgecam_gui_v41.py
.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm --windowed --name EDGECAM-Tool edgecam_gui_v41.py
```

The build creates the portable application in `dist/EDGECAM-Tool`. When a version tag is pushed, GitHub Actions builds and verifies the package and publishes it as a ZIP archive.

## Exporting tools

In the main window, open **Export tools**, select the **Source database**, and tick the tool families you want to export. Click **Start export** and confirm. The application reads tools and their mounting records from the database and saves the JSON files to `LIBRERIA_UTENSILI`, the same folder used for imports. It skips tools whose names already exist in the library. The main window shows progress, the result, and the newly exported tools.

If you previously exported tools with the standalone exporter, you can find the JSON files in `esportatori/LIBRERIA_UTENSILI`. Copy them to the corresponding subfolders in `LIBRERIA_UTENSILI`, skipping any files that already exist.
