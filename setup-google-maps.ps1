# Quick Google Maps API Key Setup

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Google Maps API Key Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 Steps to get your Google Maps API Key:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Go to Google Cloud Console:" -ForegroundColor White
Write-Host "   https://console.cloud.google.com/" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Create a new project or select existing one" -ForegroundColor White
Write-Host ""
Write-Host "3. Enable Maps JavaScript API:" -ForegroundColor White
Write-Host "   - Go to 'APIs & Services' > 'Library'" -ForegroundColor Gray
Write-Host "   - Search for 'Maps JavaScript API'" -ForegroundColor Gray
Write-Host "   - Click 'Enable'" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Create API Key:" -ForegroundColor White
Write-Host "   - Go to 'APIs & Services' > 'Credentials'" -ForegroundColor Gray
Write-Host "   - Click 'Create Credentials' > 'API Key'" -ForegroundColor Gray
Write-Host "   - Copy your API key" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Restrict your API key (Important for security):" -ForegroundColor White
Write-Host "   - Application restrictions: HTTP referrers" -ForegroundColor Gray
Write-Host "   - Add: http://localhost:8080/*" -ForegroundColor Gray
Write-Host "   - API restrictions: Maps JavaScript API only" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Prompt for API key
Write-Host "Enter your Google Maps API key (or press Enter to skip):" -ForegroundColor Yellow
$apiKey = Read-Host

if ($apiKey) {
    $envPath = "frontend\frontendhackathon-master\.env"
    
    # Check if .env exists
    if (Test-Path $envPath) {
        Write-Host ""
        Write-Host "✓ Found .env file" -ForegroundColor Green
        
        # Update or create the API key entry
        $content = Get-Content $envPath -Raw
        if ($content -match "VITE_GOOGLE_MAPS_API_KEY=") {
            $content = $content -replace "VITE_GOOGLE_MAPS_API_KEY=.*", "VITE_GOOGLE_MAPS_API_KEY=$apiKey"
            Set-Content $envPath -Value $content -NoNewline
            Write-Host "✓ Updated VITE_GOOGLE_MAPS_API_KEY in .env" -ForegroundColor Green
        } else {
            Add-Content $envPath "`nVITE_GOOGLE_MAPS_API_KEY=$apiKey"
            Write-Host "✓ Added VITE_GOOGLE_MAPS_API_KEY to .env" -ForegroundColor Green
        }
    } else {
        Write-Host ""
        Write-Host "✗ .env file not found at $envPath" -ForegroundColor Red
        Write-Host "Creating .env file..." -ForegroundColor Yellow
        
        $envContent = @"
# Google Maps API Key
# Get your key from: https://console.cloud.google.com/google/maps-apis
VITE_GOOGLE_MAPS_API_KEY=$apiKey
"@
        Set-Content $envPath -Value $envContent
        Write-Host "✓ Created .env file with API key" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Restart your frontend dev server" -ForegroundColor White
    Write-Host "   cd frontend\frontendhackathon-master" -ForegroundColor Gray
    Write-Host "   npm run dev" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Refresh your browser (Ctrl+Shift+R)" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Analyze an IP to see Google Maps!" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Skipped. You can manually add your API key to:" -ForegroundColor Yellow
    Write-Host "  frontend\frontendhackathon-master\.env" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Format:" -ForegroundColor White
    Write-Host "  VITE_GOOGLE_MAPS_API_KEY=your_actual_api_key_here" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "📚 For detailed instructions, see: GOOGLE_MAPS_SETUP.md" -ForegroundColor Cyan
Write-Host ""
