"""
Threat Scoring Engine
Calculates weighted threat scores from multiple intelligence sources
"""
from typing import Dict
from models.threat_profile import ThreatProfile

class ThreatScorer:
    """
    Calculates comprehensive threat scores using weighted algorithms
    """
    
    # Default scoring weights (can be configured)
    DEFAULT_WEIGHTS = {
        'abuseipdb': 0.30,
        'virustotal': 0.25,
        'ipgeolocation': 0.20,
        'greynoise': 0.15,
        'shodan': 0.10
    }
    
    def __init__(self, weights: Dict[str, float] = None):
        """
        Initialize threat scorer
        
        Args:
            weights: Custom scoring weights (optional)
        """
        self.weights = weights or self.DEFAULT_WEIGHTS
    
    def calculate_threat_score(self, profile: ThreatProfile) -> float:
        """
        Calculate weighted threat score from all sources
        
        Args:
            profile: ThreatProfile with source scores
            
        Returns:
            float: Final threat score (0-100)
        """
        # Check if IP is whitelisted in AbuseIPDB
        is_whitelisted = False
        if 'abuseipdb' in profile.sources:
            abuseipdb_data = profile.sources.get('abuseipdb', {})
            if isinstance(abuseipdb_data, dict):
                # Check nested 'data' structure
                if 'data' in abuseipdb_data:
                    is_whitelisted = abuseipdb_data['data'].get('isWhitelisted', False)
                else:
                    is_whitelisted = abuseipdb_data.get('isWhitelisted', False)
        
        total_score = 0
        total_weight = 0
        
        # Calculate weighted average from source scores
        for source, weight in self.weights.items():
            if source in profile.source_scores:
                score = profile.source_scores[source]
                total_score += score * weight
                total_weight += weight
        
        # If we have any scores, calculate weighted average
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            final_score = 0
        
        # Check for MITRE ATT&CK / APT attribution
        # This is CRITICAL intelligence that overrides low base scores
        mitre_boost = self._calculate_mitre_threat_boost(profile.mitre_intelligence)
        
        # For NON-whitelisted IPs: apply MITRE boost normally
        if not is_whitelisted:
            if mitre_boost > 0:
                final_score = max(final_score, mitre_boost)
        
        # Apply category-based modifiers only if not whitelisted
        if not is_whitelisted:
            final_score = self._apply_category_modifiers(final_score, profile.categories)
        
        # Apply network-based modifiers only if not whitelisted
        if not is_whitelisted:
            final_score = self._apply_network_modifiers(final_score, profile.network_info)
        
        # For whitelisted IPs, apply special capping rules
        if is_whitelisted:
            # Only allow MITRE boost if there's ACTUAL APT attribution
            # (not just OTX pulses or low-confidence intelligence)
            has_real_apt = (
                profile.mitre_intelligence.get('has_apt_attribution', False) and
                len(profile.mitre_intelligence.get('threat_actors', [])) > 0
            )
            
            if has_real_apt:
                # Whitelisted IP with confirmed APT groups - very suspicious!
                # This could indicate compromise of trusted infrastructure
                final_score = max(final_score, mitre_boost)
            else:
                # Whitelisted IP with no real APT - cap at LOW risk
                # Ignore any modifiers, categories, network info
                final_score = min(final_score, 5)  # Strict cap for trusted IPs
        
        # Ensure score is within 0-100 range
        return max(0, min(100, final_score))
    
    def _apply_category_modifiers(self, score: float, categories: list) -> float:
        """
        Apply modifiers based on threat categories
        
        Args:
            score: Current threat score
            categories: List of threat categories
            
        Returns:
            Modified threat score
        """
        # If base score is very low and there are few categories, be less aggressive
        # This prevents over-penalizing legitimate services
        category_count = len(categories)
        
        # High-risk category modifiers (reduced from previous values)
        high_risk_categories = {
            'C2': 20,
            'Botnet': 15,
            'Ransomware': 25,
            'Known Attacker': 20,
            'Malware': 15,
            'Phishing': 15,
            'Exploited Host': 15
        }
        
        # Medium-risk category modifiers (reduced)
        medium_risk_categories = {
            'Spam': 3,
            'Email Spam': 3,
            'Web Spam': 2,
            'Brute Force': 8,
            'SSH Brute Force': 10,
            'Scanner': 4,
            'Port Scan': 4,
            'DDoS': 10,
            'Web App Attack': 6,
            'Hacking': 12,
            'Fraud': 10
        }
        
        # Low-risk category modifiers (informational, minimal impact)
        low_risk_categories = {
            'Hosting Provider': 0,  # Not a threat
            'Proxy': 2,
            'VPN': 2,
            'Crawler': 0,  # Not a threat
            'Bot': 1
        }
        
        modifier = 0
        high_risk_count = 0
        
        # Apply modifiers
        for category in categories:
            if category in high_risk_categories:
                modifier += high_risk_categories[category]
                high_risk_count += 1
            elif category in medium_risk_categories:
                modifier += medium_risk_categories[category]
            elif category in low_risk_categories:
                modifier += low_risk_categories[category]
        
        # If we have multiple categories but low base score,
        # reduce the modifier impact (likely false positives)
        if score < 10 and category_count > 5:
            modifier *= 0.3  # Reduce by 70%
        elif score < 20 and high_risk_count == 0:
            modifier *= 0.5  # Reduce by 50% if no high-risk categories
        
        return score + modifier
    
    def _apply_network_modifiers(self, score: float, network_info: Dict) -> float:
        """
        Apply modifiers based on network characteristics
        
        Args:
            score: Current threat score
            network_info: Network information dictionary
            
        Returns:
            Modified threat score
        """
        modifier = 0
        
        # Tor exit nodes are high risk
        if network_info.get('is_tor'):
            modifier += 15
        
        # Proxies/VPNs increase anonymity risk, but only moderately
        # Many legitimate services use these
        if network_info.get('is_proxy') or network_info.get('is_vpn'):
            # Only add risk if base score suggests malicious activity
            if score > 20:
                modifier += 8
            else:
                modifier += 2
        
        # Hosting providers alone are NOT a threat indicator
        # Many legitimate services (CDNs, cloud services) are hosted
        # Only add minimal risk if there are other threat indicators
        if network_info.get('is_hosting'):
            if score > 30:  # Only if other threats exist
                modifier += 3
            # Otherwise, add nothing
        
        return score + modifier
    
    def _calculate_mitre_threat_boost(self, mitre_intelligence: Dict) -> float:
        """
        Calculate threat score boost based on MITRE ATT&CK intelligence
        APT groups and nation-state actors are critical threats
        
        Args:
            mitre_intelligence: MITRE intelligence dictionary
            
        Returns:
            Threat score boost (0-100)
        """
        if not mitre_intelligence or not mitre_intelligence.get('found'):
            return 0
        
        threat_score = 0
        
        # APT / Threat Actor attribution is CRITICAL
        # Support both mock database format (apt_groups) and OTX format (threat_actors)
        apt_groups = mitre_intelligence.get('apt_groups', [])
        threat_actors = mitre_intelligence.get('threat_actors', [])
        
        if (apt_groups and len(apt_groups) > 0) or (threat_actors and len(threat_actors) > 0):
            # Base score for APT attribution
            threat_score = 75  # HIGH risk baseline for any APT link
            
            # Mock database APTs are always CRITICAL (verified national/state-level threats)
            if apt_groups:
                threat_score = 90  # CRITICAL for mock database APTs
                
                # Check country attribution from mock database
                country = mitre_intelligence.get('country')
                if country in ['China', 'Russia', 'Iran', 'North Korea', 'Pakistan']:
                    threat_score = 95  # Maximum for hostile nation-state
            
            # Check for nation-state attribution from OTX data
            elif threat_actors:
                nation_states = ['China', 'Russia', 'Iran', 'North Korea', 'Unknown']
                has_nation_state = any(
                    actor.get('attribution') in nation_states 
                    for actor in threat_actors
                )
                
                if has_nation_state:
                    threat_score = 85  # CRITICAL for nation-state actors
                
                # Multiple APT groups = higher threat
                if len(threat_actors) >= 2:
                    threat_score = min(threat_score + 10, 95)
        
        # C2 Server or Botnet infrastructure
        if mitre_intelligence.get('is_c2_server'):
            threat_score = max(threat_score, 80)
        
        if mitre_intelligence.get('is_botnet'):
            threat_score = max(threat_score, 75)
        
        # Malware families indicate active infrastructure
        malware_count = len(mitre_intelligence.get('malware_families', []))
        if malware_count > 0:
            # Add moderate boost for malware presence
            if threat_score == 0:  # No APT attribution yet
                threat_score = 40 + min(malware_count * 5, 30)
            else:
                threat_score = min(threat_score + (malware_count * 2), 95)
        
        # OTX pulses indicate active threat intelligence
        # BUT: Many legitimate services (Google DNS, Cloudflare) appear in OTX
        # Only boost if we have OTHER evidence of malicious activity
        otx_count = mitre_intelligence.get('otx_pulse_count', 0)
        if otx_count > 5:
            # Only apply OTX boost if we already have some threat score
            # Don't boost just from OTX alone (prevents false positives on trusted services)
            if threat_score >= 40:  # Must have APT/malware/C2 evidence first
                threat_score = min(threat_score + 5, 95)
            # If threat_score is 0, OTX pulses alone are NOT enough
        
        # High confidence MITRE data
        confidence = mitre_intelligence.get('confidence', '').upper()
        if confidence == 'HIGH' and threat_score > 0:
            # Boost score for high-confidence attribution
            threat_score = min(threat_score + 5, 95)
        
        return threat_score
    
    def calculate_confidence(self, profile: ThreatProfile) -> float:
        """
        Calculate confidence level based on source agreement
        
        Args:
            profile: ThreatProfile with source scores
            
        Returns:
            float: Confidence score (0-100)
        """
        scores = list(profile.source_scores.values())
        
        if len(scores) < 2:
            # Low confidence with only one source
            return 30
        
        # Calculate variance in scores
        avg_score = sum(scores) / len(scores)
        variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
        
        # Lower variance = higher confidence
        # High variance = sources disagree
        if variance < 100:
            confidence = 90
        elif variance < 400:
            confidence = 70
        elif variance < 900:
            confidence = 50
        else:
            confidence = 30
        
        # Increase confidence with more sources
        source_bonus = min((len(scores) - 1) * 5, 20)
        confidence += source_bonus
        
        return min(100, confidence)
    
    def score_profile(self, profile: ThreatProfile):
        """
        Calculate all scores and update the profile
        
        Args:
            profile: ThreatProfile to score
        """
        # Calculate threat score
        profile.threat_score = self.calculate_threat_score(profile)
        
        # Calculate confidence
        profile.confidence = self.calculate_confidence(profile)
        
        # Determine risk level
        profile.calculate_risk_level()
