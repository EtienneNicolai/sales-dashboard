@echo off
cd /d "%~dp0"

if not exist .env (
    echo ERROR: .env not found.
    echo Copy .env.example to .env and add your GEMINI_API_KEY.
    pause
    exit /b 1
)

echo Starting Sales Dashboard...
echo Backend  ^>  http://localhost:8000
echo Frontend ^>  http://localhost:5173
echo.

start "Sales Dashboard - Backend" powershell -NoExit -ExecutionPolicy Bypass -File "%~dp0run.ps1"
timeout /t 2 /nobreak >nul
start "Sales Dashboard - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
