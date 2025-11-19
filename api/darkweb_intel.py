"""
Dark Web Intelligence Module
Safely checks for dark web activity using legitimate public APIs
No Tor access required - 100% legal and safe
"""
import requests
import json
from typing import Dict, Optional
from datetime import datetime


class DarkWebIntelligence:
    """
    Safe dark web intelligence gathering using public APIs
    - Tor exit node detection
    - Breach database checking
    - Malware URL tracking
    """
    
    def __init__(self, hibp_api_key: str = None):
        """
        Initialize dark web intelligence client
        
        Args:
            hibp_api_key: Have I Been Pwned API key (optional for free tier)
        """
        self.hibp_api_key = hibp_api_key
        self.tor_exit_nodes = []
        self.cache_timeout = 3600  # 1 hour
        
    def check_ip(self, ip_address: str) -> Dict:
        """
        Comprehensive dark web intelligence check
        
        Args:
            ip_address: IP address to investigate
            
        Returns:
            Dictionary with dark web intelligence
        """
        print(f"🕵️ Checking dark web intelligence for {ip_address}...")
        
        results = {
            'found_in_darkweb': False,
            'tor_exit_node': False,
            'breach_activity': {
                'found': False,
                'breach_count': 0,
                'breaches': []
            },
            'malware_urls': {
                'found': False,
                'url_count': 0,
                'urls': []
            },
            'threat_level': 'none',
            'indicators': []
        }
        
        # Check 1: Tor Exit Node
        try:
            tor_result = self._check_tor_exit_node(ip_address)
            results['tor_exit_node'] = tor_result['is_tor_exit']
            if tor_result['is_tor_exit']:
                results['found_in_darkweb'] = True
                results['indicators'].append('Tor Exit Node')
                results['tor_details'] = tor_result
        except Exception as e:
            print(f"⚠️ Tor check failed: {e}")
        
        # Check 2: URLhaus Malware URLs
        try:
            malware_result = self._check_urlhaus(ip_address)
            if malware_result['found']:
                results['found_in_darkweb'] = True
                results['malware_urls'] = malware_result
                results['indicators'].append(f"{malware_result['url_count']} Malware URLs")
        except Exception as e:
            print(f"⚠️ URLhaus check failed: {e}")
        
        # Check 3: Breach Intelligence (if API key provided)
        if self.hibp_api_key:
            try:
                breach_result = self._check_breaches(ip_address)
                if breach_result['found']:
                    results['breach_activity'] = breach_result
                    results['indicators'].append(f"{breach_result['breach_count']} Data Breaches")
            except Exception as e:
                print(f"⚠️ Breach check failed: {e}")
        
        # Determine threat level
        results['threat_level'] = self._calculate_darkweb_threat(results)
        
        return results
    
    def _check_tor_exit_node(self, ip_address: str) -> Dict:
        """
        Check if IP is a Tor exit node
        Uses public Tor exit node list
        """
        # Tor Project's official exit node list
        tor_list_url = "https://check.torproject.org/torbulkexitlist"
        
        try:
            response = requests.get(tor_list_url, timeout=10)
            if response.status_code == 200:
                exit_nodes = response.text.strip().split('\n')
                # Filter out comments
                exit_nodes = [node for node in exit_nodes if not node.startswith('#')]
                
                is_tor = ip_address in exit_nodes
                
                return {
                    'is_tor_exit': is_tor,
                    'node_count': len(exit_nodes),
                    'last_updated': datetime.utcnow().isoformat() + 'Z',
                    'source': 'Tor Project Official List'
                }
        except Exception as e:
            print(f"Tor check error: {e}")
        
        return {
            'is_tor_exit': False,
            'error': str(e) if 'e' in locals() else 'Unknown error'
        }
    
    def _check_urlhaus(self, ip_address: str) -> Dict:
        """
        Check URLhaus for malware URLs hosted on this IP
        URLhaus is a free malware URL database by abuse.ch
        """
        api_url = "https://urlhaus-api.abuse.ch/v1/host/"
        
        try:
            response = requests.post(
                api_url,
                data={'host': ip_address},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('query_status') == 'ok':
                    urls = data.get('urls', [])
                    
                    # Extract relevant info
                    malware_urls = []
                    for url_data in urls[:10]:  # Limit to 10 most recent
                        malware_urls.append({
                            'url': url_data.get('url', 'N/A'),
                            'threat': url_data.get('threat', 'Unknown'),
                            'date_added': url_data.get('date_added', 'N/A'),
                            'status': url_data.get('url_status', 'Unknown'),
                            'tags': url_data.get('tags', [])
                        })
                    
                    return {
                        'found': len(urls) > 0,
                        'url_count': len(urls),
                        'urls': malware_urls,
                        'source': 'URLhaus (abuse.ch)'
                    }
        except Exception as e:
            print(f"URLhaus error: {e}")
        
        return {
            'found': False,
            'url_count': 0,
            'urls': []
        }
    
    def _check_breaches(self, ip_address: str) -> Dict:
        """
        Check Have I Been Pwned for breach activity
        Note: HIBP doesn't directly search by IP, but we can check associated domains
        """
        # Note: HIBP primarily works with emails/domains, not IPs directly
        # For demo purposes, we'll mark this as a placeholder
        # In production, you'd reverse DNS lookup and check domains
        
        return {
            'found': False,
            'breach_count': 0,
            'breaches': [],
            'note': 'Breach checking requires reverse DNS lookup (future enhancement)'
        }
    
    def _calculate_darkweb_threat(self, results: Dict) -> str:
        """
        Calculate overall dark web threat level
        """
        score = 0
        
        if results['tor_exit_node']:
            score += 30  # Tor exit nodes are suspicious but not always malicious
        
        if results['malware_urls']['found']:
            score += 50  # Malware hosting is critical
            score += min(results['malware_urls']['url_count'] * 5, 20)  # +5 per URL, max +20
        
        if results['breach_activity']['found']:
            score += 40  # Breach activity is serious
        
        if score == 0:
            return 'none'
        elif score < 30:
            return 'low'
        elif score < 60:
            return 'medium'
        elif score < 80:
            return 'high'
        else:
            return 'critical'
    
    def to_summary(self, results: Dict) -> str:
        """
        Generate human-readable summary
        """
        if not results['found_in_darkweb']:
            return "✅ No dark web activity detected"
        
        summary = "🕵️ Dark Web Activity Detected:\n"
        
        for indicator in results['indicators']:
            summary += f"  - {indicator}\n"
        
        return summary


# Convenience function
def check_darkweb_activity(ip_address: str, hibp_api_key: str = None) -> Dict:
    """
    Quick function to check dark web activity
    """
    client = DarkWebIntelligence(hibp_api_key)
    return client.check_ip(ip_address)
