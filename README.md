# 🛡️ TICE - Threat Intelligence Correlation Engine

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> An AI-powered threat intelligence platform that aggregates, normalizes, and correlates data from multiple threat intelligence sources to provide comprehensive IP reputation analysis.

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Integrations](#api-integrations)
- [Threat Scoring Algorithm](#threat-scoring-algorithm)
- [Dark Web Intelligence](#-dark-web-intelligence)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

**TICE (Threat Intelligence Correlation Engine)** is a comprehensive cybersecurity tool designed to help investigators and security analysts quickly assess the threat level of IP addresses by automatically querying multiple threat intelligence sources and providing a unified, actionable report.

## 🚨 Problem Statement

Cybercrime investigators face significant challenges:
- **Fragmented Data**: Threat intelligence is scattered across multiple sources
- **Manual Verification**: Time-consuming process to check each IP across different platforms
- **Inconsistent Formats**: Each API provides data in different structures
- **No Unified View**: Difficult to get a comprehensive threat assessment quickly

## ✨ Features167.172.58.23      - DigitalOcean datacenter IP
54.86.50.139       - AWS EC2 instance
13.107.42.14       - Microsoft Azure

### Core Functionality
- 🔍 **Multi-Source Intelligence**: Queries 5+ threat intelligence APIs simultaneously
- 🔄 **Data Normalization**: Standardizes disparate data formats into unified profiles
- 📊 **Threat Scoring**: Advanced algorithm that calculates risk scores (0-100)
- 🎯 **Threat Attribution**: Identifies threat categories (botnet, C2, phishing, spam, proxy)
- 🌍 **Geolocation & ASN**: Detailed geographic and network information
- 🔗 **Related Entities**: Discovers linked domains, URLs, and malware samples
 - 🕵️ **Dark Web Intelligence**: Detects Tor exit nodes, tracks malware URLs via URLhaus (abuse.ch), and computes a dark web threat level that can boost overall risk

### User Interface
- 📱 **Web Dashboard**: Intuitive, responsive interface
- 📈 **Visual Analytics**: Charts and graphs for threat data
- 📄 **Detailed Reports**: Comprehensive threat attribution reports
- 💾 **Export Options**: Download results in JSON/PDF format
- 🚀 **Real-time Analysis**: Instant results from multiple sources

## 🏗️ Architecture

```
┌─────────────────┐
│   Web Frontend  │
│  (Bootstrap +   │
│   Chart.js)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Backend  │
│   (REST API)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│      Threat Intelligence Layer          │
├─────────────────────────────────────────┤
│  • API Integration Module               │
│  • Data Normalization Engine            │
│  • Threat Scoring Algorithm             │
│  • Correlation Engine                   │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│     External Threat Intel APIs          │
├─────────────────────────────────────────┤
│  • AbuseIPDB                            │
│  • VirusTotal                           │
│  • IPQualityScore                       │
│  • Shodan                               │
│  • GreyNoise                            │
│  • IPGeolocation                        │
└─────────────────────────────────────────┘
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- API keys for threat intelligence services (see [API Integrations](#api-integrations))

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/TICE.git
cd TICE
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys
Create a `.env` file in the project root:
```env
# Threat Intelligence APIs
ABUSEIPDB_API_KEY=your_abuseipdb_key
VIRUSTOTAL_API_KEY=your_virustotal_key
IPQUALITYSCORE_API_KEY=your_ipqs_key
SHODAN_API_KEY=your_shodan_key
GREYNOISE_API_KEY=your_greynoise_key
IPGEOLOCATION_API_KEY=your_ipgeo_key
HAVEIBEENPWNED_API_KEY=optional_hibp_key   # Optional, for future breach checks

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

Note: The Dark Web Intelligence feature works with public data sources and does not require any API keys. The Have I Been Pwned key is optional and reserved for future breach lookups.

### Step 5: Run the Application
```bash
# Development server
python app.py

# Production server (with gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Access the dashboard at: `http://localhost:5000`

## 📖 Usage

### Web Dashboard
1. Navigate to `http://localhost:5000`
2. Enter an IP address in the search field
3. Click "Analyze Threat"
4. View the consolidated threat intelligence report

### API Endpoint
```bash
# Query IP address
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ip_address": "8.8.8.8"}'

# Response format
{
  "ip_address": "8.8.8.8",
  "threat_score": 15,
  "risk_level": "low",
  "categories": ["proxy"],
  "geolocation": {
    "country": "United States",
    "city": "Mountain View",
    "asn": "AS15169",
    "isp": "Google LLC"
  },
  "sources": {
    "abuseipdb": {...},
    "virustotal": {...},
    "ipqualityscore": {...}
  },
  "related_entities": {
    "domains": [],
    "urls": [],
    "malware": []
  },
  "darkweb_intelligence": {
    "found_in_darkweb": false,
    "tor_exit_node": false,
    "malware_urls": {"found": false, "url_count": 0, "urls": []},
    "threat_level": "none",
    "indicators": []
  },
  "timestamp": "2025-11-06T10:30:00Z"
}
```

### CLI Mode (Optional)
```bash
python cli.py --ip 192.168.1.1
python cli.py --ip 8.8.8.8 --output report.json
```

## 🔌 API Integrations

### Supported Threat Intelligence Sources

| Service | Free Tier | Rate Limit | Features |
|---------|-----------|------------|----------|
| **AbuseIPDB** | ✅ Yes | 1,000/day | Abuse reports, confidence score |
| **VirusTotal** | ✅ Yes | 500/day | Malware detection, URL scanning |
| **IPQualityScore** | ✅ Yes | 5,000/month | Proxy/VPN detection, fraud score |
| **Shodan** | ⚠️ Limited | 100/month | Port scanning, service detection |
| **GreyNoise** | ✅ Yes | 5,000/day | Internet scanner classification |
| **IPGeolocation** | ✅ Yes | 1,000/day | Geolocation, ASN information |
| **Tor Project Exit List** | ✅ Yes | None | Tor exit node detection (public list) |
| **URLhaus (abuse.ch)** | ✅ Yes | None | Malware URL database lookup |

### Getting API Keys

1. **AbuseIPDB**: https://www.abuseipdb.com/api
2. **VirusTotal**: https://www.virustotal.com/gui/join-us
3. **IPQualityScore**: https://www.ipqualityscore.com/create-account
4. **Shodan**: https://account.shodan.io/register
5. **GreyNoise**: https://www.greynoise.io/signup
6. **IPGeolocation**: https://ipgeolocation.io/signup

## 🧮 Threat Scoring Algorithm

Our proprietary scoring algorithm combines multiple factors:

### Scoring Components
```python
Final Score = (
    AbuseIPDB_Score × 0.30 +
    VirusTotal_Score × 0.25 +
    IPQS_Score × 0.20 +
    GreyNoise_Score × 0.15 +
    Shodan_Score × 0.10
)
```

### Risk Levels
- **0-20**: 🟢 Low Risk (Benign)
- **21-50**: 🟡 Medium Risk (Suspicious)
- **51-75**: 🟠 High Risk (Likely Malicious)
- **76-100**: 🔴 Critical Risk (Confirmed Malicious)

### Threat Categories
- **Botnet**: Part of a botnet network
- **C2 (Command & Control)**: C2 server infrastructure
- **Phishing**: Hosting phishing sites
- **Spam**: Email spam source
- **Proxy/VPN**: Anonymous proxy or VPN exit node
- **Malware**: Malware distribution
- **Scanner**: Port/vulnerability scanner

### Dark Web Scoring Boosts
- Critical (malware + Tor): +15
- High (malware URLs): +10
- Medium (Tor exit node): +5
- Low/None: +0

See the Dark Web Intelligence section below for how these are determined.

## �️ Dark Web Intelligence

TICE includes real-time dark web intelligence using safe, public sources—no Tor access required.

What it checks
- Tor Exit Node Detection: Uses the official Tor Project bulk exit list to flag anonymous egress IPs.
- Malware URL Tracking: Uses URLhaus (abuse.ch) to find malicious URLs hosted on the IP.
- Threat Level Calculation: Derives a dark web threat level (none/low/medium/high/critical) and boosts the overall score accordingly.

Data sources
- Tor Project Exit List: https://check.torproject.org/torbulkexitlist
- URLhaus API (abuse.ch): https://urlhaus-api.abuse.ch/v1/host/

Backend integration
- Implemented in `api/darkweb_intel.py` and integrated in `core/correlator.py`.
- Results are added to each analysis under `darkweb_intelligence` in the API response and PDF reports.

Quick test IPs
- Tor exit node example: 185.220.101.1 (should show activity = true, level = medium)
- Clean IP example: 8.8.8.8 (no dark web activity)

For a deep dive with screenshots and examples, see `DARKWEB_FEATURE_SUMMARY.md`.

## �📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Threat Report
![Threat Report](screenshots/report.png)

### Analytics
![Analytics](screenshots/analytics.png)

## 🗂️ Project Structure

```
TICE/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
│
├── api/                       # API integration modules
│   ├── __init__.py
│   ├── abuseipdb.py
│   ├── virustotal.py
│   ├── ipqualityscore.py
│   ├── shodan.py
│   ├── greynoise.py
│   └── ipgeolocation.py
│
├── core/                      # Core engine
│   ├── __init__.py
│   ├── normalizer.py         # Data normalization
│   ├── scorer.py             # Threat scoring algorithm
│   └── correlator.py         # Intelligence correlation
│
├── models/                    # Data models
│   ├── __init__.py
│   └── threat_profile.py
│
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── cache.py              # Response caching
│   └── helpers.py
│
├── static/                    # Frontend assets
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/                 # HTML templates
│   ├── index.html
│   ├── report.html
│   └── dashboard.html
│
└── tests/                     # Unit tests
    ├── test_api.py
    ├── test_scorer.py
    └── test_normalizer.py
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test
python -m pytest tests/test_scorer.py

# Quick dark web checks (optional)
python test_darkweb.py
python test_darkweb_quick.py
```

## 🔮 Future Enhancements

- [ ] Machine learning-based threat prediction
- [ ] Historical threat tracking and trends
- [ ] Bulk IP analysis (CSV upload)
- [ ] Email notifications for critical threats
- [ ] Integration with SIEM platforms
- [x] Dark web intelligence integration
- [ ] Automated threat hunting workflows
- [ ] Multi-language support
- [ ] Mobile application

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👥 Team

- **Your Name** - Lead Developer - [GitHub](https://github.com/yourusername)
- **Team Member 2** - Backend Developer
- **Team Member 3** - Frontend Developer

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all threat intelligence API providers for their free tiers
- Inspired by the need for better cybersecurity tools
- Built for [Hackathon Name] 2025

## 📧 Contact

For questions or support:
- **Email**: your.email@example.com
- **Twitter**: [@yourhandle](https://twitter.com/yourhandle)
- **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)

---

<div align="center">
Made with ❤️ for cybersecurity professionals

**⭐ Star this repo if you find it helpful!**
</div>
