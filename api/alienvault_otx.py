"""
AlienVault OTX (Open Threat Exchange) API Client
Provides threat intelligence linking IPs to APT groups and campaigns
"""
import requests
from typing import Dict, List, Optional
from datetime import datetime


class AlienVaultOTXClient:
    """
    Client for querying AlienVault Open Threat Exchange
    FREE API key available at: https://otx.alienvault.com/
    
    Benefits of using API key:
    - Higher rate limits (1000s of requests vs 100s)
    - No 429 "Too Many Requests" errors
    - Better access to threat intelligence
    """
    
    BASE_URL = "https://otx.alienvault.com/api/v1"
    
    def __init__(self, api_key: str = None, timeout: int = 10):
        """
        Initialize OTX client
        
        Args:
            api_key: Optional API key for higher rate limits
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set headers
        headers = {
            'User-Agent': 'TICE-Threat-Intelligence/1.0'
        }
        
        # Add API key if provided
        if api_key:
            headers['X-OTX-API-KEY'] = api_key
            print("✅ AlienVault OTX: Using API key (higher rate limits)")
        else:
            print("⚠️  AlienVault OTX: No API key (limited rate limits - may get 429 errors)")
            print("   Get free API key at: https://otx.alienvault.com/")
        
        self.session.headers.update(headers)
    
    def check_ip(self, ip_address: str) -> Dict:
        """
        Check IP address for threat intelligence
        
        Args:
            ip_address: IP address to check
            
        Returns:
            Dictionary with threat intelligence data
        """
        try:
            # Query general endpoint
            general_data = self._get_general_info(ip_address)
            
            # Extract relevant intelligence
            intelligence = self._parse_intelligence(general_data, ip_address)
            
            return intelligence
            
        except requests.RequestException as e:
            print(f"AlienVault OTX error for {ip_address}: {e}")
            return self._empty_response()
        except Exception as e:
            print(f"AlienVault OTX parsing error: {e}")
            return self._empty_response()
    
    def _get_general_info(self, ip_address: str) -> Dict:
        """Get general information about IP from OTX"""
        url = f"{self.BASE_URL}/indicators/IPv4/{ip_address}/general"
        
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        return response.json()
    
    def _parse_intelligence(self, data: Dict, ip_address: str) -> Dict:
        """Parse OTX response into structured intelligence"""
        
        pulse_info = data.get('pulse_info', {})
        pulses = pulse_info.get('pulses', [])
        pulse_count = pulse_info.get('count', 0)
        
        # Extract threat groups and tags
        threat_groups = set()
        tags = set()
        campaigns = set()
        malware = set()
        first_seen = None
        last_seen = None
        
        # Known threat actor keywords to look for
        threat_keywords = [
            'apt', 'lazarus', 'fancy', 'bear', 'panda', 'kitten', 'dragon',
            'muddy', 'muddywater', 'equation', 'comment', 'crew', 'vetala',
            'unc', 'turla', 'sofacy', 'sednit', 'carbanak', 'cobalt',
            'sandworm', 'energetic bear', 'temp.', 'group', 'admin'
        ]
        
        for pulse in pulses:
            # Extract tags
            pulse_tags = pulse.get('tags', [])
            for tag in pulse_tags:
                tag_lower = tag.lower()
                tags.add(tag)
                
                # Identify threat actors/groups
                # Check if tag contains known threat keywords
                is_threat_actor = any(keyword in tag_lower for keyword in threat_keywords)
                
                # Also check if tag looks like a threat actor name
                # (usually capitalized, 2+ words, or has numbers like APT28)
                if is_threat_actor or (tag.istitle() and len(tag.split()) >= 2) or \
                   (any(char.isdigit() for char in tag) and any(char.isalpha() for char in tag)):
                    threat_groups.add(tag)
            
            # Extract from pulse name
            pulse_name = pulse.get('name', '')
            if 'apt' in pulse_name.lower():
                # Try to extract APT number
                for word in pulse_name.split():
                    if word.lower().startswith('apt'):
                        threat_groups.add(word)
            
            # Track dates
            created = pulse.get('created')
            if created:
                try:
                    pulse_date = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    if not first_seen or pulse_date < first_seen:
                        first_seen = pulse_date
                    if not last_seen or pulse_date > last_seen:
                        last_seen = pulse_date
                except:
                    pass
        
        # Determine if linked to APT
        has_apt_link = bool(threat_groups) or any('apt' in tag.lower() for tag in tags)
        
        return {
            'source': 'alienvault_otx',
            'found': pulse_count > 0,
            'pulse_count': pulse_count,
            'threat_groups': list(threat_groups),
            'tags': list(tags)[:20],  # Limit to top 20 tags
            'has_apt_link': has_apt_link,
            'first_seen': first_seen.isoformat() if first_seen else None,
            'last_seen': last_seen.isoformat() if last_seen else None,
            'pulses_sample': [
                {
                    'name': pulse.get('name', ''),
                    'created': pulse.get('created', ''),
                    'tags': pulse.get('tags', [])[:5]
                }
                for pulse in pulses[:5]  # First 5 pulses
            ]
        }
    
    def _empty_response(self) -> Dict:
        """Return empty response when API fails"""
        return {
            'source': 'alienvault_otx',
            'found': False,
            'pulse_count': 0,
            'threat_groups': [],
            'tags': [],
            'has_apt_link': False,
            'first_seen': None,
            'last_seen': None,
            'pulses_sample': []
        }
