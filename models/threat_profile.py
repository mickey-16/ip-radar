"""
Unified Threat Profile Model
Standardizes data from multiple threat intelligence sources
"""
from datetime import datetime
from typing import Dict, List, Optional

class ThreatProfile:
    """
    Unified threat intelligence profile for an IP address
    """
    
    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Threat Assessment
        self.threat_score = 0  # 0-100
        self.risk_level = 'unknown'  # low, medium, high, critical
        self.is_malicious = False
        self.confidence = 0  # 0-100
        
        # Threat Categories
        self.categories = []  # List of threat types
        
        # Geolocation Data
        self.geolocation = {
            'country': None,
            'country_code': None,
            'city': None,
            'region': None,
            'latitude': None,
            'longitude': None,
            'timezone': None
        }
        
        # Network Information
        self.network_info = {
            'asn': None,
            'isp': None,
            'organization': None,
            'is_proxy': False,
            'is_vpn': False,
            'is_tor': False,
            'is_hosting': False
        }
        
        # Source Data (raw responses from each API)
        self.sources = {}
        
        # Related Entities
        self.related_entities = {
            'domains': [],
            'urls': [],
            'malware': [],
            'hashes': []
        }
        
        # Additional Intelligence
        self.ports = []
        self.services = []
        self.vulnerabilities = []
        
        # Reputation Scores from Individual Sources
        self.source_scores = {}
        
        # Reports and Incidents
        self.reports_count = 0
        self.last_reported = None
        
        # MITRE ATT&CK Threat Intelligence
        self.mitre_intelligence = {}
        
        # Additional Threat Actor Information (for APT tracking)
        self.threat_actor = None
        self.threat_type = None
        self.malware_families = []
        self.campaign = None
        
        # Dark Web Intelligence
        self.darkweb_intelligence = {}
        
    def add_source_data(self, source_name: str, data: Dict):
        """Add raw data from a threat intelligence source"""
        self.sources[source_name] = data
        
    def add_category(self, category: str):
        """Add a threat category if not already present"""
        if category and category not in self.categories:
            self.categories.append(category)
            
    def set_geolocation(self, **kwargs):
        """Update geolocation information"""
        for key, value in kwargs.items():
            if key in self.geolocation and value is not None:
                self.geolocation[key] = value
                
    def set_network_info(self, **kwargs):
        """Update network information"""
        for key, value in kwargs.items():
            if key in self.network_info and value is not None:
                self.network_info[key] = value
                
    def calculate_risk_level(self):
        """Calculate risk level based on threat score"""
        if self.threat_score <= 20:
            self.risk_level = 'low'
        elif self.threat_score <= 50:
            self.risk_level = 'medium'
        elif self.threat_score <= 75:
            self.risk_level = 'high'
        else:
            self.risk_level = 'critical'
            
        # Set malicious flag
        self.is_malicious = self.threat_score > 50
        
    def to_dict(self) -> Dict:
        """Convert threat profile to dictionary"""
        return {
            'ip_address': self.ip_address,
            'timestamp': self.timestamp,
            'threat_score': round(self.threat_score, 2),
            'risk_level': self.risk_level,
            'is_malicious': self.is_malicious,
            'confidence': round(self.confidence, 2),
            'categories': self.categories,
            'geolocation': self.geolocation,
            'network_info': self.network_info,
            'source_scores': self.source_scores,
            'sources': self.sources,
            'related_entities': self.related_entities,
            'reports_count': self.reports_count,
            'last_reported': self.last_reported,
            'ports': self.ports,
            'services': self.services,
            'vulnerabilities': self.vulnerabilities,
            'mitre_intelligence': self.mitre_intelligence,
            'threat_actor': self.threat_actor,
            'threat_type': self.threat_type,
            'malware_families': self.malware_families,
            'campaign': self.campaign,
            'darkweb_intelligence': self.darkweb_intelligence
        }
        
    def get_summary(self) -> Dict:
        """Get a summarized version without raw source data"""
        data = self.to_dict()
        # Remove verbose source data for summary
        data['sources'] = {k: 'Available' for k in self.sources.keys()}
        return data
