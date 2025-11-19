"""
Shodan API Client
Provides port scanning and service detection
"""
import requests
from typing import Dict, Optional

class ShodanClient:
    """Client for Shodan API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.shodan.io"
        
    def check_ip(self, ip_address: str) -> Optional[Dict]:
        """
        Get information about an IP from Shodan
        
        Args:
            ip_address: IP address to check
            
        Returns:
            dict with host information or None if error
        """
        if not self.api_key:
            return None
            
        try:
            url = f"{self.base_url}/shodan/host/{ip_address}"
            params = {'key': self.api_key}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant information
            return {
                'ip': data.get('ip_str'),
                'organization': data.get('org'),
                'asn': data.get('asn'),
                'isp': data.get('isp'),
                'country_code': data.get('country_code'),
                'country_name': data.get('country_name'),
                'city': data.get('city'),
                'region_code': data.get('region_code'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'ports': data.get('ports', []),
                'hostnames': data.get('hostnames', []),
                'domains': data.get('domains', []),
                'tags': data.get('tags', []),
                'vulns': data.get('vulns', []),
                'os': data.get('os'),
                'last_update': data.get('last_update'),
                'services': self._extract_services(data.get('data', [])),
                'open_ports_count': len(data.get('ports', [])),
                'vulnerabilities_count': len(data.get('vulns', []))
            }
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                # IP not found in Shodan database
                return {
                    'ip': ip_address,
                    'found': False,
                    'message': 'No information available'
                }
            print(f"Shodan API error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Shodan API error: {e}")
            return None
        except Exception as e:
            print(f"Shodan processing error: {e}")
            return None
    
    def _extract_services(self, data_list):
        """Extract service information from Shodan data"""
        services = []
        for item in data_list[:5]:  # Limit to first 5 services
            service = {
                'port': item.get('port'),
                'transport': item.get('transport'),
                'product': item.get('product'),
                'version': item.get('version'),
                'banner': item.get('data', '')[:200]  # Truncate banner
            }
            services.append(service)
        return services
