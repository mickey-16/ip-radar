# 🧪 TICE Testing Guide

## ✅ Core Tests PASSED!

Your application is working correctly! Here's how to test it:

---

## 🚀 Method 1: Run the Web App (RECOMMENDED)

### Start the Server:
```powershell
python app.py
```

You should see:
```
==================================================
🛡️  TICE - Threat Intelligence Correlation Engine
==================================================
Environment: development
Debug Mode: True
Server: http://0.0.0.0:5000
==================================================
 * Running on http://127.0.0.1:5000
```

### Then Test in Browser:
1. Open: **http://localhost:5000**
2. You'll see a beautiful dashboard
3. Enter test IPs:
   - `8.8.8.8` - Google DNS (should be LOW risk)
   - `1.1.1.1` - Cloudflare DNS (should be LOW risk)
   - `185.220.101.1` - Known malicious (should be HIGH risk)

---

## 🧪 Method 2: Test API Endpoints

### Test the Health Check:
```powershell
# Using Invoke-RestMethod (PowerShell)
Invoke-RestMethod -Uri "http://localhost:5000/api/health"
```

Expected response:
```json
{
  "status": "healthy",
  "service": "TICE",
  "version": "1.0.0"
}
```

### Test IP Analysis:
```powershell
# Analyze an IP
$body = @{
    ip_address = "8.8.8.8"
    use_cache = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/analyze" `
                  -Method POST `
                  -ContentType "application/json" `
                  -Body $body
```

---

## 📝 Method 3: Test Without API Keys (Demo Mode)

**Good news:** The app will run even without API keys!

Without API keys, you'll get:
- ✅ Beautiful UI works
- ✅ IP validation works
- ✅ Scoring algorithm works
- ⚠️ But no real threat data (APIs return null)

The app will show a score based on limited data, perfect for testing the interface!

---

## 🔑 Method 4: Test WITH API Keys (Full Functionality)

### Get FREE API Keys (15 minutes):

1. **AbuseIPDB** (1,000/day free)
   - Visit: https://www.abuseipdb.com/api
   - Sign up → Go to API → Copy key

2. **VirusTotal** (500/day free)
   - Visit: https://www.virustotal.com/gui/join-us
   - Sign up → Profile → API Key → Copy

3. **IPGeolocation** (1,000/day free)
   - Visit: https://ipgeolocation.io/signup
   - Sign up → Dashboard → Copy API key

### Add to .env file:
```powershell
notepad .env
```

Replace placeholders:
```env
ABUSEIPDB_API_KEY=your_actual_key_here
VIRUSTOTAL_API_KEY=your_actual_key_here
IPGEOLOCATION_API_KEY=your_actual_key_here
```

Save and restart the app!

---

## 🎯 Test IP Addresses

### Safe/Clean IPs (Low Risk Scores):
```
8.8.8.8           - Google Public DNS
1.1.1.1           - Cloudflare DNS
208.67.222.222    - OpenDNS
9.9.9.9           - Quad9 DNS
```

### Suspicious IPs (Medium-High Risk):
```
185.220.101.1     - Tor exit node
45.142.212.61     - Known bad actor
195.133.18.197    - Reported malicious
```

### Your Local Network (Will be rejected):
```
192.168.1.1       - Private IP (app rejects these)
10.0.0.1          - Private IP
127.0.0.1         - Localhost
```

---

## 🐛 Troubleshooting Tests

### Port Already in Use?
Change in `.env`:
```env
PORT=5001
```

### API Errors?
- Check if you have internet connection
- Verify API keys are correct (no extra spaces)
- Check API provider's status page

### Module Not Found?
```powershell
# Make sure venv is activated
.\venv\Scripts\Activate.ps1

# Reinstall if needed
pip install -r requirements.txt
```

---

## ✅ Quick Test Checklist

Run through these:

- [ ] Virtual environment activated `(venv)` in prompt
- [ ] Run `python simple_test.py` - all tests pass
- [ ] Run `python app.py` - server starts
- [ ] Open `http://localhost:5000` - page loads
- [ ] Enter `8.8.8.8` - gets a result (any score)
- [ ] Click "Export JSON" - downloads file
- [ ] Check terminal - no error messages

---

## 📊 What to Expect

### Without API Keys:
```
Threat Score: 0-50 (based on limited data)
Sources: Empty or minimal
Risk Level: Calculated but may be inaccurate
```

### With API Keys:
```
Threat Score: Accurate (0-100)
Sources: AbuseIPDB, VirusTotal, IPGeolocation
Risk Level: Accurate based on real threat data
Categories: Shows actual threat types
```

---

## 🎬 Demo Flow for Testing

1. **Start the app**
   ```powershell
   python app.py
   ```

2. **Test Clean IP**
   - Enter: `8.8.8.8`
   - Should show: LOW risk (green)

3. **Test Suspicious IP**
   - Enter: `185.220.101.1`
   - Should show: MEDIUM-HIGH risk (orange/red)

4. **Export Data**
   - Click "Export JSON"
   - Verify download works

5. **Check API**
   - Visit: `http://localhost:5000/api/health`
   - Should return: `{"status": "healthy"}`

---

## 🚀 You're Ready!

All core components tested and working:
- ✅ Imports
- ✅ IP validation
- ✅ Threat scoring
- ✅ Profile creation
- ✅ Configuration loading

Now just run:
```powershell
python app.py
```

And open: **http://localhost:5000**

---

**Have fun testing!** 🎉
