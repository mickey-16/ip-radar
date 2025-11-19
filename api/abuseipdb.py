"""
AbuseIPDB API Integration
API Documentation: https://docs.abuseipdb.com/
"""
import requests
from typing import Dict, Optional

class AbuseIPDBClient:
    """
    Client for AbuseIPDB API
    Free tier: 1,000 requests per day
    """
    
    BASE_URL = 'https://api.abuseipdb.com/api/v2'
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'Key': api_key,
            'Accept': 'application/json'
        }
    
    def check_ip(self, ip_address: str, max_age_days: int = 90) -> Optional[Dict]:
        """
        Check IP address reputation
        
        Args:
            ip_address: IP address to check
            max_age_days: Maximum age of reports to include
            
        Returns:
            Dict containing API response or None on error
        """
        if not self.api_key:
            return None
        
        endpoint = f"{self.BASE_URL}/check"
        params = {
            'ipAddress': ip_address,
            'maxAgeInDays': max_age_days,
            'verbose': True
        }
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("AbuseIPDB: Rate limit exceeded")
                return None
            else:
                print(f"AbuseIPDB API error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"AbuseIPDB request error: {e}")
            return None
    
    def parse_response(self, response: Dict) -> Dict:
        """
        Parse AbuseIPDB response into normalized format
        
        Args:
            response: Raw API response
            
        Returns:
            Normalized data dictionary
        """
        if not response or 'data' not in response:
            return {}
        
        data = response['data']
        confidence_score = data.get('abuseConfidenceScore', 0)
        is_whitelisted = data.get('isWhitelisted', False)
        
        return {
            'source': 'AbuseIPDB',
            'is_malicious': confidence_score > 50,
            'confidence_score': confidence_score,
            'total_reports': data.get('totalReports', 0),
            'last_reported': data.get('lastReportedAt'),
            'is_public': data.get('isPublic', False),
            'is_whitelisted': is_whitelisted,
            'usage_type': data.get('usageType'),
            'isp': data.get('isp'),
            'domain': data.get('domain'),
            'country_code': data.get('countryCode'),
            'categories': self._parse_categories(data.get('reports', []), confidence_score, is_whitelisted),
            'raw_data': response
        }
    
    def _parse_categories(self, reports: list, confidence_score: int = 0, is_whitelisted: bool = False) -> list:
        """
        Parse abuse categories from reports
        
        Args:
            reports: List of abuse reports
            confidence_score: AbuseIPDB confidence score (0-100)
            is_whitelisted: Whether the IP is whitelisted
            
        Returns:
            List of abuse categories
        """
        # Don't extract categories from whitelisted IPs or very low confidence scores
        # These are likely false positives or test reports
        if is_whitelisted or confidence_score < 10:
            return []
        
        category_map = {
            3: 'Fraud',
            4: 'DDoS',
            9: 'Hacking',
            10: 'Spam',
            14: 'Port Scan',
            15: 'Brute Force',
            18: 'Web Spam',
            19: 'Email Spam',
            20: 'SSH Brute Force',
            21: 'Web App Attack',
            22: 'Botnet',
            23: 'Exploited Host'
        }
        
        categories = set()
        for report in reports:
            for cat_id in report.get('categories', []):
                if cat_id in category_map:
                    categories.add(category_map[cat_id])
        
        return list(categories)
