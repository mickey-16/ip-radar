# Start both Frontend and Backend servers for TICE

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TICE - Starting Frontend & Backend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python virtual environment exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "[✓] Found virtual environment" -ForegroundColor Green
} else {
    Write-Host "[!] Virtual environment not found. Please run setup.ps1 first" -ForegroundColor Red
    exit 1
}

# Check if frontend dependencies are installed
if (Test-Path "frontend\frontendhackathon-master\node_modules") {
    Write-Host "[✓] Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[!] Installing frontend dependencies..." -ForegroundColor Yellow
    Push-Location "frontend\frontendhackathon-master"
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[✗] Failed to install frontend dependencies" -ForegroundColor Red
        Pop-Location
        exit 1
    }
    Pop-Location
    Write-Host "[✓] Frontend dependencies installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting servers..." -ForegroundColor Cyan
Write-Host ""

# Start Backend in a new window
Write-Host "[Backend] Starting Flask server on http://localhost:5000" -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; python app.py" -WindowStyle Normal

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start Frontend in a new window
Write-Host "[Frontend] Starting Vite dev server on http://localhost:8080" -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend\frontendhackathon-master'; npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Servers Started Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop the servers" -ForegroundColor Yellow
Write-Host ""
