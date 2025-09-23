# Active venv
if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
  python -m venv .venv
}
.\.venv\Scripts\Activate.ps1

# Guarantees PyInstaller
pip install -q pyinstaller

# Build do .exe
pyinstaller --noconfirm --onefile --windowed `
  --icon=pdf_reducer_whitebg.ico `
  --name "PDF-Reducer" `
  src/main.py

Write-Host "`nBuild completed! See: dist/PDF-Reducer.exe" -ForegroundColor Green


$ErrorActionPreference = 'Stop'
if (!(Test-Path ".\.venv\Scripts\python.exe")) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -q pyinstaller

$MAIN = ".\src\main.py"
$ICON = ".\pdf_reducer_whitebg.ico"

python -m PyInstaller --clean --noconfirm --onefile --windowed --name "PDF-Reducer" --icon $ICON $MAIN

if (!(Test-Path ".\dist\PDF-Reducer.exe")) { throw "Build ok, mas dist\PDF-Reducer.exe não encontrado." }
Write-Host "`nOK! dist\PDF-Reducer.exe pronto." -ForegroundColor Green
