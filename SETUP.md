# 🚀 TICE Setup Guide

## Quick Start (3 Steps!)

### Step 1: Install Dependencies
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Get FREE API Keys (15 minutes)

You need at least these 3 API keys to get started:

#### 1. AbuseIPDB (REQUIRED)
- Visit: https://www.abuseipdb.com/api
- Sign up for free account
- Go to API section
- Copy your API key
- Free tier: 1,000 requests/day

#### 2. VirusTotal (REQUIRED)
- Visit: https://www.virustotal.com/gui/join-us
- Sign up with email
- Go to your profile → API Key
- Copy your API key
- Free tier: 500 requests/day

#### 3. IPGeolocation (REQUIRED)
- Visit: https://ipgeolocation.io/signup
- Sign up for free
- Dashboard → Copy API key
- Free tier: 1,000 requests/day

### Step 3: Configure Environment

Create a `.env` file in the project root:

```powershell
# Copy the example file
copy .env.example .env

# Edit .env with your API keys
notepad .env
```

Add your API keys to `.env`:
```env
ABUSEIPDB_API_KEY=your_actual_key_here
VIRUSTOTAL_API_KEY=your_actual_key_here
IPGEOLOCATION_API_KEY=your_actual_key_here
```

### Step 4: Run the Application

```powershell
python app.py
```

Open your browser: http://localhost:5000

## Testing

Test with these sample IPs:

### Known Malicious IPs (High Scores)
- `185.220.101.1` - Tor exit node
- `45.142.212.61` - Known attacker
- `195.133.18.197` - Botnet activity

### Clean IPs (Low Scores)
- `8.8.8.8` - Google DNS
- `1.1.1.1` - Cloudflare DNS
- `208.67.222.222` - OpenDNS

## Troubleshooting

### Issue: Module not found
```powershell
pip install -r requirements.txt
```

### Issue: API key not working
- Check if API key is correctly copied in `.env`
- Make sure there are no quotes around the key
- Verify the API key is active on the provider's website

### Issue: Port already in use
Edit `.env` and change:
```env
PORT=5001
```

## API Usage

### Analyze IP via API
```powershell
# Using curl (install: choco install curl)
curl -X POST http://localhost:5000/api/analyze -H "Content-Type: application/json" -d "{\"ip_address\": \"8.8.8.8\"}"

# Using PowerShell
Invoke-RestMethod -Uri "http://localhost:5000/api/analyze" -Method POST -ContentType "application/json" -Body '{"ip_address": "8.8.8.8"}'
```

### Get Quick Summary
```powershell
curl http://localhost:5000/api/summary/8.8.8.8
```

## Project Structure

```
TICE/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Your API keys (create this)
├── .env.example          # Template for .env
│
├── api/                   # API integration modules
│   ├── abuseipdb.py      # AbuseIPDB client
│   ├── virustotal.py     # VirusTotal client
│   └── ipgeolocation.py  # IPGeolocation client
│
├── core/                  # Core engine
│   ├── normalizer.py     # Data normalization
│   ├── scorer.py         # Threat scoring
│   └── correlator.py     # Main orchestrator
│
├── models/               # Data models
│   └── threat_profile.py # Unified threat profile
│
├── utils/                # Utilities
│   ├── helpers.py        # Helper functions
│   └── cache.py          # Caching system
│
└── templates/            # HTML templates
    └── index.html        # Main dashboard
```

## Next Steps

1. ✅ Get your API keys
2. ✅ Configure .env file
3. ✅ Install dependencies
4. ✅ Run the app
5. ✅ Test with sample IPs
6. 🎨 Customize the scoring weights in `config.py`
7. 📊 Add more features
8. 🎤 Prepare your demo!

## Hackathon Tips

### What to Highlight
- ✨ Real-time multi-source aggregation
- 🧮 Smart weighted scoring algorithm
- 🎯 Accurate threat categorization
- ⚡ Fast response time (concurrent API calls)
- 💾 Intelligent caching
- 📊 Clean, professional UI

### Demo Script
1. Start with a clean IP (8.8.8.8) - show low score
2. Then analyze a malicious IP - show high score
3. Explain the scoring algorithm
4. Show the JSON export feature
5. Mention scalability (can add more sources)

### Potential Improvements to Mention
- Machine learning for predictive analysis
- Historical tracking
- Bulk IP analysis
- Integration with SIEM systems
- Email alerts for critical threats

## Support

For issues or questions:
- Check the logs in the terminal
- Verify API keys are valid
- Test each API individually
- Check your internet connection

---

**Good luck with your hackathon! 🚀**
