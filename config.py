"""
Configuration settings for TICE application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Server Settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # API Keys
    ABUSEIPDB_API_KEY = os.getenv('ABUSEIPDB_API_KEY', '')
    VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY', '')
    IPQUALITYSCORE_API_KEY = os.getenv('IPQUALITYSCORE_API_KEY', '')
    SHODAN_API_KEY = os.getenv('SHODAN_API_KEY', '')
    GREYNOISE_API_KEY = os.getenv('GREYNOISE_API_KEY', '')
    IPGEOLOCATION_API_KEY = os.getenv('IPGEOLOCATION_API_KEY', '')
    ALIENVAULT_OTX_API_KEY = os.getenv('ALIENVAULT_OTX_API_KEY', '')  # NEW: For MITRE/APT intelligence
    
    # Cache Settings
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 3600  # 1 hour
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "100 per hour"
    
    # Threat Scoring Weights
    SCORING_WEIGHTS = {
        'abuseipdb': 0.30,      # 30%
        'virustotal': 0.25,      # 25%
        'ipqualityscore': 0.20,  # 20%
        'shodan': 0.15,          # 15%
        'ipapi': 0.10,           # 10%
        'greynoise': 0.00
    }
    
    # Risk Level Thresholds
    RISK_LEVELS = {
        'low': (0, 20),
        'medium': (21, 50),
        'high': (51, 75),
        'critical': (76, 100)
    }
    
    # API Timeouts (seconds)
    API_TIMEOUT = 10
    
    # Maximum concurrent API calls
    MAX_WORKERS = 5

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
