"""
Search for APT IPs from Pakistan and China using AlienVault OTX API
"""
import requests
from config import Config
import time

config = Config()
OTX_API_KEY = config.ALIENVAULT_OTX_API_KEY

BASE_URL = "https://otx.alienvault.com/api/v1"

headers = {
    'X-OTX-API-KEY': OTX_API_KEY,
    'User-Agent': 'TICE-Threat-Intelligence/1.0'
}

print("="*80)
print("🔍 SEARCHING FOR APT IPs - PAKISTAN & CHINA")
print("="*80)

# Pakistan APT search terms
pakistan_searches = [
    "Transparent Tribe",
    "APT36",
    "SideCopy", 
    "Bitter APT",
    "Pakistan APT"
]

# China APT search terms
china_searches = [
    "APT41",
    "APT10",
    "Mustang Panda",
    "Winnti",
    "APT15",
    "Earth Lusca",
    "APT27",
    "APT40",
    "Stone Panda",
    "China APT"
]

def search_otx_pulses(query, max_results=20):
    """Search OTX for pulses matching query"""
    try:
        url = f"{BASE_URL}/search/pulses"
        params = {
            'q': query,
            'limit': max_results,
            'sort': '-created'  # Most recent first
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        else:
            print(f"   ⚠️  Error {response.status_code} for query: {query}")
            return []
    except Exception as e:
        print(f"   ❌ Error searching {query}: {e}")
        return []

def extract_ips_from_pulses(pulses):
    """Extract IPv4 addresses from pulses"""
    ips = []
    for pulse in pulses:
        indicators = pulse.get('indicators', [])
        pulse_name = pulse.get('name', 'Unknown')
        created = pulse.get('created', '')[:10]
        
        for indicator in indicators:
            if indicator.get('type') == 'IPv4':
                ip = indicator.get('indicator')
                if ip:
                    ips.append({
                        'ip': ip,
                        'pulse_name': pulse_name,
                        'created': created,
                        'pulse_id': pulse.get('id', '')
                    })
    
    return ips

# Search for Pakistan APTs
print("\n" + "="*80)
print("🇵🇰 SEARCHING PAKISTAN APT IPs")
print("="*80)

pakistan_ips = []
for search_term in pakistan_searches:
    print(f"\n🔍 Searching: {search_term}")
    pulses = search_otx_pulses(search_term)
    print(f"   Found {len(pulses)} pulses")
    
    ips = extract_ips_from_pulses(pulses)
    pakistan_ips.extend(ips)
    print(f"   Extracted {len(ips)} IP addresses")
    
    time.sleep(1)  # Rate limiting

# Deduplicate Pakistan IPs
pakistan_unique = {}
for item in pakistan_ips:
    ip = item['ip']
    if ip not in pakistan_unique:
        pakistan_unique[ip] = item

print(f"\n✅ Total unique Pakistan IPs found: {len(pakistan_unique)}")

# Search for China APTs
print("\n" + "="*80)
print("🇨🇳 SEARCHING CHINA APT IPs")
print("="*80)

china_ips = []
for search_term in china_searches:
    print(f"\n🔍 Searching: {search_term}")
    pulses = search_otx_pulses(search_term)
    print(f"   Found {len(pulses)} pulses")
    
    ips = extract_ips_from_pulses(pulses)
    china_ips.extend(ips)
    print(f"   Extracted {len(ips)} IP addresses")
    
    time.sleep(1)  # Rate limiting

# Deduplicate China IPs
china_unique = {}
for item in china_ips:
    ip = item['ip']
    if ip not in china_unique:
        china_unique[ip] = item

print(f"\n✅ Total unique China IPs found: {len(china_unique)}")

# Save to files for verification
print("\n" + "="*80)
print("💾 SAVING CANDIDATE IPs")
print("="*80)

with open('pakistan_apt_candidates.txt', 'w') as f:
    f.write("PAKISTAN APT IP CANDIDATES\n")
    f.write("="*80 + "\n\n")
    for ip, data in pakistan_unique.items():
        f.write(f"{ip} | {data['pulse_name'][:60]} | {data['created']}\n")

print(f"✅ Saved {len(pakistan_unique)} Pakistan IPs to: pakistan_apt_candidates.txt")

with open('china_apt_candidates.txt', 'w') as f:
    f.write("CHINA APT IP CANDIDATES\n")
    f.write("="*80 + "\n\n")
    for ip, data in china_unique.items():
        f.write(f"{ip} | {data['pulse_name'][:60]} | {data['created']}\n")

print(f"✅ Saved {len(china_unique)} China IPs to: china_apt_candidates.txt")

# Export for verification script
import json

with open('pakistan_ips.json', 'w') as f:
    json.dump(list(pakistan_unique.keys()), f, indent=2)

with open('china_ips.json', 'w') as f:
    json.dump(list(china_unique.keys()), f, indent=2)

print("\n" + "="*80)
print("📊 SUMMARY")
print("="*80)
print(f"Pakistan candidate IPs: {len(pakistan_unique)}")
print(f"China candidate IPs: {len(china_unique)}")
print(f"\nNext step: Run verify_apt_ips.py to test each IP")
print("="*80)
