"""
Verify which IPs will show MITRE intelligence in PDF
Tests each IP and keeps only those with APT attribution
"""
from core.correlator import ThreatCorrelator
from config import Config
import json
import time

print("="*80)
print("🧪 VERIFYING IPs FOR MITRE INTELLIGENCE")
print("="*80)

config = Config()
config_dict = {
    'ABUSEIPDB_API_KEY': config.ABUSEIPDB_API_KEY,
    'VIRUSTOTAL_API_KEY': config.VIRUSTOTAL_API_KEY,
    'IPQUALITYSCORE_API_KEY': config.IPQUALITYSCORE_API_KEY,
    'SHODAN_API_KEY': config.SHODAN_API_KEY,
    'ALIENVAULT_OTX_API_KEY': config.ALIENVAULT_OTX_API_KEY,
    'SCORING_WEIGHTS': {}
}

correlator = ThreatCorrelator(config_dict)

# Load candidate IPs
countries = ['china', 'pakistan', 'iran']
verified_ips = {'china': [], 'pakistan': [], 'iran': []}

for country in countries:
    print(f"\n{'='*80}")
    print(f"🔍 Testing {country.upper()} IPs")
    print(f"{'='*80}")
    
    try:
        with open(f'{country}_apt_ips_verified.json', 'r') as f:
            candidates = json.load(f)
    except:
        print(f"   ⚠️  No candidates found for {country}")
        continue
    
    for ip, metadata in candidates.items():
        print(f"\n📡 Testing: {ip} ({metadata['apt_group']})")
        
        try:
            # Analyze IP
            profile = correlator.analyze_ip(ip, use_cache=False)
            
            # Check MITRE intelligence
            mitre = profile.mitre_intelligence
            has_apt = len(mitre.get('threat_actors', [])) > 0
            has_malware = len(mitre.get('malware_families', [])) > 0
            is_c2 = mitre.get('is_c2_server', False)
            
            # Check if will show in PDF
            will_show_mitre = has_apt or has_malware or is_c2
            
            print(f"   Score: {profile.threat_score:.1f}")
            print(f"   Risk: {profile.risk_level.upper()}")
            print(f"   APT Groups: {len(mitre.get('threat_actors', []))}")
            print(f"   Malware: {len(mitre.get('malware_families', []))}")
            print(f"   OTX Pulses: {mitre.get('otx_pulse_count', 0)}")
            print(f"   Confidence: {mitre.get('confidence', 'NONE')}")
            
            if will_show_mitre:
                print(f"   ✅ WILL SHOW MITRE SECTION IN PDF")
                
                # Get APT group names
                apt_groups = [actor.get('name') for actor in mitre.get('threat_actors', [])]
                attribution = mitre.get('threat_actors', [{}])[0].get('attribution', 'Unknown') if apt_groups else 'Unknown'
                
                verified_ips[country].append({
                    'ip': ip,
                    'score': profile.threat_score,
                    'risk': profile.risk_level,
                    'apt_groups': apt_groups,
                    'attribution': attribution,
                    'malware_count': len(mitre.get('malware_families', [])),
                    'otx_pulses': mitre.get('otx_pulse_count', 0),
                    'confidence': mitre.get('confidence', 'NONE'),
                    'original_metadata': metadata
                })
            else:
                print(f"   ❌ NO MITRE SECTION (no APT/malware/C2)")
            
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"   ❌ Error testing IP: {e}")
            continue

# Save verified results
print(f"\n{'='*80}")
print("💾 SAVING VERIFIED IPs")
print(f"{'='*80}")

for country, ips in verified_ips.items():
    if ips:
        # Save JSON
        filename = f"VERIFIED_{country.upper()}_APT_IPs.json"
        with open(filename, 'w') as f:
            json.dump(ips, f, indent=2)
        print(f"\n{country.upper()}: {len(ips)} verified IPs")
        print(f"   ✅ Saved to: {filename}")
        
        # Print summary
        for ip_data in ips:
            apt_str = ', '.join(ip_data['apt_groups'][:2]) if ip_data['apt_groups'] else 'No APT'
            print(f"   • {ip_data['ip']} - {apt_str} ({ip_data['attribution']}) - Score: {ip_data['score']:.0f}")

print(f"\n{'='*80}")
print("📊 FINAL SUMMARY")
print(f"{'='*80}")
print(f"China IPs with MITRE: {len(verified_ips['china'])}")
print(f"Pakistan IPs with MITRE: {len(verified_ips['pakistan'])}")
print(f"Iran IPs with MITRE: {len(verified_ips['iran'])}")
print(f"\n🎯 Need 10 from each country - will search for more if needed")
print(f"{'='*80}")
