# start.ps1 — starts backend and frontend with one command
# Usage: .\start.ps1

# Check .env exists
if (-not (Test-Path "$PSScriptRoot\.env")) {
    Write-Host "ERROR: .env file not found. Copy .env.example to .env and add your ANTHROPIC_API_KEY." -ForegroundColor Red
    exit 1
}

# Launch backend in a new window
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\run.ps1"

# Brief pause so backend starts before the browser opens
Start-Sleep -Seconds 2

Write-Host "Backend starting at http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend starting at http://localhost:5173" -ForegroundColor Cyan

# Start frontend in this window
Set-Location "$PSScriptRoot\frontend"
npm run dev
