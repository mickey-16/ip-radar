"""
Debug AlienVault OTX Response for IP
Check what data we're actually getting
"""
import sys
sys.path.insert(0, 'd:\\TICE hackthaon project')

from api.alienvault_otx import AlienVaultOTXClient
import json

def debug_otx_response():
    """Debug what AlienVault OTX returns for the test IP"""
    
    test_ip = "45.142.212.61"
    
    print("=" * 80)
    print(f"DEBUGGING ALIENVAULT OTX RESPONSE FOR: {test_ip}")
    print("=" * 80)
    print()
    
    client = AlienVaultOTXClient()
    result = client.check_ip(test_ip)
    
    print("PARSED RESULT:")
    print(json.dumps(result, indent=2))
    
    print("\n" + "=" * 80)
    print("ANALYSIS:")
    print("=" * 80)
    print(f"Found: {result.get('found')}")
    print(f"Pulse Count: {result.get('pulse_count', 0)}")
    print(f"Threat Groups: {result.get('threat_groups', [])}")
    print(f"Has APT Link: {result.get('has_apt_link', False)}")
    print(f"Tags: {result.get('tags', [])[:10]}")  # First 10 tags
    
    if not result.get('threat_groups'):
        print("\n⚠️  PROBLEM: No specific threat group names extracted!")
        print("   Without group names like 'APT28', 'Lazarus', etc.,")
        print("   the MITRE scraper won't be triggered.")
        print("\n   Tags found:", ', '.join(result.get('tags', [])[:15]))

if __name__ == '__main__':
    debug_otx_response()
