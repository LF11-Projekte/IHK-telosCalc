# Erstellungsprozess

Im CMD.EXE:
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

In PowerShell.exe
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Für alle:
```cmd
pip install -r requirements.txt
pip install pyinstaller     # Um eine .exe / .bin / &c. zu builden
pyinstall main.spec
```

Die .EXE befindet sich dann im ./dist Ordner.
