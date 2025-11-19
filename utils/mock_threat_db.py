"""
Mock Threat Database Module
Provides national/state-level threat intelligence for demonstration purposes
"""

import json
import os
from typing import Dict, Optional, Any


class MockThreatDatabase:
    """
    Mock threat intelligence database containing national/state-level APT infrastructure
    with MITRE ATT&CK mappings for demonstration purposes.
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize the mock threat database
        
        Args:
            db_path: Path to the mock database JSON file
        """
        if db_path is None:
            # Default to mock_threat_database.json in the project root
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            db_path = os.path.join(project_root, 'mock_threat_database.json')
        
        self.db_path = db_path
        self.threat_data = self._load_database()
    
    def _load_database(self) -> Dict:
        """Load the mock threat database from JSON file"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('mock_threat_ips', {})
        except FileNotFoundError:
            print(f"Warning: Mock database not found at {self.db_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error parsing mock database: {e}")
            return {}
    
    def is_mock_threat_ip(self, ip_address: str) -> bool:
        """
        Check if an IP address exists in the mock threat database
        
        Args:
            ip_address: IP address to check
            
        Returns:
            True if IP is in mock database, False otherwise
        """
        return ip_address in self.threat_data
    
    def get_threat_info(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """
        Get complete threat information for an IP address
        
        Args:
            ip_address: IP address to lookup
            
        Returns:
            Dictionary containing threat information or None if not found
        """
        return self.threat_data.get(ip_address)
    
    def get_mitre_attack_info(self, ip_address: str) -> Optional[Dict[str, Any]]:
        """
        Get MITRE ATT&CK information for an IP address
        
        Args:
            ip_address: IP address to lookup
            
        Returns:
            Dictionary containing MITRE ATT&CK tactics and techniques or None
        """
        threat_info = self.get_threat_info(ip_address)
        if threat_info:
            return threat_info.get('mitre_attack')
        return None
    
    def get_threat_actor(self, ip_address: str) -> Optional[str]:
        """
        Get threat actor name for an IP address
        
        Args:
            ip_address: IP address to lookup
            
        Returns:
            Threat actor name or None
        """
        threat_info = self.get_threat_info(ip_address)
        if threat_info:
            return threat_info.get('threat_actor')
        return None
    
    def get_all_mock_ips(self) -> list:
        """
        Get list of all IP addresses in the mock database
        
        Returns:
            List of IP addresses
        """
        return list(self.threat_data.keys())
    
    def enrich_threat_profile(self, ip_address: str, base_profile: Dict) -> Dict:
        """
        Enrich a threat profile with mock database information
        
        Args:
            ip_address: IP address being analyzed
            base_profile: Base threat profile from real APIs
            
        Returns:
            Enriched threat profile with mock data if IP is in database
        """
        if not self.is_mock_threat_ip(ip_address):
            return base_profile
        
        mock_data = self.get_threat_info(ip_address)
        
        # Enrich the profile with mock data
        enriched = base_profile.copy()
        
        # Add MITRE ATT&CK information
        if 'mitre_attack' in mock_data:
            enriched['mitre_attack'] = mock_data['mitre_attack']
        
        # Add threat actor information
        if 'threat_actor' in mock_data:
            enriched['threat_actor'] = mock_data['threat_actor']
        
        # Add threat type
        if 'threat_type' in mock_data:
            enriched['threat_type'] = mock_data['threat_type']
        
        # Enhance threat categories
        if 'categories' in mock_data:
            existing_categories = enriched.get('threat_categories', [])
            mock_categories = mock_data['categories']
            # Merge and deduplicate
            enriched['threat_categories'] = list(set(existing_categories + mock_categories))
        
        # Add malware families
        if 'malware_families' in mock_data:
            enriched['malware_families'] = mock_data['malware_families']
        
        # Add IOC references
        if 'ioc_references' in mock_data:
            enriched['ioc_references'] = mock_data['ioc_references']
        
        # Add campaign information
        if 'mitre_attack' in mock_data and 'campaign' in mock_data['mitre_attack']:
            enriched['campaign'] = mock_data['mitre_attack']['campaign']
        
        # Enhance risk score with APT classification
        if mock_data.get('threat_type') == 'Advanced Persistent Threat (APT)':
            # Ensure high risk score for APTs
            current_score = enriched.get('risk_score', 0)
            enriched['risk_score'] = max(current_score, 85)  # Minimum 85 for APTs
        
        # Add confidence from mock data
        if 'confidence_score' in mock_data:
            enriched['confidence_score'] = mock_data['confidence_score']
        
        # Mark as APT infrastructure
        enriched['is_apt_infrastructure'] = True
        enriched['data_source'] = 'mock_threat_database'
        
        return enriched
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the mock database
        
        Returns:
            Dictionary containing database statistics
        """
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('metadata', {})
        except:
            return {
                'total_threat_actors': len(self.threat_data),
                'ip_addresses': self.get_all_mock_ips()
            }


# Global instance
mock_db = MockThreatDatabase()


# Convenience functions
def is_mock_threat_ip(ip_address: str) -> bool:
    """Check if IP is in mock threat database"""
    return mock_db.is_mock_threat_ip(ip_address)


def get_mock_threat_info(ip_address: str) -> Optional[Dict[str, Any]]:
    """Get threat information from mock database"""
    return mock_db.get_threat_info(ip_address)


def enrich_with_mock_data(ip_address: str, base_profile: Dict) -> Dict:
    """Enrich threat profile with mock database data"""
    return mock_db.enrich_threat_profile(ip_address, base_profile)
