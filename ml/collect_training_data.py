"""
Training Data Collection Script
Analyzes IPs and builds dataset for ML model training
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pandas as pd
from pathlib import Path
from core.correlator import ThreatCorrelator
from config import config
import time

# Known IP lists for balanced dataset
MALICIOUS_IPS = [
    "144.31.194.33",  # Spam/Phishing
    "183.166.137.160",  # Web Spam
    "206.168.34.44",  # Phishing/Malware
    "185.220.101.1",  # Tor Exit Node
    "45.142.214.48",  # Known malware C2
    "89.248.165.137",  # Botnet
    "91.92.109.43",  # SSH Brute Force
    "192.42.116.16",  # Tor Relay
    "23.129.64.143",  # Phishing host
    "104.168.155.129"  # Malware distribution
]

BENIGN_IPS = [
    "8.8.8.8",  # Google DNS
    "1.1.1.1",  # Cloudflare DNS
    "208.67.222.222",  # OpenDNS
    "149.112.112.112",  # Quad9 DNS
    "4.2.2.2",  # Level3 DNS
    "76.76.19.19",  # Alternate DNS
    "185.228.168.9",  # CleanBrowsing DNS
    "94.140.14.14",  # AdGuard DNS
    "216.239.32.10",  # Google (another)
    "64.6.64.6"  # Verisign DNS
]

def extract_features(threat_profile):
    """Extract ML features from ThreatProfile"""
    data = threat_profile.to_dict()
    
    # Extract features
    features = {
        # Target variable
        'threat_score': data['threat_score'],
        'is_malicious': data['is_malicious'],
        
        # Geolocation features
        'country_code': data['geolocation'].get('country_code', 'UNKNOWN'),
        'country': data['geolocation'].get('country', 'UNKNOWN'),
        
        # Network features
        'is_hosting': data['network_info'].get('is_hosting', False),
        'is_vpn': data['network_info'].get('is_vpn', False),
        'is_proxy': data['network_info'].get('is_proxy', False),
        'is_tor': data['network_info'].get('is_tor', False),
        'isp': data['network_info'].get('isp', 'UNKNOWN'),
        'organization': data['network_info'].get('organization', 'UNKNOWN'),
        
        # ASN
        'asn': data['network_info'].get('asn', 'UNKNOWN'),
        
        # Source scores
        'abuseipdb_score': data['source_scores'].get('abuseipdb', 0),
        'virustotal_score': data['source_scores'].get('virustotal', 0),
        'ipapi_score': data['source_scores'].get('ipapi', 0),
        
        # Categories (count)
        'num_categories': len(data.get('categories', [])),
        'categories': ','.join(data.get('categories', [])),
        
        # Reports
        'reports_count': data.get('reports_count', 0),
        'confidence': data['confidence'],
        'risk_level': data['risk_level']
    }
    
    return features

def collect_data():
    """Collect training data from both cached and live IPs"""
    print("=" * 60)
    print("🤖 ML Training Data Collection")
    print("=" * 60)
    
    # Initialize correlator
    correlator = ThreatCorrelator(config['development'])
    
    all_features = []
    
    # Collect from malicious IPs
    print(f"\n📊 Analyzing {len(MALICIOUS_IPS)} known malicious IPs...")
    for idx, ip in enumerate(MALICIOUS_IPS, 1):
        try:
            print(f"  [{idx}/{len(MALICIOUS_IPS)}] {ip}...", end=" ")
            profile = correlator.analyze_ip(ip, use_cache=True)
            features = extract_features(profile)
            features['label'] = 'malicious'
            features['ip_address'] = ip
            all_features.append(features)
            print(f"✓ Score: {features['threat_score']}")
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Collect from benign IPs
    print(f"\n📊 Analyzing {len(BENIGN_IPS)} known benign IPs...")
    for idx, ip in enumerate(BENIGN_IPS, 1):
        try:
            print(f"  [{idx}/{len(BENIGN_IPS)}] {ip}...", end=" ")
            profile = correlator.analyze_ip(ip, use_cache=True)
            features = extract_features(profile)
            features['label'] = 'benign'
            features['ip_address'] = ip
            all_features.append(features)
            print(f"✓ Score: {features['threat_score']}")
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Create DataFrame
    df = pd.DataFrame(all_features)
    
    # Save to CSV
    output_file = Path(__file__).parent / 'training_data.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✅ Training data saved: {output_file}")
    print(f"📊 Total samples: {len(df)}")
    print(f"   - Malicious: {len(df[df['label'] == 'malicious'])}")
    print(f"   - Benign: {len(df[df['label'] == 'benign'])}")
    print(f"\n📈 Threat Score Distribution:")
    print(df.groupby('label')['threat_score'].describe())
    
    return df

if __name__ == '__main__':
    collect_data()
