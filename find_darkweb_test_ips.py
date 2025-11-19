"""
Find test IPs for dark web intelligence feature
"""
import requests
import json

print("🔍 Finding IPs to test Dark Web Intelligence...\n")

# 1. Get some Tor exit nodes
print("=" * 60)
print("1. TOR EXIT NODES (from official Tor Project list)")
print("=" * 60)
try:
    response = requests.get('https://check.torproject.org/torbulkexitlist', timeout=10)
    tor_ips = [ip.strip() for ip in response.text.split('\n') if ip.strip() and not ip.startswith('#')]
    print(f"✅ Found {len(tor_ips)} Tor exit nodes")
    print("\nFirst 10 Tor Exit Node IPs to test:")
    for i, ip in enumerate(tor_ips[:10], 1):
        print(f"   {i}. {ip}")
except Exception as e:
    print(f"❌ Error fetching Tor list: {e}")

print("\n" + "=" * 60)
print("2. MALWARE DISTRIBUTION IPs (from URLhaus)")
print("=" * 60)
try:
    # Get recent malware URLs from URLhaus
    response = requests.post(
        'https://urlhaus-api.abuse.ch/v1/urls/recent/',
        timeout=10
    )
    data = response.json()
    
    if data.get('query_status') == 'ok':
        urls = data.get('urls', [])[:20]
        malware_ips = set()
        
        for url_data in urls:
            host = url_data.get('url_status')
            # Try to extract IPs from URLs
            if url_data.get('host'):
                host_val = url_data.get('host')
                # Check if host is an IP address
                parts = host_val.split('.')
                if len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts):
                    malware_ips.add(host_val)
        
        if malware_ips:
            print(f"✅ Found {len(malware_ips)} IPs hosting malware")
            print("\nMalware Distribution IPs to test:")
            for i, ip in enumerate(list(malware_ips)[:10], 1):
                print(f"   {i}. {ip}")
        else:
            print("⚠️  No direct IP-based malware URLs found in recent data")
            print("   (Most malware uses domain names, not direct IPs)")
    else:
        print(f"❌ URLhaus returned: {data.get('query_status')}")
except Exception as e:
    print(f"❌ Error fetching URLhaus data: {e}")

print("\n" + "=" * 60)
print("3. RECOMMENDED TEST IPs")
print("=" * 60)
print("\n📋 Use these IPs to test the dark web feature:\n")

# Print tor IPs if we got them
if 'tor_ips' in locals() and tor_ips:
    print("✅ TOR EXIT NODE (will trigger dark web alert):")
    print(f"   → {tor_ips[0]}")
    print(f"   → {tor_ips[1] if len(tor_ips) > 1 else 'N/A'}")
    print(f"   → {tor_ips[2] if len(tor_ips) > 2 else 'N/A'}")

print("\n✅ SAFE/CLEAN IP (no dark web activity):")
print("   → 8.8.8.8 (Google DNS)")
print("   → 1.1.1.1 (Cloudflare DNS)")

print("\n✅ OUR MOCK APT IPs (should show MITRE + possibly dark web):")
print("   → 185.220.101.1 (Mock APT41)")
print("   → 117.14.157.213 (Mock Lazarus)")
print("   → 45.142.212.61 (Mock APT28)")

print("\n" + "=" * 60)
print("💡 TESTING TIPS")
print("=" * 60)
print("""
1. Start with Tor exit node IPs - guaranteed dark web detection
2. Test with Google DNS (8.8.8.8) - should show NO dark web activity
3. Try mock APT IPs - will show MITRE intelligence + maybe dark web
4. Check the frontend UI for the 🕵️ Dark Web Intelligence card
5. Download PDF to see dark web section in the report

Expected Results:
- Tor IPs: Shows "ACTIVITY DETECTED" badge, Tor exit node warning
- Google DNS: Shows "NO ACTIVITY" badge with green checkmark
- Mock APTs: Shows MITRE data, may or may not show dark web activity
""")

print("\n🎯 QUICK TEST COMMAND:")
print("=" * 60)
if 'tor_ips' in locals() and tor_ips:
    print(f"python -c \"from api.darkweb_intel import DarkWebIntelligence; dw = DarkWebIntelligence(); print(dw.check_ip('{tor_ips[0]}'))\"")
else:
    print("# Tor list not available, test with a known IP manually")

print("\n✅ Test setup complete! Use the IPs above in the frontend.\n")
