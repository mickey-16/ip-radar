# 🚀 TICE Quick Reference Card

## Installation (One-Time Setup)

```powershell
# Option 1: Use setup script (EASIEST)
.\setup.ps1

# Option 2: Manual setup
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your API keys
notepad .env
```

## Running the Application

```powershell
# Option 1: Use run script
.\run.ps1

# Option 2: Manual run
.\venv\Scripts\activate
python app.py

# Access at: http://localhost:5000
```

## API Keys (Get These First!)

| Service | URL | Free Limit |
|---------|-----|------------|
| AbuseIPDB | https://www.abuseipdb.com/api | 1,000/day |
| VirusTotal | https://www.virustotal.com/gui/join-us | 500/day |
| IPGeolocation | https://ipgeolocation.io/signup | 1,000/day |

## Test IP Addresses

### Malicious IPs (Should show HIGH scores)
```
185.220.101.1    # Tor exit node
45.142.212.61    # Known attacker
195.133.18.197   # Botnet activity
```

### Clean IPs (Should show LOW scores)
```
8.8.8.8          # Google DNS
1.1.1.1          # Cloudflare DNS
208.67.222.222   # OpenDNS
```

## API Endpoints

### Analyze IP (POST)
```powershell
curl -X POST http://localhost:5000/api/analyze `
  -H "Content-Type: application/json" `
  -d '{"ip_address": "8.8.8.8"}'
```

### Quick Summary (GET)
```powershell
curl http://localhost:5000/api/summary/8.8.8.8
```

### Health Check
```powershell
curl http://localhost:5000/api/health
```

### Configuration Info
```powershell
curl http://localhost:5000/api/config
```

## File Structure Cheat Sheet

```
app.py                    # Start here - main application
config.py                 # Configure scoring weights
.env                      # YOUR API KEYS GO HERE

api/
  abuseipdb.py           # AbuseIPDB integration
  virustotal.py          # VirusTotal integration
  ipgeolocation.py       # Geolocation integration

core/
  correlator.py          # Main orchestrator
  normalizer.py          # Data normalization
  scorer.py              # Threat scoring algorithm

models/
  threat_profile.py      # Data model

templates/
  index.html             # Web UI
```

## Common Commands

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Deactivate virtual environment
deactivate

# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Clear cache
Remove-Item cache\*.json

# Check Python version
python --version

# Test if Flask is working
python -c "import flask; print(flask.__version__)"
```

## Troubleshooting

### "Module not found"
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

### "Port 5000 already in use"
Edit `.env`:
```
PORT=5001
```

### "API key invalid"
1. Check `.env` file
2. No quotes around keys
3. No extra spaces
4. Verify key on API provider's website

### "No module named 'dotenv'"
```powershell
pip install python-dotenv
```

### Clear everything and restart
```powershell
Remove-Item -Recurse venv
Remove-Item -Recurse cache
.\setup.ps1
```

## Scoring Algorithm Quick Reference

### Risk Levels
- 0-20: 🟢 Low (Benign)
- 21-50: 🟡 Medium (Suspicious)
- 51-75: 🟠 High (Likely Malicious)
- 76-100: 🔴 Critical (Confirmed Malicious)

### Scoring Weights (Configurable in config.py)
```python
AbuseIPDB:      30%
VirusTotal:     25%
IPGeolocation:  20%
GreyNoise:      15%
Shodan:         10%
```

### Category Modifiers
```
High Risk (+15-20):
  - C2 Server
  - Botnet
  - Ransomware
  - Known Attacker

Medium Risk (+5-10):
  - Spam
  - Brute Force
  - Scanner
  - DDoS
```

## Demo Script (7 minutes)

### 1. Problem (1 min)
"Analysts spend 10-15 min checking each IP manually across multiple sites"

### 2. Solution (1 min)
"TICE automates this in seconds with intelligent correlation"

### 3. Live Demo (3 min)
- Test 8.8.8.8 → Low score
- Test 185.220.101.1 → High score
- Show JSON export

### 4. Technical (1 min)
- Concurrent API calls
- Weighted scoring
- Smart caching

### 5. Future (1 min)
- ML prediction
- Bulk analysis
- SIEM integration

## Important Files to Review Before Demo

1. ✅ `README.md` - Overview for GitHub
2. ✅ `PROJECT_SUMMARY.md` - Technical details
3. ✅ `SETUP.md` - Installation guide
4. ✅ `.env` - Has all your API keys
5. ✅ `templates/index.html` - UI looks good

## Performance Tips

```powershell
# Use caching (default: enabled)
# APIs are called concurrently
# Timeout: 10 seconds per API
# Cache TTL: 1 hour

# To disable caching for testing:
# In your API request:
{"ip_address": "8.8.8.8", "use_cache": false}
```

## Security Checklist

- [ ] Never commit `.env` file
- [ ] Keep API keys secret
- [ ] Validate all inputs
- [ ] Use HTTPS in production
- [ ] Rate limit API endpoints
- [ ] Sanitize user inputs

## Customization Quick Tips

### Change Scoring Weights
Edit `config.py`:
```python
SCORING_WEIGHTS = {
    'abuseipdb': 0.40,     # Increase importance
    'virustotal': 0.30,
    ...
}
```

### Change Risk Thresholds
Edit `config.py`:
```python
RISK_LEVELS = {
    'low': (0, 15),        # More strict
    'medium': (16, 40),
    ...
}
```

### Change Cache Duration
Edit `config.py`:
```python
CACHE_DEFAULT_TIMEOUT = 7200  # 2 hours
```

### Add Custom Categories
Edit `utils/helpers.py` → `normalize_category()`

## Git Commands for Submission

```powershell
# Initialize repo
git init
git add .
git commit -m "Initial commit - TICE v1.0"

# Create GitHub repo, then:
git remote add origin https://github.com/yourusername/TICE.git
git branch -M main
git push -u origin main
```

## Final Checklist Before Demo

- [ ] `.env` file has all 3 API keys
- [ ] Test with 8.8.8.8 (should work)
- [ ] Test with malicious IP
- [ ] UI loads correctly
- [ ] JSON export works
- [ ] README is updated with your team info
- [ ] Screenshots added (optional)
- [ ] Practiced demo script

## Emergency Contacts

- Flask docs: https://flask.palletsprojects.com/
- Python docs: https://docs.python.org/3/
- Bootstrap docs: https://getbootstrap.com/docs/

---

**You're all set! Good luck! 🚀**
