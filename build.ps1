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


