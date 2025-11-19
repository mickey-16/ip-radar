"""
Data Normalizer
Consolidates and normalizes data from multiple threat intelligence sources
"""
from typing import Dict, List
from models.threat_profile import ThreatProfile
from utils.helpers import normalize_category

class DataNormalizer:
    """
    Normalizes threat intelligence data from multiple sources into a unified format
    """
    
    def normalize_abuseipdb(self, profile: ThreatProfile, data: Dict):
        """
        Normalize AbuseIPDB data into threat profile
        
        Args:
            profile: ThreatProfile to update
            data: Parsed AbuseIPDB data
        """
        if not data:
            return
        
        # Add source data (including whitelisted status)
        profile.add_source_data('abuseipdb', data.get('raw_data', {}))
        
        # Get confidence score and whitelisted status
        confidence = data.get('confidence_score', 0)
        is_whitelisted = data.get('is_whitelisted', False)
        
        # Update confidence score
        # For whitelisted IPs, use 0 score regardless of reports
        if is_whitelisted:
            profile.source_scores['abuseipdb'] = 0
        else:
            profile.source_scores['abuseipdb'] = confidence
        
        # Update report count (informational only)
        profile.reports_count += data.get('total_reports', 0)
        
        # Update last reported
        if data.get('last_reported'):
            profile.last_reported = data['last_reported']
        
        # Add categories (already filtered by _parse_categories for whitelisted IPs)
        for category in data.get('categories', []):
            profile.add_category(normalize_category(category))
        
        # Update network info
        if data.get('isp'):
            profile.set_network_info(isp=data['isp'])
        
        if data.get('domain'):
            profile.set_network_info(organization=data['domain'])
        
        # Update geolocation
        if data.get('country_code'):
            profile.set_geolocation(country_code=data['country_code'])
    
    def normalize_virustotal(self, profile: ThreatProfile, data: Dict):
        """
        Normalize VirusTotal data into threat profile
        
        Args:
            profile: ThreatProfile to update
            data: Parsed VirusTotal data
        """
        if not data:
            return
        
        # Add source data
        profile.add_source_data('virustotal', data.get('raw_data', {}))
        
        # Calculate score based on detection rate
        detection_rate = data.get('detection_rate', 0)
        profile.source_scores['virustotal'] = detection_rate
        
        # Add categories
        for category in data.get('categories', []):
            profile.add_category(normalize_category(category))
        
        # Update network info
        if data.get('asn'):
            profile.set_network_info(asn=data['asn'])
        
        if data.get('as_owner'):
            profile.set_network_info(organization=data['as_owner'])
        
        # Update geolocation
        if data.get('country'):
            profile.set_geolocation(country=data['country'])
    
    def normalize_ipapi(self, profile: ThreatProfile, data: Dict):
        """
        Normalize IP-API data into threat profile
        
        Args:
            profile: ThreatProfile to update
            data: Parsed IP-API data
        """
        if not data:
            return
        
        # Add source data
        profile.add_source_data('ipapi', data.get('raw_data', {}))
        
        # Calculate score based on threat indicators
        threat_score = 0
        if data.get('is_proxy'):
            threat_score += 30
        if data.get('is_hosting'):
            threat_score += 10
        
        profile.source_scores['ipapi'] = min(threat_score, 100)
        
        # Update network info
        profile.set_network_info(
            is_proxy=data.get('is_proxy', False),
            is_hosting=data.get('is_hosting', False),
            isp=data.get('isp'),
            organization=data.get('organization'),
            asn=data.get('asn')
        )
        
        # Update geolocation
        profile.set_geolocation(
            country=data.get('country'),
            country_code=data.get('country_code'),
            city=data.get('city'),
            region=data.get('region'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            timezone=data.get('timezone')
        )
        
        # Add categories based on flags
        if data.get('is_proxy'):
            profile.add_category('Proxy/VPN')
        if data.get('is_hosting'):
            profile.add_category('Hosting Provider')
    
    def normalize_ipgeolocation(self, profile: ThreatProfile, data: Dict):
        """
        Normalize IPGeolocation data into threat profile
        
        Args:
            profile: ThreatProfile to update
            data: Parsed IPGeolocation data
        """
        if not data:
            return
        
        # Add source data
        profile.add_source_data('ipgeolocation', data.get('raw_data', {}))
        
        # Calculate score based on threat indicators
        threat_score = 0
        if data.get('is_proxy'):
            threat_score += 30
        if data.get('is_tor'):
            threat_score += 40
        if data.get('is_known_attacker'):
            threat_score += 80
        if data.get('is_anonymous'):
            threat_score += 20
        
        # Use their threat score if available
        if data.get('threat_score'):
            threat_score = max(threat_score, data['threat_score'])
        
        profile.source_scores['ipgeolocation'] = min(threat_score, 100)
        
        # Update network info
        profile.set_network_info(
            is_proxy=data.get('is_proxy', False),
            is_tor=data.get('is_tor', False),
            isp=data.get('isp'),
            organization=data.get('organization'),
            asn=data.get('asn')
        )
        
        # Update geolocation
        profile.set_geolocation(
            country=data.get('country'),
            country_code=data.get('country_code'),
            city=data.get('city'),
            region=data.get('region'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            timezone=data.get('timezone')
        )
        
        # Add categories based on flags
        if data.get('is_proxy'):
            profile.add_category('Proxy/VPN')
        if data.get('is_tor'):
            profile.add_category('Tor')
        if data.get('is_known_attacker'):
            profile.add_category('Known Attacker')
    
    def consolidate(self, profile: ThreatProfile, api_responses: Dict) -> ThreatProfile:
        """
        Consolidate all API responses into a unified threat profile
        
        Args:
            profile: ThreatProfile to update
            api_responses: Dictionary of parsed API responses
            
        Returns:
            Updated ThreatProfile
        """
        # Normalize each source
        if 'abuseipdb' in api_responses:
            self.normalize_abuseipdb(profile, api_responses['abuseipdb'])
        
        if 'virustotal' in api_responses:
            self.normalize_virustotal(profile, api_responses['virustotal'])
        
        if 'ipapi' in api_responses:
            self.normalize_ipapi(profile, api_responses['ipapi'])
        
        if 'ipqualityscore' in api_responses:
            self.normalize_ipqualityscore(profile, api_responses['ipqualityscore'])
        
        if 'shodan' in api_responses:
            self.normalize_shodan(profile, api_responses['shodan'])
        
        return profile
    
    def normalize_ipqualityscore(self, profile: ThreatProfile, data: Dict):
        """
        Normalize IPQualityScore data into threat profile
        
        Args:
            profile: ThreatProfile to update
            data: IPQualityScore response data
        """
        if not data:
            return
        
        # Add source data
        profile.add_source_data('ipqualityscore', data)
        
        # Fraud score (0-100, higher = more likely fraud)
        fraud_score = data.get('fraud_score', 0)
        profile.source_scores['ipqualityscore'] = fraud_score
        
        # Update network info with proxy/VPN detection
        profile.set_network_info(
            is_proxy=data.get('proxy', False) or data.get('vpn', False),
            is_vpn=data.get('vpn', False) or data.get('active_vpn', False),
            is_tor=data.get('tor', False) or data.get('active_tor', False),
            isp=data.get('ISP'),
            asn=f"AS{data.get('ASN')}" if data.get('ASN') else None,
            organization=data.get('organization')
        )
        
        # Update geolocation
        profile.set_geolocation(
            country_code=data.get('country_code'),
            region=data.get('region'),
            city=data.get('city'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            timezone=data.get('timezone')
        )
        
        # Add categories based on detection
        if data.get('proxy'):
            profile.add_category('Proxy')
        if data.get('vpn'):
            profile.add_category('VPN')
        if data.get('tor'):
            profile.add_category('Tor')
        if data.get('recent_abuse'):
            profile.add_category('Recent Abuse')
        if data.get('bot_status'):
            profile.add_category('Bot')
        if data.get('is_crawler'):
            profile.add_category('Crawler')
        if fraud_score >= 75:
            profile.add_category('High Fraud Risk')
    
    def normalize_shodan(self, profile: ThreatProfile, data: Dict):
        """
        Normalize Shodan data into threat profile
        
        Args:
            profile: ThreatProfile to update
            data: Shodan response data
        """
        if not data or not data.get('found', True):
            return
        
        # Add source data
        profile.add_source_data('shodan', data)
        
        # Calculate threat score based on vulnerabilities and open ports
        vulns_count = data.get('vulnerabilities_count', 0)
        ports_count = data.get('open_ports_count', 0)
        
        # Simple scoring: vulnerabilities are high risk, many open ports = medium risk
        threat_score = min(vulns_count * 20 + ports_count * 2, 100)
        profile.source_scores['shodan'] = threat_score
        
        # Update network info
        profile.set_network_info(
            isp=data.get('isp'),
            organization=data.get('organization'),
            asn=data.get('asn')
        )
        
        # Update geolocation
        profile.set_geolocation(
            country_code=data.get('country_code'),
            city=data.get('city'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        
        # Add open ports
        profile.ports = data.get('ports', [])
        profile.services = data.get('services', [])
        
        # Add vulnerabilities as categories
        for vuln in data.get('vulns', [])[:5]:  # Limit to first 5
            profile.add_category(f'CVE: {vuln}')
        
        # Add tags as categories
        for tag in data.get('tags', [])[:5]:
            profile.add_category(tag.title())
        
        # Add domains to related entities
        for domain in data.get('domains', [])[:10]:
            if domain not in profile.related_entities['domains']:
                profile.related_entities['domains'].append(domain)
        
        # Add hostnames
        for hostname in data.get('hostnames', [])[:10]:
            if hostname not in profile.related_entities['domains']:
                profile.related_entities['domains'].append(hostname)
        
        return profile
