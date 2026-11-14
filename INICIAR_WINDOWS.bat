@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Primeiro siga a instalacao no README.md.
 pause
 exit /b 1
)
echo Abra http://localhost:8000 no navegador. Ctrl+C encerra.
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
