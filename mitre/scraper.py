"""
MITRE ATT&CK Web Scraper
Scrapes threat group profiles from attack.mitre.org
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re


class MITREAttackScraper:
    """
    Scraper for MITRE ATT&CK framework website
    Extracts detailed threat group profiles
    """
    
    BASE_URL = "https://attack.mitre.org"
    
    # Known APT group mappings (APT name → MITRE Group ID)
    GROUP_MAPPINGS = {
        'apt28': 'G0007',
        'apt29': 'G0016',
        'apt1': 'G0006',
        'apt3': 'G0022',
        'apt12': 'G0005',
        'apt16': 'G0023',
        'apt17': 'G0025',
        'apt18': 'G0026',
        'apt19': 'G0073',
        'apt30': 'G0013',
        'apt32': 'G0050',
        'apt33': 'G0064',
        'apt34': 'G0057',
        'apt37': 'G0067',
        'apt38': 'G0082',
        'apt39': 'G0087',
        'apt41': 'G0096',
        'lazarus': 'G0032',
        'fancy bear': 'G0007',
        'cozy bear': 'G0016',
        'equation group': 'G0020',
        # Iranian APT groups
        'muddywater': 'G0069',
        'static kitten': 'G0069',  # Static Kitten is associated with MuddyWater
        'earth vetala': 'G1006',   # Earth Vetala/MuddyC2
        # Other groups
        'temp.zagros': 'G0069',    # Another name for MuddyWater
    }
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_group_profile(self, group_name: str) -> Dict:
        """
        Get detailed profile for a threat group
        
        Args:
            group_name: Name of threat group (e.g., 'APT28', 'Lazarus')
            
        Returns:
            Dictionary with group profile data
        """
        try:
            # Find MITRE group ID
            group_id = self._find_group_id(group_name)
            
            if not group_id:
                return self._empty_profile()
            
            # Scrape group page
            url = f"{self.BASE_URL}/groups/{group_id}/"
            
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Extract profile data
            profile = self._parse_group_page(soup, group_id, group_name)
            
            return profile
            
        except requests.RequestException as e:
            print(f"MITRE scraping error for {group_name}: {e}")
            return self._empty_profile()
        except Exception as e:
            print(f"MITRE parsing error: {e}")
            return self._empty_profile()
    
    def _find_group_id(self, group_name: str) -> Optional[str]:
        """Find MITRE group ID from group name"""
        group_lower = group_name.lower().strip()
        
        # Direct mapping
        if group_lower in self.GROUP_MAPPINGS:
            return self.GROUP_MAPPINGS[group_lower]
        
        # Try to extract APT number
        apt_match = re.search(r'apt\s*(\d+)', group_lower)
        if apt_match:
            apt_num = apt_match.group(1)
            apt_key = f'apt{apt_num}'
            if apt_key in self.GROUP_MAPPINGS:
                return self.GROUP_MAPPINGS[apt_key]
        
        return None
    
    def _parse_group_page(self, soup: BeautifulSoup, group_id: str, group_name: str) -> Dict:
        """Parse MITRE group page HTML"""
        
        profile = {
            'source': 'mitre_attack',
            'found': True,
            'group_id': group_id,
            'group_name': group_name,
            'aliases': [],
            'description': '',
            'techniques': [],
            'software': [],
            'campaigns': [],
            'targets': [],
            'attribution': None
        }
        
        # Extract description
        desc_div = soup.find('div', class_='description-body')
        if desc_div:
            # Get first paragraph
            paragraphs = desc_div.find_all('p')
            if paragraphs:
                profile['description'] = paragraphs[0].get_text().strip()[:500]  # First 500 chars
        
        # Extract aliases
        alias_section = soup.find('div', string=re.compile('Associated Groups', re.I))
        if alias_section:
            alias_content = alias_section.find_next('div', class_='values')
            if alias_content:
                aliases = [a.get_text().strip() for a in alias_content.find_all('a')]
                profile['aliases'] = aliases
        
        # Extract techniques used
        techniques_table = soup.find('table', class_='techniques-used')
        if techniques_table:
            technique_rows = techniques_table.find_all('tr')[1:]  # Skip header
            for row in technique_rows[:10]:  # Limit to 10 techniques
                cells = row.find_all('td')
                if len(cells) >= 2:
                    tech_id_link = cells[0].find('a')
                    tech_name = cells[1].get_text().strip()
                    
                    if tech_id_link:
                        tech_id = tech_id_link.get_text().strip()
                        profile['techniques'].append({
                            'id': tech_id,
                            'name': tech_name
                        })
        
        # Extract software/malware
        software_section = soup.find('h2', string=re.compile('Software', re.I))
        if software_section:
            software_table = software_section.find_next('table')
            if software_table:
                software_rows = software_table.find_all('tr')[1:]  # Skip header
                for row in software_rows[:10]:  # Limit to 10
                    cells = row.find_all('td')
                    if cells:
                        sw_link = cells[0].find('a')
                        if sw_link:
                            profile['software'].append(sw_link.get_text().strip())
        
        # Try to extract attribution from description
        desc_text = profile['description'].lower()
        if 'russia' in desc_text or 'gru' in desc_text:
            profile['attribution'] = 'Russia'
        elif 'china' in desc_text or 'prc' in desc_text:
            profile['attribution'] = 'China'
        elif 'north korea' in desc_text or 'dprk' in desc_text:
            profile['attribution'] = 'North Korea'
        elif 'iran' in desc_text:
            profile['attribution'] = 'Iran'
        
        return profile
    
    def _empty_profile(self) -> Dict:
        """Return empty profile when scraping fails"""
        return {
            'source': 'mitre_attack',
            'found': False,
            'group_id': None,
            'group_name': None,
            'aliases': [],
            'description': '',
            'techniques': [],
            'software': [],
            'campaigns': [],
            'targets': [],
            'attribution': None
        }
