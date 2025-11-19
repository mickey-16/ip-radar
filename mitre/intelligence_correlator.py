"""
Threat Intelligence Correlator
Combines AlienVault OTX, ThreatFox, and MITRE ATT&CK data
"""
from typing import Dict, List
from api.alienvault_otx import AlienVaultOTXClient
from api.threatfox import ThreatFoxClient
from mitre.scraper import MITREAttackScraper


class ThreatIntelligenceCorrelator:
    """
    Correlates threat intelligence from multiple sources
    Provides law enforcement-grade historical context
    """
    
    def __init__(self, otx_api_key: str = None):
        """
        Initialize threat intelligence correlator
        
        Args:
            otx_api_key: Optional AlienVault OTX API key for higher rate limits
        """
        self.otx_client = AlienVaultOTXClient(api_key=otx_api_key)
        self.threatfox_client = ThreatFoxClient()
        self.mitre_scraper = MITREAttackScraper()
    
    def analyze_ip(self, ip_address: str) -> Dict:
        """
        Perform comprehensive threat intelligence analysis
        
        Args:
            ip_address: IP address to analyze
            
        Returns:
            Correlated intelligence report
        """
        
        # 1. Query AlienVault OTX for threat groups
        otx_intel = self.otx_client.check_ip(ip_address)
        
        # 2. Query ThreatFox for malware IOCs
        threatfox_intel = self.threatfox_client.check_ip(ip_address)
        
        # 3. Get MITRE profiles for identified threat groups
        mitre_profiles = []
        if otx_intel['found'] and otx_intel['threat_groups']:
            for group in otx_intel['threat_groups'][:3]:  # Limit to top 3
                profile = self.mitre_scraper.get_group_profile(group)
                if profile['found']:
                    mitre_profiles.append(profile)
        
        # 4. Correlate findings
        correlated = self._correlate_intelligence(
            ip_address, 
            otx_intel, 
            threatfox_intel, 
            mitre_profiles
        )
        
        return correlated
    
    def _correlate_intelligence(
        self, 
        ip: str,
        otx: Dict, 
        threatfox: Dict, 
        mitre: List[Dict]
    ) -> Dict:
        """Correlate all intelligence sources"""
        
        # Determine if any intelligence found
        found = otx['found'] or threatfox['found'] or len(mitre) > 0
        
        # Build threat actor list
        threat_actors = []
        for profile in mitre:
            actor = {
                'name': profile['group_name'],
                'mitre_id': profile['group_id'],
                'aliases': profile['aliases'],
                'attribution': profile['attribution'],
                'description': profile['description']
            }
            threat_actors.append(actor)
        
        # Build malware list (from both sources)
        malware_families = set()
        if threatfox['found']:
            malware_families.update(threatfox['malware_families'])
        
        # Add MITRE software
        for profile in mitre:
            malware_families.update(profile['software'])
        
        # Build timeline
        timeline = self._build_timeline(otx, threatfox)
        
        # Build techniques list
        techniques = []
        for profile in mitre:
            techniques.extend(profile['techniques'])
        
        # Determine confidence level
        confidence = self._calculate_confidence(otx, threatfox, mitre)
        
        # Build campaigns list
        campaigns = []
        if otx['found'] and 'sample_pulses' in otx:
            for pulse in otx['sample_pulses']:
                campaigns.append({
                    'name': pulse['name'],
                    'date': pulse['created'],
                    'source': 'AlienVault OTX'
                })
        
        # Identify threat types
        threat_types = set()
        if threatfox['found']:
            threat_types.update(threatfox['threat_types'])
        
        if threatfox['is_c2_server']:
            threat_types.add('C2 Server')
        if threatfox['is_botnet']:
            threat_types.add('Botnet Infrastructure')
        
        # Build correlated report
        report = {
            'source': 'threat_intelligence_correlator',
            'found': found,
            'ip_address': ip,
            'threat_actors': threat_actors,
            'malware_families': sorted(list(malware_families)),
            'campaigns': campaigns,
            'timeline': timeline,
            'techniques': techniques[:15],  # Limit to 15
            'threat_types': sorted(list(threat_types)),
            'confidence': confidence,
            'has_apt_attribution': len(threat_actors) > 0,
            'is_c2_server': threatfox['is_c2_server'],
            'is_botnet': threatfox['is_botnet'],
            'otx_pulse_count': otx.get('pulse_count', 0),
            'threatfox_ioc_count': threatfox.get('ioc_count', 0),
            'mitre_group_count': len(mitre),
            'raw_sources': {
                'alienvault_otx': otx,
                'threatfox': threatfox,
                'mitre_attack': mitre
            }
        }
        
        return report
    
    def _build_timeline(self, otx: Dict, threatfox: Dict) -> Dict:
        """Build activity timeline from all sources"""
        timeline = {
            'first_seen': None,
            'last_seen': None,
            'activity_span_days': 0
        }
        
        # Get dates from OTX
        if otx['found']:
            if 'first_seen' in otx and otx['first_seen']:
                timeline['first_seen'] = otx['first_seen']
            if 'last_seen' in otx and otx['last_seen']:
                timeline['last_seen'] = otx['last_seen']
        
        # Calculate span
        if timeline['first_seen'] and timeline['last_seen']:
            try:
                from datetime import datetime
                first = datetime.fromisoformat(timeline['first_seen'].replace('Z', '+00:00'))
                last = datetime.fromisoformat(timeline['last_seen'].replace('Z', '+00:00'))
                timeline['activity_span_days'] = (last - first).days
            except:
                pass
        
        return timeline
    
    def _calculate_confidence(self, otx: Dict, threatfox: Dict, mitre: List[Dict]) -> str:
        """Calculate overall confidence level"""
        
        # Count evidence sources
        sources = 0
        if otx['found']:
            sources += 1
        if threatfox['found']:
            sources += 1
        if len(mitre) > 0:
            sources += 1
        
        # Additional weight factors
        has_apt = len(mitre) > 0
        high_pulse_count = otx.get('pulse_count', 0) > 5
        is_c2 = threatfox.get('is_c2_server', False)
        
        # Determine confidence
        if sources >= 3 and has_apt:
            return 'CRITICAL'
        elif sources >= 2 and (has_apt or is_c2 or high_pulse_count):
            return 'HIGH'
        elif sources >= 2:
            return 'MEDIUM'
        elif sources == 1:
            return 'LOW'
        else:
            return 'NONE'
