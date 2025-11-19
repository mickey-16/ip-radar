"""
Helper utility functions
"""
import re
import ipaddress
from datetime import datetime
from typing import Optional

def validate_ip(ip_string: str) -> bool:
    """
    Validate if a string is a valid IP address (IPv4 or IPv6)
    
    Args:
        ip_string: String to validate
        
    Returns:
        bool: True if valid IP address, False otherwise
    """
    try:
        ipaddress.ip_address(ip_string)
        return True
    except ValueError:
        return False

def is_private_ip(ip_string: str) -> bool:
    """
    Check if IP address is private/internal
    
    Args:
        ip_string: IP address string
        
    Returns:
        bool: True if private IP, False otherwise
    """
    try:
        ip = ipaddress.ip_address(ip_string)
        return ip.is_private
    except ValueError:
        return False

def format_timestamp(timestamp: Optional[str] = None) -> str:
    """
    Format timestamp to ISO 8601 format
    
    Args:
        timestamp: Timestamp string or None for current time
        
    Returns:
        str: Formatted timestamp
    """
    if timestamp is None:
        return datetime.utcnow().isoformat() + 'Z'
    
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.isoformat() + 'Z'
    except:
        return datetime.utcnow().isoformat() + 'Z'

def get_risk_emoji(risk_level: str) -> str:
    """
    Get emoji representation of risk level
    
    Args:
        risk_level: Risk level string
        
    Returns:
        str: Emoji representing risk level
    """
    emoji_map = {
        'low': '🟢',
        'medium': '🟡',
        'high': '🟠',
        'critical': '🔴',
        'unknown': '⚪'
    }
    return emoji_map.get(risk_level.lower(), '⚪')

def get_risk_color(risk_level: str) -> str:
    """
    Get color code for risk level
    
    Args:
        risk_level: Risk level string
        
    Returns:
        str: Color code
    """
    color_map = {
        'low': '#28a745',
        'medium': '#ffc107',
        'high': '#fd7e14',
        'critical': '#dc3545',
        'unknown': '#6c757d'
    }
    return color_map.get(risk_level.lower(), '#6c757d')

def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        text: Input text
        
    Returns:
        str: Sanitized text
    """
    # Remove any HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    # Remove special characters except dots and colons (for IPs)
    text = re.sub(r'[^\w\s\.\:]', '', text)
    return text.strip()

def normalize_category(category: str) -> str:
    """
    Normalize threat category names
    
    Args:
        category: Category string
        
    Returns:
        str: Normalized category
    """
    category_map = {
        'malware': 'Malware',
        'botnet': 'Botnet',
        'c2': 'C2',
        'c&c': 'C2',
        'command and control': 'C2',
        'phishing': 'Phishing',
        'spam': 'Spam',
        'proxy': 'Proxy/VPN',
        'vpn': 'Proxy/VPN',
        'tor': 'Tor',
        'scanner': 'Scanner',
        'brute-force': 'Brute Force',
        'ddos': 'DDoS',
        'exploit': 'Exploit'
    }
    
    return category_map.get(category.lower(), category.title())
