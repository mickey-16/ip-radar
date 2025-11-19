# TICE Project Startup Script
# This script starts both the backend Flask server and the frontend React app

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TICE - Threat Intelligence Engine" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Check if Node.js is available
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found. Please install Node.js 18 or higher." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Backend Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Start backend in a new PowerShell window
$backendScript = {
    Set-Location "d:\TICE hackthaon project"
    Write-Host "Starting Flask backend on http://localhost:5000..." -ForegroundColor Green
    python app.py
}

$backendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {$backendScript}" -PassThru
Write-Host "✓ Backend server starting (PID: $($backendJob.Id))..." -ForegroundColor Green
Write-Host "  Backend URL: http://localhost:5000" -ForegroundColor Cyan

# Wait a moment for backend to start
Write-Host ""
Write-Host "Waiting for backend to initialize (5 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Frontend Dev Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if node_modules exists
$frontendPath = "d:\TICE hackthaon project\frontend\frontendhackathon-master"
if (-not (Test-Path "$frontendPath\node_modules")) {
    Write-Host "Installing frontend dependencies (this may take a few minutes)..." -ForegroundColor Yellow
    Set-Location $frontendPath
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
}

# Start frontend in a new PowerShell window
$frontendScript = {
    Set-Location "d:\TICE hackthaon project\frontend\frontendhackathon-master"
    Write-Host "Starting React frontend on http://localhost:5173..." -ForegroundColor Green
    npm run dev
}

$frontendJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {$frontendScript}" -PassThru
Write-Host "✓ Frontend dev server starting (PID: $($frontendJob.Id))..." -ForegroundColor Green
Write-Host "  Frontend URL: http://localhost:5173" -ForegroundColor Cyan

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Both Servers Are Starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop the servers" -ForegroundColor Yellow
Write-Host ""
Write-Host "Opening frontend in browser in 10 seconds..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Open browser
Start-Process "http://localhost:5173"

Write-Host "✓ Browser opened. Enjoy using TICE!" -ForegroundColor Green
