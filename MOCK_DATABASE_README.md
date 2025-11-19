# Mock Threat Database Documentation

## Overview

The **Mock Threat Database** is a demonstration database containing **10 simulated national/state-level threat actor IP addresses** with complete MITRE ATT&CK intelligence. This allows you to showcase the full capabilities of the IP Risk Radar system without relying on finding real APT infrastructure.

## Purpose

Your mentor correctly identified that finding real national/state-level malicious IPs is challenging. This mock database solves that problem by providing:

✅ **Realistic APT threat data** - Based on actual threat actor groups (APT41, Lazarus, APT36, etc.)  
✅ **Complete MITRE ATT&CK mappings** - Tactics, techniques, campaigns, target sectors  
✅ **Professional PDF reports** - Full intelligence reports with attribution and IOCs  
✅ **Demonstration ready** - Perfect for hackathon presentations and demos  

## Mock IP Addresses

All 10 IP addresses you provided have been configured as national/state-level APT infrastructure:

| IP Address | Threat Actor | Country | Campaign |
|------------|--------------|---------|----------|
| `1.222.92.35` | APT41 (Double Dragon) | China | Operation ShadowPad India |
| `1.225.51.122` | Lazarus Group (Hidden Cobra) | North Korea | Operation DreamJob |
| `1.235.192.131` | APT36 (Transparent Tribe) | Pakistan | Operation Sindoor |
| `1.236.160.55` | APT28 (Fancy Bear) | Russia | Operation Grey Falcon |
| `1.246.248.62` | APT10 (Stone Panda) | China | Operation Cloud Hopper |
| `2.54.97.134` | APT33 (Elfin) | Iran | Operation Shamoon 3.0 |
| `2.55.64.191` | APT15 (Vixen Panda) | China | Operation Diplomatic Orbiter |
| `2.55.85.196` | Kimsuky (Thallium) | North Korea | Operation Stolen Pencil |
| `2.55.122.202` | APT29 (Cozy Bear) | Russia | Operation StellarParticle |
| `2.57.121.15` | SideCopy | Pakistan | Operation SideCopy India |

## Data Structure

Each mock IP contains:

### 1. Threat Actor Information
- **Threat Actor Name** (e.g., "APT41 (Double Dragon)")
- **Country Attribution** (China, Russia, North Korea, Iran, Pakistan)
- **Threat Type** ("Advanced Persistent Threat (APT)")
- **Threat Categories** (Espionage, C2 Server, APT Infrastructure, etc.)

### 2. MITRE ATT&CK Mappings
- **Tactics** - High-level attack phases (Initial Access, Persistence, etc.)
- **Techniques** - Specific attack methods with IDs (T1566.001, T1071.001, etc.)
- **Associated Groups** - APT group aliases
- **Campaign Name** - Operation name and targets
- **Target Sectors** - Industries targeted (Government, Defense, Finance, etc.)
- **Target Regions** - Geographic focus (India, Asia, Global, etc.)

### 3. Malware & IOCs
- **Malware Families** - Known malware used by the group
- **Ports** - Common ports used
- **IOC References** - Advisory references (CERT-In, FBI, etc.)

### 4. Threat Assessment
- **Threat Level** - CRITICAL or HIGH
- **Confidence Score** - 87-96 (high confidence)
- **Abuse Score** - 85-93
- **First/Last Seen** - Simulated timeline

## How It Works

### 1. Detection
When you analyze an IP address, the system first checks if it's in the mock database:

```python
from utils.mock_threat_db import mock_db

if mock_db.is_mock_threat_ip("1.222.92.35"):
    # Use mock data with MITRE intelligence
```

### 2. Data Enrichment
The system:
1. ✅ Queries real APIs for geolocation and network info
2. ✅ **Overrides** with mock MITRE ATT&CK intelligence
3. ✅ Forces threat score to **90-100 (CRITICAL)**
4. ✅ Marks as **malicious APT infrastructure**

### 3. PDF Report Generation
The PDF generator creates a professional report with:
- ⚠️ **Threat Actor identification**
- 🎯 **MITRE ATT&CK techniques** with IDs and descriptions
- 📅 **Campaign information**
- 🦠 **Malware families**
- 🌍 **Target sectors and regions**
- 📊 **CRITICAL confidence level banner**

## Usage

### Test the Mock Database

```bash
# Run the test script
python test_mock_database.py
```

Expected output:
```
🎯 Mock Threat Database Hit: 1.222.92.35
✅ Analysis Complete!
   Threat Score: 95/100
   Risk Level: CRITICAL
   Threat Actor: APT41 (Double Dragon)
   Attribution: China
   Tactics: Initial Access, Persistence, Command and Control
   Malware: ShadowPad, Cobalt Strike, PlugX
```

### Analyze from Frontend

1. Open `http://localhost:8080`
2. Enter any mock IP (e.g., `1.222.92.35`)
3. Click "Analyze IP"
4. See **CRITICAL** threat level with complete APT intelligence
5. Download PDF report with full MITRE mappings

### Generate PDF Report

```bash
# Via API
curl -X POST http://localhost:5000/api/download-report \
  -H "Content-Type: application/json" \
  -d '{"ip": "1.222.92.35"}'
```

The PDF will include:
- 🎯 **MITRE ATT&CK Threat Intelligence** section
- ⚠️ **Identified Threat Actors** with attribution
- ⚔️ **Attack Techniques** table with MITRE IDs
- 🦠 **Malware families**
- 📊 **CRITICAL confidence banner**

## Files

### Core Files
- **`mock_threat_database.json`** - Main database with all 10 IPs
- **`utils/mock_threat_db.py`** - Python module for database access
- **`test_mock_database.py`** - Test script

### Integration Points
- **`core/correlator.py`** - Checks mock DB and enriches profiles
- **`core/scorer.py`** - Gives CRITICAL scores (90-100) for APT IPs
- **`reports/pdf_generator.py`** - Generates MITRE intelligence sections
- **`models/threat_profile.py`** - Added APT fields (threat_actor, campaign, etc.)

## Customization

### Adding More IPs

Edit `mock_threat_database.json`:

```json
{
  "mock_threat_ips": {
    "YOUR.IP.ADDRESS.HERE": {
      "is_malicious": true,
      "threat_level": "CRITICAL",
      "country": "Country Name",
      "threat_actor": "APT Group Name",
      "threat_type": "Advanced Persistent Threat (APT)",
      "categories": ["C2 Server", "Espionage"],
      "mitre_attack": {
        "tactics": ["Initial Access", "Persistence"],
        "techniques": [
          {
            "id": "T1566.001",
            "name": "Phishing: Spearphishing Attachment",
            "description": "Description here"
          }
        ],
        "associated_groups": ["APT Name"],
        "campaign": "Operation Name",
        "target_sectors": ["Government", "Defense"],
        "target_regions": ["India"]
      },
      "malware_families": ["Malware1", "Malware2"]
    }
  }
}
```

### Modifying Threat Scores

In `core/scorer.py`, adjust the scoring logic:

```python
if apt_groups:
    threat_score = 90  # Change this value (0-100)
```

## Demo Workflow

### For Your Hackathon Presentation

1. **Start both servers:**
   ```bash
   .\start-all.ps1
   ```

2. **Analyze a mock IP:**
   - Open frontend: `http://localhost:8080`
   - Enter: `1.222.92.35`
   - Show **CRITICAL** threat level
   - Highlight **APT41** attribution

3. **Download PDF report:**
   - Click "Download Report"
   - Open PDF and show:
     - ⚠️ Threat actor: **APT41 (Double Dragon)**
     - 🌍 Attribution: **China**
     - 🎯 Campaign: **Operation ShadowPad India**
     - ⚔️ MITRE techniques with IDs
     - 🦠 Malware families

4. **Explain the intelligence:**
   - Point out **CRITICAL confidence level**
   - Show **target sectors** (Government, Healthcare)
   - Highlight **target regions** (India focus)
   - Emphasize **national/state-level threat**

## Benefits

✅ **No API Limits** - Mock data doesn't consume API quotas  
✅ **Consistent Results** - Always shows CRITICAL threat level  
✅ **Complete Intelligence** - Full MITRE ATT&CK mappings  
✅ **Professional Reports** - Publication-ready PDF output  
✅ **Demo Ready** - Perfect for presentations  
✅ **Realistic Data** - Based on actual APT groups  

## Real vs Mock Data

### Mock Database Advantages:
- ✅ Guaranteed to show MITRE intelligence
- ✅ Consistent threat scores (90-100)
- ✅ Complete APT attribution
- ✅ No API rate limits

### Real API Data:
- Real-time threat intelligence
- Actual malicious activity
- May not always have APT attribution
- Subject to API limits

## Troubleshooting

### Mock IP not detected?
Check that the IP is in `mock_threat_database.json`:
```python
from utils.mock_threat_db import mock_db
print(mock_db.get_all_mock_ips())
```

### Low threat score?
Verify the scorer is using MITRE boost:
```bash
# Should see: "🎯 Mock Threat Database Hit: X.X.X.X"
python test_mock_database.py
```

### PDF missing MITRE section?
Check that `mitre_intelligence['found']` is `True`:
```python
profile.mitre_intelligence['found']  # Should be True
```

## Support

For issues or questions:
1. Check `test_mock_database.py` output
2. Verify all files are in place
3. Ensure servers are running (`start-all.ps1`)
4. Check console for error messages

---

**Created for:** TICE Hackathon Project  
**Purpose:** Demonstrate national/state-level threat intelligence capabilities  
**Database Version:** 1.0  
**Last Updated:** 2025-11-07
