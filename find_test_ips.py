"""
Find IPs with Threat Intelligence
Queries AlienVault OTX to find IPs that have pulse data
"""
import sys
sys.path.insert(0, 'd:\\TICE hackthaon project')

from api.alienvault_otx import AlienVaultOTXClient
import time

def find_ips_with_intelligence():
    """Search for IPs that have threat intelligence"""
    
    print("=" * 80)
    print("SEARCHING FOR IPs WITH THREAT INTELLIGENCE")
    print("=" * 80)
    print()
    
    client = AlienVaultOTXClient()
    
    # Sample IPs from different ranges to test
    # These are randomly selected public IPs for testing
    test_ips = [
        # Some IPs that might have intelligence (random samples)
        "45.142.212.61",   # Known hosting range
        "185.220.101.1",   # Tor exit node range
        "91.219.236.197",  # Eastern Europe range
        "103.253.145.30",  # Asia Pacific range
        "194.135.33.150",  # Europe range
    ]
    
    found_ips = []
    
    print("Testing sample IPs for threat intelligence...\n")
    
    for ip in test_ips:
        print(f"Checking {ip}... ", end="", flush=True)
        
        try:
            result = client.check_ip(ip)
            
            if result.get('found') and result.get('pulse_count', 0) > 0:
                pulse_count = result.get('pulse_count', 0)
                threat_groups = result.get('threat_groups', [])
                
                print(f"✓ FOUND! Pulses: {pulse_count}", end="")
                if threat_groups:
                    print(f", Groups: {', '.join(threat_groups[:3])}")
                    found_ips.append({
                        'ip': ip,
                        'pulses': pulse_count,
                        'groups': threat_groups
                    })
                else:
                    print()
            else:
                print("✗ No intelligence")
            
            time.sleep(1)  # Be nice to the API
            
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    if found_ips:
        print(f"\n✓ Found {len(found_ips)} IP(s) with threat intelligence:\n")
        for item in found_ips:
            print(f"IP: {item['ip']}")
            print(f"  Pulses: {item['pulses']}")
            if item['groups']:
                print(f"  Threat Groups: {', '.join(item['groups'])}")
            print()
        
        print("=" * 80)
        print("RECOMMENDATION")
        print("=" * 80)
        print("\nTest these IPs in your TICE application:")
        for item in found_ips:
            print(f"  - {item['ip']}")
        print("\nThese should show the MITRE ATT&CK section in the PDF report!")
    else:
        print("\n✗ No IPs found with threat intelligence in this sample.")
        print("\nTry these alternatives:")
        print("  1. Visit https://otx.alienvault.com/browse/pulses/")
        print("  2. Search for recent threat pulses")
        print("  3. Extract IPs from pulses tagged with APT groups")
        print("  4. Visit https://threatfox.abuse.ch/browse/ for C2 servers")

if __name__ == '__main__':
    find_ips_with_intelligence()
