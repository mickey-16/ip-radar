# TICE Run Script
# Quick script to run the application

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Starting TICE Server" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment if not already activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠ WARNING: .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file with your API keys" -ForegroundColor Yellow
    Write-Host "See SETUP.md for instructions" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit
    }
}

# Run the application
Write-Host "Starting Flask application..." -ForegroundColor Green
Write-Host ""
python app.py
