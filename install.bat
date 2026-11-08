@echo off
cd /d "%~dp0"
py -3 -m venv .venv
if errorlevel 1 (
  echo Could not create virtual environment. Install a supported Python version first.
  pause
  exit /b 1
)
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo Installation finished. Edit .env and add your OpenAI API key.
pause
