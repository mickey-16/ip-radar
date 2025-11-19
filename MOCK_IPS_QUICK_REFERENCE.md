# Mock Threat Database - Quick Reference

## 🎯 10 National/State-Level APT IP Addresses

Use these IPs for demonstrations, testing, and PDF report generation.

---

## 1. **1.222.92.35** - APT41 (China)
- **Threat Actor:** APT41 (Double Dragon)
- **Attribution:** China
- **Campaign:** Operation ShadowPad India
- **Target:** Government, Healthcare, Telecommunications, Education
- **Tactics:** Initial Access, Persistence, Command and Control, Exfiltration
- **Malware:** ShadowPad, Cobalt Strike, PlugX
- **Threat Level:** ⛔ **CRITICAL** (95/100)

---

## 2. **1.225.51.122** - Lazarus Group (North Korea)
- **Threat Actor:** Lazarus Group (Hidden Cobra)
- **Attribution:** North Korea
- **Campaign:** Operation DreamJob
- **Target:** Financial Services, Cryptocurrency, Banking, Technology
- **Tactics:** Initial Access, Execution, Defense Evasion, Impact
- **Malware:** AppleJeus, Dacls, RATANKBA
- **Threat Level:** ⛔ **CRITICAL** (100/100)

---

## 3. **1.235.192.131** - APT36 (Pakistan)
- **Threat Actor:** APT36 (Transparent Tribe)
- **Attribution:** Pakistan
- **Campaign:** Operation Sindoor
- **Target:** Defense, Government, Military, Diplomatic
- **Tactics:** Reconnaissance, Initial Access, Persistence, Collection, C2
- **Malware:** Crimson RAT, ObliqueRAT
- **Threat Level:** ⛔ **CRITICAL** (95/100)

---

## 4. **1.236.160.55** - APT28 (Russia)
- **Threat Actor:** APT28 (Fancy Bear)
- **Attribution:** Russia (GRU)
- **Campaign:** Operation Grey Falcon
- **Target:** Government, Diplomatic, Defense, Media
- **Tactics:** Initial Access, Credential Access, Lateral Movement, Exfiltration
- **Malware:** X-Agent, Sofacy, Zebrocy
- **Threat Level:** ⚠️ **HIGH** (91/100)

---

## 5. **1.246.248.62** - APT10 (China)
- **Threat Actor:** APT10 (Stone Panda)
- **Attribution:** China (MSS)
- **Campaign:** Operation Cloud Hopper
- **Target:** Managed Services, Cloud Providers, Technology, Telecom
- **Tactics:** Initial Access, Execution, Persistence, Defense Evasion, Collection
- **Malware:** QuasarRAT, PlugX, RedLeaves
- **Threat Level:** ⛔ **CRITICAL** (94/100)

---

## 6. **2.54.97.134** - APT33 (Iran)
- **Threat Actor:** APT33 (Elfin)
- **Attribution:** Iran
- **Campaign:** Operation Shamoon 3.0
- **Target:** Energy, Oil & Gas, Aviation, Government
- **Tactics:** Initial Access, Execution, Persistence, Impact
- **Malware:** Shamoon, Dropshot, Turnedup
- **Threat Level:** ⚠️ **HIGH** (87/100)

---

## 7. **2.55.64.191** - APT15 (China)
- **Threat Actor:** APT15 (Vixen Panda)
- **Attribution:** China
- **Campaign:** Operation Diplomatic Orbiter
- **Target:** Diplomatic, Trade, Government, Think Tanks
- **Tactics:** Initial Access, Execution, Defense Evasion, C2, Exfiltration
- **Malware:** RoyalCli, RoyalDNS, BS2005
- **Threat Level:** ⛔ **CRITICAL** (92/100)

---

## 8. **2.55.85.196** - Kimsuky (North Korea)
- **Threat Actor:** Kimsuky (Thallium)
- **Attribution:** North Korea
- **Campaign:** Operation Stolen Pencil
- **Target:** Research, Think Tanks, Academia, Government
- **Tactics:** Reconnaissance, Initial Access, Credential Access, Collection
- **Malware:** BabyShark, AppleSeed, PebbleDash
- **Threat Level:** ⚠️ **HIGH** (88/100)

---

## 9. **2.55.122.202** - APT29 (Russia)
- **Threat Actor:** APT29 (Cozy Bear)
- **Attribution:** Russia (SVR)
- **Campaign:** Operation StellarParticle (SolarWinds-style)
- **Target:** Government, Technology, Research, Think Tanks
- **Tactics:** Initial Access, Execution, Persistence, Defense Evasion, C2
- **Malware:** Sunburst, Teardrop, Raindrop, GoldMax
- **Threat Level:** ⛔ **CRITICAL** (96/100)

---

## 10. **2.57.121.15** - SideCopy (Pakistan)
- **Threat Actor:** SideCopy (APT36 variant)
- **Attribution:** Pakistan
- **Campaign:** Operation SideCopy India
- **Target:** Defense, Military, Government, Research
- **Tactics:** Initial Access, Execution, Persistence, Collection, Exfiltration
- **Malware:** ActionRAT, AuTo Stealer, AllaKore RAT
- **Threat Level:** ⚠️ **HIGH** (90/100)

---

## 📊 Statistics

| Country | Count | % |
|---------|-------|---|
| 🇨🇳 China | 4 | 40% |
| 🇷🇺 Russia | 2 | 20% |
| 🇰🇵 North Korea | 2 | 20% |
| 🇵🇰 Pakistan | 2 | 20% |
| 🇮🇷 Iran | 1 | 10% |

| Threat Level | Count |
|--------------|-------|
| ⛔ CRITICAL | 6 |
| ⚠️ HIGH | 4 |

---

## 🎯 Best IPs for Demo

### Most Impressive for Presentation:
1. **2.55.122.202** (APT29 - SolarWinds-level threat)
2. **1.222.92.35** (APT41 - Targeting India specifically)
3. **1.225.51.122** (Lazarus - Financial crime focus)

### India-Focused Threats:
- **1.222.92.35** - APT41 (Operation ShadowPad India)
- **1.235.192.131** - APT36 (Operation Sindoor - Defense targeting)
- **2.57.121.15** - SideCopy (Operation SideCopy India)

### Most Dangerous (Score 95-100):
- **1.225.51.122** - Lazarus Group (100/100)
- **2.55.122.202** - APT29 Cozy Bear (96/100)
- **1.222.92.35** - APT41 (95/100)
- **1.235.192.131** - APT36 (95/100)

---

## 💡 Usage Tips

### For Quick Testing:
```bash
# Test single IP
curl http://localhost:5000/api/analyze -X POST \
  -H "Content-Type: application/json" \
  -d '{"ip":"1.222.92.35"}'
```

### For PDF Generation:
```bash
# Download PDF report
curl http://localhost:5000/api/download-report -X POST \
  -H "Content-Type: application/json" \
  -d '{"ip":"1.222.92.35"}' \
  --output apt41_report.pdf
```

### For Batch Analysis:
```bash
# Analyze all 10 IPs
python test_mock_database.py
```

---

## 🔍 What Each IP Demonstrates

| IP | Demonstrates |
|----|--------------|
| 1.222.92.35 | Multi-tactic APT, India targeting |
| 1.225.51.122 | Financial cybercrime, cryptocurrency threats |
| 1.235.192.131 | Defense/military espionage |
| 1.236.160.55 | Nation-state cyber warfare |
| 1.246.248.62 | Supply chain attacks, MSP targeting |
| 2.54.97.134 | Critical infrastructure sabotage |
| 2.55.64.191 | Diplomatic espionage |
| 2.55.85.196 | Academic/research targeting |
| 2.55.122.202 | Sophisticated supply chain compromise |
| 2.57.121.15 | Document theft, defense targeting |

---

## 📝 Notes

- All IPs return **real geolocation data** from IP-API
- MITRE intelligence is **mock data** (realistic but simulated)
- Threat scores are **automatically set to 90-100** (CRITICAL/HIGH)
- PDF reports include **complete MITRE ATT&CK mappings**
- **No API rate limits** - use as many times as needed

---

**Quick Start:** Just enter any of these IPs in your frontend and analyze! 🚀
