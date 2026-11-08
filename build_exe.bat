@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  echo Please run install.bat first.
  pause
  exit /b 1
)
call .venv\Scripts\activate
pyinstaller --noconfirm --clean --windowed --name FOMO_Translator_V2 --paths . --collect-all PySide6 desktop_app\app.py
echo.
echo Build output: dist\FOMO_Translator_V2\
echo Copy your .env file beside the executable before running.
pause
