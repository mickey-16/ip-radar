# Frontend-Backend Integration Guide

## Overview
This guide explains how the React frontend is connected to the Flask backend for the TICE (Threat Intelligence Correlation Engine) application.

## Architecture

### Backend (Flask)
- **Location**: `d:\TICE hackthaon project\`
- **Main File**: `app.py`
- **Port**: 5000
- **API Base URL**: `http://localhost:5000/api`
- **CORS**: Enabled for all origins

### Frontend (React + Vite)
- **Location**: `frontend/frontendhackathon-master/`
- **Framework**: React 18.3.1 + TypeScript
- **Build Tool**: Vite 5.4.19
- **Port**: 8080
- **API Proxy**: Configured to forward `/api` requests to backend

## Key Files

### Backend API Endpoints
All defined in `app.py`:

1. **POST /api/analyze**
   - Analyzes an IP address
   - Request: `{ "ip_address": "8.8.8.8", "use_cache": true }`
   - Response: Full threat profile with scores, categories, intelligence data

2. **GET /api/download-report/<ip_address>**
   - Downloads PDF report for analyzed IP
   - Returns: PDF file as attachment

3. **GET /api/health**
   - Health check endpoint
   - Response: `{ "status": "healthy", "service": "TICE", "version": "1.0.0" }`

### Frontend API Client
**File**: `src/lib/api.ts`

```typescript
// Main API functions
export async function analyzeIP(ipAddress: string, useCache: boolean = true): Promise<ThreatAnalysisResponse>
export async function downloadReport(ipAddress: string): Promise<Blob>
export async function getHealthStatus(): Promise<{ status: string; service: string; version: string }>
export function transformToIntelligenceRecords(apiResults: any): IntelligenceRecord[]
```

### Frontend UI Component
**File**: `src/pages/Index.tsx`

Main page that:
- Takes IP address input
- Calls `analyzeIP()` to get threat intelligence
- Displays threat score, risk level, categories
- Shows consolidated intelligence table from multiple sources
- Allows PDF download via `downloadReport()`

### Vite Proxy Configuration
**File**: `vite.config.ts`

```typescript
server: {
  host: "::",
  port: 8080,
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      secure: false,
    }
  }
}
```

This configuration makes Vite forward all requests to `/api/*` to the Flask backend at `http://localhost:5000/api/*`.

## Data Flow

### IP Analysis Flow
1. User enters IP address in frontend (`Index.tsx`)
2. User clicks "Analyze" button
3. Frontend calls `analyzeIP(ipAddress)` from `api.ts`
4. API client makes POST request to `/api/analyze`
5. Vite proxy forwards to `http://localhost:5000/api/analyze`
6. Flask backend (`app.py`):
   - Validates IP address
   - Calls `ThreatCorrelator.analyze_ip()`
   - Fetches data from multiple threat intelligence APIs
   - Calculates threat score using `ThreatScorer`
   - Returns threat profile JSON
7. Backend response flows back to frontend
8. Frontend:
   - Animates threat score increase
   - Updates threat categories
   - Transforms API results to intelligence records using `transformToIntelligenceRecords()`
   - Displays data in UI table

### PDF Download Flow
1. User clicks "Download PDF" button (only enabled after analysis)
2. Frontend calls `downloadReport(ipAddress)` from `api.ts`
3. API client makes GET request to `/api/download-report/<ip>`
4. Vite proxy forwards to Flask backend
5. Flask backend:
   - Retrieves cached analysis or re-analyzes IP
   - Calls `PDFReportGenerator.generate_report()`
   - Returns PDF bytes as file download
6. Frontend receives PDF blob
7. Creates temporary download link and triggers browser download
8. Saves as `TICE-Report-<ip>.pdf`

## Intelligence Data Transformation

The backend returns raw API results from sources like:
- AbuseIPDB
- VirusTotal
- Shodan
- AlienVault OTX
- IPQualityScore
- ThreatFox

The frontend transforms these into a unified format for display:

```typescript
interface IntelligenceRecord {
  source: string;      // "VirusTotal", "AbuseIPDB", etc.
  category: string;    // "Malicious", "Botnet", "C2 Server", etc.
  evidence: string;    // "Flagged by 45/89 security vendors"
  confidence: string;  // "95%"
  date: string;        // "12/20/2024, 3:45:23 PM"
}
```

The `transformToIntelligenceRecords()` function in `api.ts` handles this transformation.

## Starting the Application

### Option 1: Automated Script (Recommended)
```powershell
.\start-frontend-backend.ps1
```

This script will:
1. Check for virtual environment
2. Install frontend dependencies if needed
3. Start Flask backend on port 5000 (new window)
4. Start Vite dev server on port 8080 (new window)

### Option 2: Manual Start

**Terminal 1 - Backend:**
```powershell
.\venv\Scripts\Activate.ps1
python app.py
```

**Terminal 2 - Frontend:**
```powershell
cd frontend\frontendhackathon-master
npm install  # First time only
npm run dev
```

### Access Points
- Frontend UI: http://localhost:8080
- Backend API: http://localhost:5000/api
- Health Check: http://localhost:5000/api/health

## Testing the Integration

### 1. Health Check
```powershell
# Test backend is running
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "TICE",
  "version": "1.0.0"
}
```

### 2. Analyze IP via Frontend
1. Open http://localhost:8080
2. Enter IP: `8.8.8.8` (Google DNS - should show LOW risk)
3. Click "Analyze"
4. Verify:
   - Threat score appears (0-5 for whitelisted IPs)
   - Risk level shows "Benign" (green)
   - Intelligence table shows data from multiple sources
   - API status indicators show green checkmarks

### 3. Test APT IP
1. Enter IP: `45.142.212.61` (Known APT IP)
2. Click "Analyze"
3. Verify:
   - Threat score ~100 (CRITICAL)
   - Risk level shows "Malicious" (red)
   - Categories include C2 Server or Botnet
   - AlienVault OTX shows APT groups (e.g., MuddyWater)
   - High confidence level (>85%)

### 4. Download PDF
1. After analyzing an IP, click "Download PDF"
2. Verify:
   - PDF downloads automatically
   - Filename: `TICE-Report-<ip>.pdf`
   - PDF contains threat intelligence, MITRE section (for APT IPs), scores

## API Response Structure

### Analyze IP Response
```json
{
  "ip_address": "45.142.212.61",
  "threat_score": 100,
  "risk_level": "CRITICAL",
  "confidence": "HIGH",
  "is_malicious": true,
  "geolocation": {
    "country": "Iran",
    "city": "Tehran",
    "latitude": 35.6892,
    "longitude": 51.3890
  },
  "network_info": {
    "isp": "Example ISP",
    "organization": "Example Org",
    "asn": "AS12345"
  },
  "threat_categories": ["Botnet", "C2 Server"],
  "threat_actors": ["MuddyWater", "APT34"],
  "malware_families": ["PowerStats"],
  "is_c2_server": true,
  "is_botnet": false,
  "api_results": {
    "abuseipdb": { /* raw response */ },
    "virustotal": { /* raw response */ },
    "otx": { /* raw response */ },
    "shodan": { /* raw response */ },
    "ipqualityscore": { /* raw response */ }
  },
  "mitre_intelligence": {
    "techniques": [/* ATT&CK techniques */],
    "tactics": [/* ATT&CK tactics */],
    "threat_groups": [/* APT groups */]
  },
  "ml_prediction": {
    "available": true,
    "predicted_threat_score": 98,
    "is_malicious": true,
    "confidence": 0.95
  }
}
```

## Troubleshooting

### CORS Errors
If you see CORS errors in browser console:
- Verify Flask backend has `CORS(app)` enabled (already configured)
- Check backend is running on port 5000
- Verify Vite proxy configuration in `vite.config.ts`

### API Calls Failing
1. Check backend is running:
   ```powershell
   curl http://localhost:5000/api/health
   ```

2. Check browser console for errors

3. Verify Vite proxy is forwarding:
   - Open browser DevTools → Network tab
   - Analyze an IP
   - Check request URL shows `/api/analyze`
   - Check "Initiator" shows proxy

### Frontend Not Updating
1. Clear browser cache
2. Hard refresh: Ctrl+Shift+R
3. Check React DevTools for state updates

### PDF Download Not Working
1. Verify IP has been analyzed first
2. Check backend logs for PDF generation errors
3. Ensure reportlab is installed: `pip install reportlab`

## Environment Variables

Backend requires `.env` file with API keys:
```env
ABUSEIPDB_API_KEY=your_key_here
VIRUSTOTAL_API_KEY=your_key_here
ALIENVAULT_OTX_API_KEY=your_key_here
IPQUALITYSCORE_API_KEY=your_key_here
SHODAN_API_KEY=your_key_here
```

Frontend doesn't require any environment variables (API keys are server-side only).

## Development Tips

### Hot Reload
Both servers support hot reload:
- **Frontend**: Vite auto-reloads on file changes in `src/`
- **Backend**: Flask debug mode auto-reloads on `.py` file changes

### Debugging Frontend API Calls
Add console logs in `api.ts`:
```typescript
export async function analyzeIP(ipAddress: string, useCache: boolean = true) {
  console.log('Analyzing IP:', ipAddress);
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ip_address: ipAddress, use_cache: useCache }),
  });
  console.log('Response:', response);
  const data = await response.json();
  console.log('Data:', data);
  return data;
}
```

### Debugging Backend API
Backend logs to console automatically. Check the terminal running `python app.py` for:
- Request logs
- Error messages
- API call status

## Production Deployment

For production deployment:

1. **Build Frontend**:
   ```powershell
   cd frontend\frontendhackathon-master
   npm run build
   ```
   This creates optimized static files in `dist/`

2. **Serve Frontend from Flask**:
   Configure Flask to serve the built frontend from `dist/`

3. **Use Production Server**:
   Replace Flask development server with Gunicorn or similar

4. **Environment Variables**:
   Use environment-specific `.env` files

5. **CORS Configuration**:
   Lock down CORS to specific frontend domain instead of allowing all origins

## Summary

The integration is complete and working:
- ✅ Vite proxy forwards `/api` requests to Flask backend
- ✅ Frontend makes real API calls instead of using mock data
- ✅ Intelligence data is transformed and displayed in UI table
- ✅ PDF download functionality integrated
- ✅ CORS enabled for cross-origin requests
- ✅ Automated startup script provided

You can now test the full application by running `.\start-frontend-backend.ps1` and accessing http://localhost:8080!
