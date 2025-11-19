"""
Threat Intelligence Correlator
Main orchestrator that queries APIs, normalizes data, and scores threats
"""
import concurrent.futures
from typing import Dict, Optional
from models.threat_profile import ThreatProfile
from core.normalizer import DataNormalizer
from core.scorer import ThreatScorer
from api.abuseipdb import AbuseIPDBClient
from api.virustotal import VirusTotalClient
from api.ipapi import IPAPIClient  # Free API, no key needed!
from api.ipqualityscore import IPQualityScoreClient
from api.shodan import ShodanClient
from mitre.intelligence_correlator import ThreatIntelligenceCorrelator
from utils.cache import cache_manager
from utils.mock_threat_db import mock_db
from api.darkweb_intel import DarkWebIntelligence

class ThreatCorrelator:
    """
    Main correlation engine that orchestrates threat intelligence gathering
    """
    
    def __init__(self, config):
        """
        Initialize the correlator with API clients
        
        Args:
            config: Configuration object with API keys
        """
        # Initialize API clients
        self.abuseipdb = AbuseIPDBClient(config.get('ABUSEIPDB_API_KEY', ''))
        self.virustotal = VirusTotalClient(config.get('VIRUSTOTAL_API_KEY', ''))
        self.ipapi = IPAPIClient()  # Free API, no key needed!
        self.ipqualityscore = IPQualityScoreClient(config.get('IPQUALITYSCORE_API_KEY', ''))
        self.shodan = ShodanClient(config.get('SHODAN_API_KEY', ''))
        
        # Initialize normalizer and scorer
        self.normalizer = DataNormalizer()
        self.scorer = ThreatScorer(config.get('SCORING_WEIGHTS', {}))
        
        # Initialize threat intelligence correlator with OTX API key
        otx_api_key = config.get('ALIENVAULT_OTX_API_KEY', '')
        self.threat_intel_correlator = ThreatIntelligenceCorrelator(otx_api_key=otx_api_key)
        
        # Initialize dark web intelligence
        hibp_key = config.get('HAVEIBEENPWNED_API_KEY', '')
        self.darkweb_intel = DarkWebIntelligence(hibp_api_key=hibp_key)
        
        self.config = config
    
    def analyze_ip(self, ip_address: str, use_cache: bool = False) -> ThreatProfile:
        """
        Perform comprehensive threat analysis on an IP address
        
        Args:
            ip_address: IP address to analyze
            use_cache: Whether to use cached results (disabled by default for fresh data)
            
        Returns:
            ThreatProfile with complete analysis
        """
        # Caching disabled - always fetch fresh data
        use_cache = False  # Force disable caching
        
        # Check cache first
        if use_cache:
            cached_dict = cache_manager.get(ip_address)
            if cached_dict:
                print(f"Using cached data for {ip_address}")
                # Recreate ThreatProfile from cached data
                profile = ThreatProfile(ip_address)
                profile.threat_score = cached_dict.get('threat_score', 0)
                profile.risk_level = cached_dict.get('risk_level', 'unknown')
                profile.is_malicious = cached_dict.get('is_malicious', False)
                profile.confidence = cached_dict.get('confidence', 0)
                profile.categories = cached_dict.get('categories', [])
                profile.geolocation = cached_dict.get('geolocation', {})
                profile.network_info = cached_dict.get('network_info', {})
                profile.sources = cached_dict.get('sources', {})
                profile.source_scores = cached_dict.get('source_scores', {})
                profile.reports_count = cached_dict.get('reports_count', 0)
                profile.last_reported = cached_dict.get('last_reported')
                profile.timestamp = cached_dict.get('timestamp')
                profile.mitre_intelligence = cached_dict.get('mitre_intelligence', {})  # CRITICAL FIX!
                return profile
        
        # Create new threat profile
        profile = ThreatProfile(ip_address)
        
        # Check if this is a mock threat IP (national/state-level APT)
        is_mock_threat = mock_db.is_mock_threat_ip(ip_address)
        
        if is_mock_threat:
            print(f"🎯 Mock Threat Database Hit: {ip_address}")
            # Get mock threat data
            mock_data = mock_db.get_threat_info(ip_address)
            
            # Still query real APIs for basic info (geo, network, etc.)
            api_responses = self._query_all_apis(ip_address)
            parsed_responses = self._parse_responses(api_responses)
            profile = self.normalizer.consolidate(profile, parsed_responses)
            
            # Override with mock MITRE intelligence (this is the critical part!)
            if 'mitre_attack' in mock_data:
                profile.mitre_intelligence = {
                    'found': True,
                    'apt_groups': mock_data['mitre_attack'].get('associated_groups', []),
                    'tactics': mock_data['mitre_attack'].get('tactics', []),
                    'techniques': mock_data['mitre_attack'].get('techniques', []),
                    'campaign': mock_data['mitre_attack'].get('campaign', ''),
                    'target_sectors': mock_data['mitre_attack'].get('target_sectors', []),
                    'target_regions': mock_data['mitre_attack'].get('target_regions', []),
                    'threat_actor': mock_data.get('threat_actor', ''),
                    'country': mock_data.get('country', '')
                }
            
            # Add threat actor information
            if 'threat_actor' in mock_data:
                profile.threat_actor = mock_data['threat_actor']
            
            # Add threat categories
            if 'categories' in mock_data:
                profile.categories = list(set(profile.categories + mock_data['categories']))
            
            # Add malware families
            if 'malware_families' in mock_data:
                profile.malware_families = mock_data['malware_families']
            
            # Add campaign info
            if 'mitre_attack' in mock_data and 'campaign' in mock_data['mitre_attack']:
                profile.campaign = mock_data['mitre_attack']['campaign']
            
            # Force high threat classification for APTs
            profile.is_malicious = True
            profile.threat_type = mock_data.get('threat_type', 'Advanced Persistent Threat (APT)')
            
        else:
            # Normal flow for non-mock IPs
            # Query all APIs concurrently
            api_responses = self._query_all_apis(ip_address)
            
            # Parse API responses
            parsed_responses = self._parse_responses(api_responses)
            
            # Normalize and consolidate data
            profile = self.normalizer.consolidate(profile, parsed_responses)
            
            # Get MITRE ATT&CK threat intelligence BEFORE scoring (law enforcement context)
            # This is CRITICAL as APT attribution significantly affects the threat score
            try:
                threat_intel = self.threat_intel_correlator.analyze_ip(ip_address)
                profile.mitre_intelligence = threat_intel
            except Exception as e:
                print(f"Threat intelligence error: {e}")
                profile.mitre_intelligence = {'found': False}
        
        # Calculate threat scores (now includes MITRE boost if APT groups detected)
        self.scorer.score_profile(profile)
        
        # Check dark web intelligence (for all IPs - mock and real)
        try:
            print("🕵️ Checking dark web intelligence...")
            darkweb_intel = self.darkweb_intel.check_ip(ip_address)
            profile.darkweb_intelligence = darkweb_intel
            
            # Boost threat score if found on dark web
            if darkweb_intel.get('found_in_darkweb'):
                if darkweb_intel.get('threat_level') == 'critical':
                    profile.threat_score = min(profile.threat_score + 15, 100)
                elif darkweb_intel.get('threat_level') == 'high':
                    profile.threat_score = min(profile.threat_score + 10, 100)
                elif darkweb_intel.get('threat_level') == 'medium':
                    profile.threat_score = min(profile.threat_score + 5, 100)
                
                # Recalculate risk level
                profile.calculate_risk_level()
        except Exception as e:
            print(f"⚠️ Dark web intelligence error: {e}")
            profile.darkweb_intelligence = {'found_in_darkweb': False, 'error': str(e)}
        
        # Caching disabled - do not save results
        # if use_cache:
        #     cache_manager.set(ip_address, profile.to_dict())
        
        return profile
    
    def _query_all_apis(self, ip_address: str) -> Dict:
        """
        Query all threat intelligence APIs concurrently
        
        Args:
            ip_address: IP address to query
            
        Returns:
            Dictionary of API responses
        """
        responses = {}
        
        # Use ThreadPoolExecutor for concurrent API calls
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all API calls
            future_abuseipdb = executor.submit(self.abuseipdb.check_ip, ip_address)
            future_virustotal = executor.submit(self.virustotal.check_ip, ip_address)
            future_ipapi = executor.submit(self.ipapi.check_ip, ip_address)
            future_ipqs = executor.submit(self.ipqualityscore.check_ip, ip_address)
            future_shodan = executor.submit(self.shodan.check_ip, ip_address)
            
            # Gather results
            try:
                responses['abuseipdb'] = future_abuseipdb.result(timeout=self.config.get('API_TIMEOUT', 10))
            except Exception as e:
                print(f"AbuseIPDB error: {e}")
                responses['abuseipdb'] = None
            
            try:
                responses['virustotal'] = future_virustotal.result(timeout=self.config.get('API_TIMEOUT', 10))
            except Exception as e:
                print(f"VirusTotal error: {e}")
                responses['virustotal'] = None
            
            try:
                responses['ipapi'] = future_ipapi.result(timeout=self.config.get('API_TIMEOUT', 10))
            except Exception as e:
                print(f"IP-API error: {e}")
                responses['ipapi'] = None
            
            try:
                responses['ipqualityscore'] = future_ipqs.result(timeout=self.config.get('API_TIMEOUT', 10))
            except Exception as e:
                print(f"IPQualityScore error: {e}")
                responses['ipqualityscore'] = None
            
            try:
                responses['shodan'] = future_shodan.result(timeout=self.config.get('API_TIMEOUT', 10))
            except Exception as e:
                print(f"Shodan error: {e}")
                responses['shodan'] = None
        
        return responses
    
    def _parse_responses(self, api_responses: Dict) -> Dict:
        """
        Parse raw API responses into normalized format
        
        Args:
            api_responses: Dictionary of raw API responses
            
        Returns:
            Dictionary of parsed responses
        """
        parsed = {}
        
        if api_responses.get('abuseipdb'):
            parsed['abuseipdb'] = self.abuseipdb.parse_response(api_responses['abuseipdb'])
        
        if api_responses.get('virustotal'):
            parsed['virustotal'] = self.virustotal.parse_response(api_responses['virustotal'])
        
        if api_responses.get('ipapi'):
            parsed['ipapi'] = self.ipapi.parse_response(api_responses['ipapi'])
        
        if api_responses.get('ipqualityscore'):
            parsed['ipqualityscore'] = api_responses['ipqualityscore']  # Already parsed
        
        if api_responses.get('shodan'):
            parsed['shodan'] = api_responses['shodan']  # Already parsed
        
        return parsed
    
    def get_quick_summary(self, ip_address: str) -> Dict:
        """
        Get a quick summary without full analysis
        
        Args:
            ip_address: IP address to check
            
        Returns:
            Quick summary dictionary
        """
        profile = self.analyze_ip(ip_address)
        return profile.get_summary()
