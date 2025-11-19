"""
ThreatFox API Client (by Abuse.ch)
Provides malware IOC intelligence - C2 servers, malware families
"""
import requests
from typing import Dict, List, Optional


class ThreatFoxClient:
    """
    Client for querying ThreatFox IOC database
    FREE - No API key required
    """
    
    API_URL = "https://threatfox-api.abuse.ch/api/v1/"
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TICE-Threat-Intelligence/1.0',
            'Content-Type': 'application/json'
        })
    
    def check_ip(self, ip_address: str) -> Dict:
        """
        Check IP address for malware IOC intelligence
        
        Args:
            ip_address: IP address to check
            
        Returns:
            Dictionary with malware intelligence data
        """
        try:
            # Search for IP in IOC database
            payload = {
                "query": "search_ioc",
                "search_term": ip_address
            }
            
            response = self.session.post(
                self.API_URL,
                json=payload,
                timeout=self.timeout
            )
            
            # Handle 401/403 errors gracefully (API might have rate limits)
            if response.status_code in [401, 403]:
                print(f"ThreatFox API access restricted (status {response.status_code})")
                return self._empty_response()
            
            response.raise_for_status()
            
            data = response.json()
            
            # Parse intelligence
            intelligence = self._parse_intelligence(data, ip_address)
            
            return intelligence
            
        except requests.RequestException as e:
            print(f"ThreatFox error for {ip_address}: {e}")
            return self._empty_response()
        except Exception as e:
            print(f"ThreatFox parsing error: {e}")
            return self._empty_response()
    
    def _parse_intelligence(self, data: Dict, ip_address: str) -> Dict:
        """Parse ThreatFox response into structured intelligence"""
        
        query_status = data.get('query_status')
        
        if query_status != 'ok':
            return self._empty_response()
        
        ioc_data = data.get('data', [])
        
        if not ioc_data:
            return self._empty_response()
        
        # Extract malware families and threat types
        malware_families = set()
        threat_types = set()
        tags = set()
        confidence_levels = []
        references = []
        
        for ioc in ioc_data:
            # Malware family
            malware = ioc.get('malware')
            if malware:
                malware_families.add(malware)
            
            # Threat type
            threat_type = ioc.get('threat_type')
            if threat_type:
                threat_types.add(threat_type)
            
            # Tags
            ioc_tags = ioc.get('tags', [])
            for tag in ioc_tags:
                tags.add(tag)
            
            # Confidence
            confidence = ioc.get('confidence_level')
            if confidence:
                confidence_levels.append(confidence)
            
            # References
            reference = ioc.get('reference')
            if reference and reference not in references:
                references.append(reference)
        
        # Calculate average confidence
        avg_confidence = sum(confidence_levels) / len(confidence_levels) if confidence_levels else 0
        
        # Determine if it's a C2 server
        is_c2_server = any('c2' in tt.lower() or 'cc' in tt.lower() for tt in threat_types)
        
        # Determine if it's botnet related
        is_botnet = any('botnet' in tt.lower() for tt in threat_types)
        
        return {
            'source': 'threatfox',
            'found': True,
            'ioc_count': len(ioc_data),
            'malware_families': list(malware_families),
            'threat_types': list(threat_types),
            'tags': list(tags),
            'is_c2_server': is_c2_server,
            'is_botnet': is_botnet,
            'confidence': round(avg_confidence, 2),
            'references': references[:5],  # Top 5 references
            'iocs_sample': [
                {
                    'malware': ioc.get('malware'),
                    'threat_type': ioc.get('threat_type'),
                    'confidence': ioc.get('confidence_level'),
                    'first_seen': ioc.get('first_seen')
                }
                for ioc in ioc_data[:5]  # First 5 IOCs
            ]
        }
    
    def _empty_response(self) -> Dict:
        """Return empty response when API fails or no data"""
        return {
            'source': 'threatfox',
            'found': False,
            'ioc_count': 0,
            'malware_families': [],
            'threat_types': [],
            'tags': [],
            'is_c2_server': False,
            'is_botnet': False,
            'confidence': 0,
            'references': [],
            'iocs_sample': []
        }
