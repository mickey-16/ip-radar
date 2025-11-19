"""
VirusTotal API Integration
API Documentation: https://developers.virustotal.com/reference/overview
"""
import requests
from typing import Dict, Optional
import time

class VirusTotalClient:
    """
    Client for VirusTotal API v3
    Free tier: 500 requests per day, 4 requests per minute
    """
    
    BASE_URL = 'https://www.virustotal.com/api/v3'
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'x-apikey': api_key,
            'Accept': 'application/json'
        }
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Implement rate limiting (4 requests per minute)"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < 15:  # 15 seconds between requests
            time.sleep(15 - time_since_last)
        
        self.last_request_time = time.time()
    
    def check_ip(self, ip_address: str) -> Optional[Dict]:
        """
        Get IP address report
        
        Args:
            ip_address: IP address to check
            
        Returns:
            Dict containing API response or None on error
        """
        if not self.api_key:
            return None
        
        self._rate_limit()
        
        endpoint = f"{self.BASE_URL}/ip_addresses/{ip_address}"
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("VirusTotal: Rate limit exceeded")
                return None
            elif response.status_code == 404:
                print(f"VirusTotal: IP {ip_address} not found in database")
                return None
            else:
                print(f"VirusTotal API error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"VirusTotal request error: {e}")
            return None
    
    def parse_response(self, response: Dict) -> Dict:
        """
        Parse VirusTotal response into normalized format
        
        Args:
            response: Raw API response
            
        Returns:
            Normalized data dictionary
        """
        if not response or 'data' not in response:
            return {}
        
        data = response['data']
        attributes = data.get('attributes', {})
        stats = attributes.get('last_analysis_stats', {})
        
        # Calculate threat score from detection stats
        total_engines = sum(stats.values())
        malicious = stats.get('malicious', 0)
        suspicious = stats.get('suspicious', 0)
        
        detection_rate = 0
        if total_engines > 0:
            detection_rate = ((malicious + suspicious * 0.5) / total_engines) * 100
        
        return {
            'source': 'VirusTotal',
            'is_malicious': malicious > 0,
            'detection_rate': round(detection_rate, 2),
            'malicious_count': malicious,
            'suspicious_count': suspicious,
            'harmless_count': stats.get('harmless', 0),
            'undetected_count': stats.get('undetected', 0),
            'total_engines': total_engines,
            'reputation': attributes.get('reputation', 0),
            'country': attributes.get('country'),
            'asn': attributes.get('asn'),
            'as_owner': attributes.get('as_owner'),
            'network': attributes.get('network'),
            'categories': self._extract_categories(attributes),
            'raw_data': response
        }
    
    def _extract_categories(self, attributes: Dict) -> list:
        """Extract threat categories from attributes"""
        categories = []
        
        # Check last analysis results for common threats
        results = attributes.get('last_analysis_results', {})
        
        threat_keywords = {
            'malware': 'Malware',
            'trojan': 'Trojan',
            'botnet': 'Botnet',
            'phishing': 'Phishing',
            'spam': 'Spam',
            'c2': 'C2',
            'ransomware': 'Ransomware'
        }
        
        for engine_result in results.values():
            category = engine_result.get('category', '').lower()
            result = engine_result.get('result', '').lower()
            
            for keyword, threat_type in threat_keywords.items():
                if keyword in category or keyword in result:
                    if threat_type not in categories:
                        categories.append(threat_type)
        
        return categories
