"""
IPQualityScore API Client
Provides fraud detection and proxy/VPN detection
"""
import requests
from typing import Dict, Optional

class IPQualityScoreClient:
    """Client for IPQualityScore API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://ipqualityscore.com/api/json/ip"
        
    def check_ip(self, ip_address: str) -> Optional[Dict]:
        """
        Check IP reputation and fraud score
        
        Args:
            ip_address: IP address to check
            
        Returns:
            dict with fraud score and detection data or None if error
        """
        if not self.api_key:
            return None
            
        try:
            url = f"{self.base_url}/{self.api_key}/{ip_address}"
            
            # Parameters for detailed analysis
            params = {
                'strictness': 1,  # 0=least strict, 3=most strict
                'allow_public_access_points': 'true',
                'fast': 'false',  # More accurate, slower
                'mobile': 'true',
                'user_language': 'en-US'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('success'):
                return {
                    'fraud_score': data.get('fraud_score', 0),
                    'country_code': data.get('country_code'),
                    'region': data.get('region'),
                    'city': data.get('city'),
                    'ISP': data.get('ISP'),
                    'ASN': data.get('ASN'),
                    'organization': data.get('organization'),
                    'is_crawler': data.get('is_crawler', False),
                    'timezone': data.get('timezone'),
                    'mobile': data.get('mobile', False),
                    'host': data.get('host'),
                    'proxy': data.get('proxy', False),
                    'vpn': data.get('vpn', False),
                    'tor': data.get('tor', False),
                    'active_vpn': data.get('active_vpn', False),
                    'active_tor': data.get('active_tor', False),
                    'recent_abuse': data.get('recent_abuse', False),
                    'bot_status': data.get('bot_status', False),
                    'connection_type': data.get('connection_type'),
                    'abuse_velocity': data.get('abuse_velocity'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'request_id': data.get('request_id')
                }
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"IPQualityScore API error: {e}")
            return None
        except Exception as e:
            print(f"IPQualityScore processing error: {e}")
            return None
