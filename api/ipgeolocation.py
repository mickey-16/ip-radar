"""
IPGeolocation API Integration
API Documentation: https://ipgeolocation.io/documentation.html
"""
import requests
from typing import Dict, Optional

class IPGeolocationClient:
    """
    Client for IPGeolocation API
    Free tier: 1,000 requests per day
    """
    
    BASE_URL = 'https://api.ipgeolocation.io/ipgeo'
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def check_ip(self, ip_address: str) -> Optional[Dict]:
        """
        Get IP geolocation and security information
        
        Args:
            ip_address: IP address to check
            
        Returns:
            Dict containing API response or None on error
        """
        if not self.api_key:
            return None
        
        params = {
            'apiKey': self.api_key,
            'ip': ip_address,
            'fields': 'geo,security'
        }
        
        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print("IPGeolocation: Rate limit exceeded")
                return None
            else:
                print(f"IPGeolocation API error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"IPGeolocation request error: {e}")
            return None
    
    def parse_response(self, response: Dict) -> Dict:
        """
        Parse IPGeolocation response into normalized format
        
        Args:
            response: Raw API response
            
        Returns:
            Normalized data dictionary
        """
        if not response:
            return {}
        
        security = response.get('security', {})
        
        return {
            'source': 'IPGeolocation',
            'country': response.get('country_name'),
            'country_code': response.get('country_code2'),
            'city': response.get('city'),
            'region': response.get('state_prov'),
            'latitude': response.get('latitude'),
            'longitude': response.get('longitude'),
            'timezone': response.get('time_zone', {}).get('name'),
            'zip_code': response.get('zipcode'),
            'isp': response.get('isp'),
            'organization': response.get('organization'),
            'asn': f"AS{response.get('geoname_id')}" if response.get('geoname_id') else None,
            'is_proxy': security.get('is_proxy', False),
            'proxy_type': security.get('proxy_type'),
            'is_tor': security.get('is_tor', False),
            'is_crawler': security.get('is_crawler', False),
            'threat_score': security.get('threat_score', 0),
            'is_anonymous': security.get('is_anonymous', False),
            'is_known_attacker': security.get('is_known_attacker', False),
            'is_cloud_provider': security.get('is_cloud_provider', False),
            'raw_data': response
        }
