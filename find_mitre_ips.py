"""
Find IPs that will DEFINITELY show MITRE intelligence
Strategy: Get IPs from specific APT group pulses with confirmed attribution
"""
import requests
from config import Config
import json
import time

config = Config()
OTX_API_KEY = config.ALIENVAULT_OTX_API_KEY
BASE_URL = "https://otx.alienvault.com/api/v1"

headers = {
    'X-OTX-API-KEY': OTX_API_KEY,
    'User-Agent': 'TICE-Threat-Intelligence/1.0'
}

print("="*80)
print("🎯 FINDING IPs WITH GUARANTEED APT ATTRIBUTION")
print("="*80)

# Known APT group MITRE IDs that our scraper can find
apt_groups_to_search = {
    'China': [
        'APT41',
        'Mustang Panda', 
        'APT10',
        'Winnti',
        'APT15',
        'APT27',
        'APT40',
        'Emissary Panda',
        'Stone Panda'
    ],
    'Pakistan': [
        'Transparent Tribe',
        'APT36',
        'SideCopy',
        'Bitter'
    ],
    'Iran': [  # Backup if Pakistan is limited
        'MuddyWater',
        'APT33',
        'APT34',
        'Static Kitten',
        'Charming Kitten'
    ]
}

def get_subscribed_pulses(page=1):
    """Get pulses with specific tags"""
    try:
        # Search for pulses with 'APT' tag sorted by most recent
        url = f"{BASE_URL}/pulses/subscribed"
        params = {
            'page': page,
            'limit': 20
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            return response.json().get('results', [])
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def search_pulses_by_tag(tag):
    """Search for pulses by specific tag"""
    try:
        url = f"{BASE_URL}/search/pulses"
        params = {
            'q': f'tag:{tag}',
            'limit': 10,
            'sort': '-created'
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            return response.json().get('results', [])
        return []
    except Exception as e:
        return []

def get_pulse_details(pulse_id):
    """Get full details of a specific pulse including all indicators"""
    try:
        url = f"{BASE_URL}/pulses/{pulse_id}"
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

def extract_ipv4_from_pulse(pulse):
    """Extract all IPv4 addresses from pulse"""
    ips = []
    indicators = pulse.get('indicators', [])
    
    for ind in indicators:
        if ind.get('type') == 'IPv4':
            ips.append(ind.get('indicator'))
    
    return ips

# Collect IPs by searching for each APT group
all_ips = {'China': {}, 'Pakistan': {}, 'Iran': {}}

for country, apt_groups in apt_groups_to_search.items():
    print(f"\n{'='*80}")
    print(f"🔍 Searching {country} APT Groups")
    print(f"{'='*80}")
    
    for apt_name in apt_groups:
        print(f"\n📡 Searching: {apt_name}")
        
        # Search for pulses with this APT group name
        pulses = search_pulses_by_tag(apt_name)
        
        if not pulses:
            # Try searching in title/description
            try:
                url = f"{BASE_URL}/search/pulses"
                params = {'q': apt_name, 'limit': 5, 'sort': '-created'}
                response = requests.get(url, headers=headers, params=params, timeout=15)
                if response.status_code == 200:
                    pulses = response.json().get('results', [])
            except:
                pass
        
        print(f"   Found {len(pulses)} pulses")
        
        # Get IPs from each pulse
        for pulse in pulses[:3]:  # Limit to top 3 most recent
            pulse_id = pulse.get('id')
            pulse_name = pulse.get('name', '')
            
            # Get full pulse details
            full_pulse = get_pulse_details(pulse_id)
            if full_pulse:
                ips = extract_ipv4_from_pulse(full_pulse)
                
                for ip in ips[:5]:  # Max 5 IPs per pulse
                    if ip not in all_ips[country]:
                        all_ips[country][ip] = {
                            'apt_group': apt_name,
                            'pulse_name': pulse_name,
                            'pulse_id': pulse_id
                        }
                
                if ips:
                    print(f"   ✅ Extracted {len(ips[:5])} IPs from: {pulse_name[:60]}")
            
            time.sleep(0.5)  # Rate limiting
        
        time.sleep(1)  # Rate limiting between APT groups

# Save results
print(f"\n{'='*80}")
print("💾 SAVING RESULTS")
print(f"{'='*80}")

for country, ips in all_ips.items():
    print(f"\n{country}: {len(ips)} candidate IPs found")
    
    if ips:
        filename = f"{country.lower()}_apt_ips_verified.json"
        with open(filename, 'w') as f:
            json.dump(ips, f, indent=2)
        print(f"   ✅ Saved to: {filename}")
        
        # Also save simple list
        with open(f"{country.lower()}_ips_list.txt", 'w') as f:
            for ip, data in ips.items():
                f.write(f"{ip} | {data['apt_group']} | {data['pulse_name'][:50]}\n")

print(f"\n{'='*80}")
print("📊 SUMMARY")
print(f"{'='*80}")
print(f"China IPs: {len(all_ips['China'])}")
print(f"Pakistan IPs: {len(all_ips['Pakistan'])}")
print(f"Iran IPs: {len(all_ips['Iran'])} (backup)")
print(f"\nNext: Run verify script to test with MITRE system")
print(f"{'='*80}")
