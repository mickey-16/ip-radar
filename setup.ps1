# TICE Quick Start Script
# Run this to set up the project

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  TICE Setup Assistant" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "[4/5] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Check for .env file
Write-Host ""
Write-Host "[5/5] Checking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "⚠ .env file not found!" -ForegroundColor Red
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✓ .env created - PLEASE ADD YOUR API KEYS!" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file and add your API keys" -ForegroundColor White
Write-Host "2. Run: python app.py" -ForegroundColor White
Write-Host "3. Open: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "Get API Keys:" -ForegroundColor Yellow
Write-Host "• AbuseIPDB: https://www.abuseipdb.com/api" -ForegroundColor White
Write-Host "• VirusTotal: https://www.virustotal.com/gui/join-us" -ForegroundColor White
Write-Host "• IPGeolocation: https://ipgeolocation.io/signup" -ForegroundColor White
Write-Host ""
