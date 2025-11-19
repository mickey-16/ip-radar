# 🛡 TICE - Threat Intelligence Correlation Engine

> An AI-powered threat intelligence platform that aggregates, normalizes, and correlates data from multiple threat intelligence sources to provide comprehensive IP reputation analysis.

## 🎯 Overview

*TICE (Threat Intelligence Correlation Engine)* is a comprehensive cybersecurity tool designed to help investigators and security analysts quickly assess the threat level of IP addresses by automatically querying multiple threat intelligence sources and providing a unified, actionable report.

## 🚨 Problem Statement

Cybercrime investigators face significant challenges:
- *Fragmented Data*: Threat intelligence is scattered across multiple sources
- *Manual Verification*: Time-consuming process to check each IP across different platforms
- *Inconsistent Formats*: Each API provides data in different structures
- *No Unified View*: Difficult to get a comprehensive threat assessment quickly

## ✨ Features

### Core Functionality
- 🔍 *Multi-Source Intelligence*: Queries 5+ threat intelligence APIs simultaneously
- 🔄 *Data Normalization*: Standardizes disparate data formats into unified profiles
- 📊 *Threat Scoring*: Advanced algorithm that calculates risk scores (0-100)
- 🎯 *Threat Attribution*: Identifies threat categories (botnet, C2, phishing, spam, proxy)
- 🌍 *Geolocation & ASN*: Detailed geographic and network information
- 🔗 *Related Entities*: Discovers linked domains, URLs, and malware samples

### User Interface
- 📱 *Web Dashboard*: Intuitive, responsive interface
- 📈 *Visual Analytics*: Charts and graphs for threat data
- 📄 *Detailed Reports*: Comprehensive threat attribution reports
- 💾 *Export Options*: Download results in JSON/PDF format
- 🚀 *Real-time Analysis*: Instant results from multiple sources

## 🏗 Architecture


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


## 🔌 API Integrations

### Supported Threat Intelligence Sources

| Service          | Free Tier | Rate Limit  | Features |
|------------------|-----------|------------ |----------------------------------|
| *AbuseIPDB*      | ✅ Yes    | 1,000/day   | Abuse reports, confidence score  |
| *VirusTotal*     | ✅ Yes    | 500/day     | Malware detection, URL scanning  |
| *IPQualityScore* | ✅ Yes    | 5,000/month | Proxy/VPN detection, fraud score |
| *Shodan*         | ⚠ Limited | 100/month   | Port scanning, service detection |
| *GreyNoise*      | ✅ Yes    | 5,000/day   | Internet scanner classification  |
| *IPGeolocation*  | ✅ Yes    | 1,000/day   | Geolocation, ASN information     
|

### Getting API Keys

1. *AbuseIPDB*: https://www.abuseipdb.com/api
2. *VirusTotal*: https://www.virustotal.com/gui/join-us
3. *IPQualityScore*: https://www.ipqualityscore.com/create-account
4. *Shodan*: https://account.shodan.io/register
5. *GreyNoise*: https://www.greynoise.io/signup
6. *IPGeolocation*: https://ipgeolocation.io/signup

## 🧮 Threat Scoring Algorithm

Our proprietary scoring algorithm combines multiple factors:

### Scoring Components
python
Final Score = (
    AbuseIPDB_Score × 0.30 +
    VirusTotal_Score × 0.25 +
    IPQS_Score × 0.20 +
    GreyNoise_Score × 0.15 +
    Shodan_Score × 0.10
)


### Risk Levels
- *0-20*: 🟢 Low Risk (Benign)
- *21-50*: 🟡 Medium Risk (Suspicious)
- *51-75*: 🟠 High Risk (Likely Malicious)
- *76-100*: 🔴 Critical Risk (Confirmed Malicious)

### Threat Categories
- *Botnet*: Part of a botnet network
- *C2 (Command & Control)*: C2 server infrastructure
- *Phishing*: Hosting phishing sites
- *Spam*: Email spam source
- *Proxy/VPN*: Anonymous proxy or VPN exit node
- *Malware*: Malware distribution
- *Scanner*: Port/vulnerability scanner
