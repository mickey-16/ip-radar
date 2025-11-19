"""
Debug why Cloudflare DNS scoring isn't being capped
"""
from core.correlator import ThreatCorrelator
from config import Config

ip = "1.1.1.1"

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
profile = correlator.analyze_ip(ip, use_cache=False)

print(f"IP: {ip}")
print(f"Final Score: {profile.threat_score}")
print(f"\nSource Scores:")
for source, score in profile.source_scores.items():
    print(f"  {source}: {score}")

# Check whitelist
abuse_data = profile.sources.get('abuseipdb', {}).get('data', {})
is_whitelisted = abuse_data.get('isWhitelisted', False)
print(f"\nWhitelisted: {is_whitelisted}")

# Check MITRE
mitre = profile.mitre_intelligence
has_apt = mitre.get('has_apt_attribution', False)
apt_count = len(mitre.get('threat_actors', []))
print(f"Has APT: {has_apt}, APT Count: {apt_count}")

# Manual calculation
weights = {'abuseipdb': 0.30, 'virustotal': 0.25, 'ipgeolocation': 0.20, 'greynoise': 0.15, 'shodan': 0.10}
total_score = 0
total_weight = 0
for source, weight in weights.items():
    if source in profile.source_scores:
        score = profile.source_scores[source]
        total_score += score * weight
        total_weight += weight
        print(f"  {source}: {score} * {weight} = {score * weight}")

weighted_avg = total_score / total_weight if total_weight > 0 else 0
print(f"\nWeighted Average: {weighted_avg}")
print(f"Should be capped at: 5 (for whitelisted IPs)")
print(f"Actual final score: {profile.threat_score}")
