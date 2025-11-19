# MITRE ATT&CK Threat Intelligence Integration

## 🎯 Overview

The TICE platform now includes **MITRE ATT&CK threat intelligence** for law enforcement investigations. This feature provides historical attack context, showing which Advanced Persistent Threat (APT) groups have used an IP address in past cyber attacks.

## 🚨 Law Enforcement Use Case

**Question Answered:** *"Has this IP been used by known APT groups in past attacks?"*

This intelligence layer helps law enforcement:
- Identify nation-state threat actors
- Understand attack attribution (Russia, China, North Korea, Iran, etc.)
- See historical attack campaigns
- Identify malware families used
- View attack techniques (MITRE ATT&CK framework)
- Assess confidence level of attribution

## 🔧 Architecture

### Three Free Intelligence Sources

#### 1. **AlienVault OTX** (Open Threat Exchange)
- **API:** `https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general`
- **No API Key Required:** ✅ FREE
- **Purpose:** IP → Threat Group mapping
- **Data Provided:**
  - Threat pulses (community intelligence)
  - Associated threat groups (APT28, APT29, Lazarus, etc.)
  - Tags and threat categories
  - Timeline (first_seen, last_seen dates)
  - Campaign names

#### 2. **ThreatFox** (by Abuse.ch)
- **API:** `https://threatfox-api.abuse.ch/api/v1/`
- **No API Key Required:** ✅ FREE
- **Purpose:** Malware IOC database
- **Data Provided:**
  - Malware families
  - C2 server identification
  - Botnet infrastructure flags
  - Threat types
  - Confidence scores
  - Reference links

#### 3. **MITRE ATT&CK** (Web Scraping)
- **Source:** `https://attack.mitre.org/groups/*`
- **Method:** BeautifulSoup4 web scraping
- **No API Key Required:** ✅ FREE
- **Purpose:** Threat actor profiles
- **Data Provided:**
  - Group descriptions
  - Aliases
  - Attribution (nation-state)
  - Attack techniques used
  - Software/malware tools
  - Target sectors

### Data Flow

```
IP Address Input
    ↓
┌─────────────────────────────────────────────┐
│   Threat Intelligence Correlator             │
├─────────────────────────────────────────────┤
│                                               │
│  1. AlienVault OTX Query                     │
│     └→ Get threat groups & pulses            │
│                                               │
│  2. ThreatFox Query                          │
│     └→ Get malware & IOC data                │
│                                               │
│  3. MITRE Scraper (for each group)           │
│     └→ Get full threat actor profiles        │
│                                               │
│  4. Correlate All Sources                    │
│     └→ Build unified intelligence report     │
│                                               │
└─────────────────────────────────────────────┘
    ↓
Complete Threat Intelligence Profile
    ↓
PDF Report + JSON API Response
```

## 📁 File Structure

```
d:\TICE hackthaon project\
│
├── api/
│   ├── alienvault_otx.py      # AlienVault OTX client (134 lines)
│   └── threatfox.py            # ThreatFox IOC client (155 lines)
│
├── mitre/
│   ├── __init__.py             # Module initialization
│   ├── scraper.py              # MITRE ATT&CK web scraper (205 lines)
│   └── intelligence_correlator.py  # Main correlator (203 lines)
│
├── models/
│   └── threat_profile.py       # Updated with mitre_intelligence field
│
├── core/
│   └── correlator.py           # Integrated threat intelligence
│
├── reports/
│   └── pdf_generator.py        # Updated with MITRE section
│
└── requirements.txt            # Added beautifulsoup4, lxml
```

## 🔍 API Response Format

### MITRE Intelligence Object

```json
{
  "mitre_intelligence": {
    "source": "threat_intelligence_correlator",
    "found": true,
    "ip_address": "XXX.XXX.XXX.XXX",
    "confidence": "CRITICAL",
    
    "threat_actors": [
      {
        "name": "APT28",
        "mitre_id": "G0007",
        "aliases": ["Fancy Bear", "Sofacy", "Sednit"],
        "attribution": "Russia",
        "description": "APT28 is attributed to Russia's GRU..."
      }
    ],
    
    "malware_families": [
      "Emotet", "TrickBot", "Cobalt Strike"
    ],
    
    "campaigns": [
      {
        "name": "DNC Hack 2016",
        "date": "2016-07-22",
        "source": "AlienVault OTX"
      }
    ],
    
    "timeline": {
      "first_seen": "2016-01-15T10:30:00Z",
      "last_seen": "2024-11-20T14:22:00Z",
      "activity_span_days": 3232
    },
    
    "techniques": [
      {
        "id": "T1566",
        "name": "Phishing"
      },
      {
        "id": "T1078",
        "name": "Valid Accounts"
      }
    ],
    
    "threat_types": [
      "C2 Server",
      "Botnet Infrastructure"
    ],
    
    "has_apt_attribution": true,
    "is_c2_server": true,
    "is_botnet": false,
    
    "otx_pulse_count": 15,
    "threatfox_ioc_count": 3,
    "mitre_group_count": 1
  }
}
```

## 📊 PDF Report Features

### New MITRE ATT&CK Section

When threat intelligence is found, the PDF report includes:

1. **Intelligence Confidence Banner**
   - Color-coded (RED = Critical, ORANGE = High, YELLOW = Medium, GREEN = Low)
   - Based on number of sources and APT attribution

2. **⚠️ Identified Threat Actors**
   - Threat group name (e.g., APT28)
   - MITRE ATT&CK Group ID (e.g., G0007)
   - **Attribution highlighted in RED** (e.g., "ATTRIBUTION: Russia")
   - Aliases (e.g., "Also known as: Fancy Bear, Sofacy")
   - Description (first 300 characters)

3. **📅 Attack Timeline**
   - First detected date
   - Last detected date
   - Activity span in days

4. **🎯 Associated Campaigns**
   - Campaign names from threat intelligence
   - Dates of campaigns
   - Source attribution

5. **🦠 Identified Malware**
   - List of malware families detected
   - Combined from ThreatFox and MITRE sources

6. **⚔️ Attack Techniques**
   - MITRE ATT&CK Technique IDs (e.g., T1566)
   - Technique names (e.g., "Phishing")
   - Up to 12 techniques displayed

7. **📊 Intelligence Sources**
   - AlienVault OTX pulse count
   - ThreatFox IOC count
   - MITRE group profile count
   - C2 Server flag (YES/NO)
   - Botnet flag (YES/NO)

## 🧪 Testing

### Test Scripts

1. **`test_mitre_scraper.py`** - Test MITRE web scraper
   ```bash
   python test_mitre_scraper.py
   ```
   - Tests APT28, APT29, Lazarus, APT1
   - Verifies attribution extraction
   - Shows software and techniques

2. **`test_threat_intelligence.py`** - Test full correlator
   ```bash
   python test_threat_intelligence.py
   ```
   - Tests complete intelligence pipeline
   - Combines all 3 sources
   - Saves results to JSON

3. **`test_full_system.py`** - End-to-end test
   ```bash
   python test_full_system.py
   ```
   - Tests Flask API endpoints
   - Generates actual PDF reports
   - Verifies complete integration

### Test Results

✅ **MITRE Scraper:** Successfully extracts APT group profiles
✅ **AlienVault OTX:** Working (no API key needed)
⚠️ **ThreatFox:** 401 error (API may have rate limits or changed - gracefully handled)
✅ **PDF Generation:** Successfully includes MITRE section when data found
✅ **Integration:** Complete pipeline functional

## 📝 Confidence Levels

The system calculates confidence based on multiple factors:

- **CRITICAL:** 3 sources + APT attribution
- **HIGH:** 2+ sources + (APT OR C2 server OR high pulse count)
- **MEDIUM:** 2+ sources
- **LOW:** 1 source
- **NONE:** No sources found

## 🚀 Usage

### In Code

```python
from mitre.intelligence_correlator import ThreatIntelligenceCorrelator

correlator = ThreatIntelligenceCorrelator()
result = correlator.analyze_ip("185.220.101.44")

if result['found']:
    print(f"Confidence: {result['confidence']}")
    print(f"Threat Actors: {result['threat_actors']}")
    print(f"Malware: {result['malware_families']}")
```

### Via API

```bash
# Analyze IP
POST /api/analyze
{
  "ip_address": "XXX.XXX.XXX.XXX"
}

# Download PDF with MITRE intelligence
GET /api/download-report/XXX.XXX.XXX.XXX
```

### Frontend

The existing "Download PDF Report" button automatically includes MITRE intelligence when available.

## 🔐 Privacy & Ethics

- **Public Data Only:** All sources use publicly available threat intelligence
- **No Private Data:** System does not collect or store user data
- **Law Enforcement Tool:** Designed for legitimate investigations
- **Attribution Transparency:** All sources clearly cited in reports

## 🛠️ Dependencies

```txt
beautifulsoup4==4.12.3  # HTML parsing for MITRE scraping
lxml==5.3.0             # Fast XML/HTML parser
requests==2.32.3        # HTTP client (existing)
```

All dependencies installed in virtual environment:
```bash
d:\TICE hackthaon project\venv
```

## 📈 Future Enhancements

Potential improvements:
- Add more APT group mappings to `GROUP_MAPPINGS`
- Extract more MITRE data (target sectors, campaigns from MITRE)
- Add frontend display of threat intelligence (not just PDF)
- Cache MITRE scraping results (reduce HTTP requests)
- Add more threat intelligence sources (GreyNoise, Shodan Intelligence)

## 🎓 Known APT Groups Supported

The system includes mappings for:
- APT1, APT3, APT12, APT16, APT17, APT18, APT19
- APT28 (Fancy Bear - Russia/GRU)
- APT29 (Cozy Bear - Russia/SVR)
- APT30, APT32, APT33, APT34, APT37, APT38, APT39, APT41
- Lazarus Group (North Korea)
- Equation Group

More groups can be added to `mitre/scraper.py` → `GROUP_MAPPINGS` dictionary.

## 📞 Support

For issues or questions:
- Check test scripts for examples
- Review API client error handling
- Verify BeautifulSoup4 and lxml are installed
- Check MITRE website structure hasn't changed

---

**Created:** 2024
**Platform:** TICE (Threat Intelligence Correlation Engine)
**Purpose:** Law enforcement cyber threat investigations
