# Run the FastAPI backend
# Usage: .\run.ps1
# Requires ANTHROPIC_API_KEY to be set (or add it to .env and load it here)

$env:PYTHONPATH = "$PSScriptRoot;$PSScriptRoot\backend\lib"

# Load .env if it exists
if (Test-Path "$PSScriptRoot\.env") {
    Get-Content "$PSScriptRoot\.env" | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]*)\s*=\s*(.*)\s*$") {
            [System.Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), "Process")
        }
    }
}

python -m uvicorn backend.src.api.main:app --reload --host 0.0.0.0 --port 8000
