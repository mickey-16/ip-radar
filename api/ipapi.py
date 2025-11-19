"""
Free IP-API.com Integration (No API Key Required!)
API Documentation: https://ip-api.com/docs/api:json
Free tier: 45 requests/minute
"""
import requests
from typing import Dict, Optional

class IPAPIClient:
    """
    Client for ip-api.com - FREE geolocation API (no key needed!)
    Free tier: 45 requests per minute
    """
    
    BASE_URL = 'http://ip-api.com/json'
    
    def __init__(self):
        """No API key needed!"""
        pass
    
    def check_ip(self, ip_address: str) -> Optional[Dict]:
        """
        Get IP geolocation information
        
        Args:
            ip_address: IP address to check
            
        Returns:
            Dict containing API response or None on error
        """
        endpoint = f"{self.BASE_URL}/{ip_address}"
        params = {
            'fields': 'status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,proxy,hosting'
        }
        
        try:
            response = requests.get(
                endpoint,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return data
                else:
                    print(f"IP-API: {data.get('message', 'Unknown error')}")
                    return None
            else:
                print(f"IP-API error: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"IP-API request error: {e}")
            return None
    
    def parse_response(self, response: Dict) -> Dict:
        """
        Parse IP-API response into normalized format
        
        Args:
            response: Raw API response
            
        Returns:
            Normalized data dictionary
        """
        if not response:
            return {}
        
        return {
            'source': 'IP-API',
            'country': response.get('country'),
            'country_code': response.get('countryCode'),
            'city': response.get('city'),
            'region': response.get('regionName'),
            'latitude': response.get('lat'),
            'longitude': response.get('lon'),
            'timezone': response.get('timezone'),
            'zip_code': response.get('zip'),
            'isp': response.get('isp'),
            'organization': response.get('org'),
            'asn': response.get('as'),
            'as_name': response.get('asname'),
            'is_proxy': response.get('proxy', False),
            'is_hosting': response.get('hosting', False),
            'is_tor': False,  # IP-API doesn't provide this
            'threat_score': 0,  # We'll calculate based on flags
            'raw_data': response
        }
