"""
ML-Powered Threat Predictor
Fast IP threat assessment using pre-trained ML models
"""
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ml.train_model import ThreatPredictionModel

class MLThreatPredictor:
    """
    Provides ML-based threat predictions for IP addresses
    Works without API calls - uses only IP metadata
    """
    
    def __init__(self, model_dir=None):
        self.model = ThreatPredictionModel()
        self.is_loaded = False
        
        if model_dir is None:
            model_dir = Path(__file__).parent / 'models'
        
        # Try to load pre-trained model
        try:
            if Path(model_dir).exists():
                self.model.load(model_dir)
                self.is_loaded = True
                print("✅ ML Model loaded successfully")
            else:
                print("⚠️  ML Model not trained yet")
        except Exception as e:
            print(f"⚠️  Could not load ML model: {e}")
    
    def predict_from_profile(self, threat_profile):
        """
        Predict threat level from a ThreatProfile object
        
        Args:
            threat_profile: ThreatProfile instance with geolocation and network data
            
        Returns:
            dict with ML predictions
        """
        if not self.is_loaded:
            return {
                'available': False,
                'message': 'ML model not trained. Run ml/collect_training_data.py and ml/train_model.py'
            }
        
        # Extract metadata from profile
        data = threat_profile.to_dict()
        
        metadata = {
            'country_code': data['geolocation'].get('country_code', 'UNKNOWN'),
            'is_hosting': data['network_info'].get('is_hosting', False),
            'is_vpn': data['network_info'].get('is_vpn', False),
            'is_proxy': data['network_info'].get('is_proxy', False),
            'is_tor': data['network_info'].get('is_tor', False),
            'abuseipdb_score': data['source_scores'].get('abuseipdb', 0),
            'virustotal_score': data['source_scores'].get('virustotal', 0),
            'ipapi_score': data['source_scores'].get('ipapi', 0),
            'num_categories': len(data.get('categories', [])),
            'reports_count': data.get('reports_count', 0)
        }
        
        # Get ML prediction
        prediction = self.model.predict(metadata)
        prediction['available'] = True
        prediction['model_type'] = 'Random Forest'
        
        return prediction
    
    def predict_from_metadata(self, ip_metadata):
        """
        Predict threat level from raw IP metadata
        
        Args:
            ip_metadata: dict with IP metadata (country_code, is_hosting, etc.)
            
        Returns:
            dict with ML predictions
        """
        if not self.is_loaded:
            return {
                'available': False,
                'message': 'ML model not trained'
            }
        
        prediction = self.model.predict(ip_metadata)
        prediction['available'] = True
        prediction['model_type'] = 'Random Forest'
        
        return prediction
    
    def get_feature_importance(self):
        """Get feature importance rankings"""
        if not self.is_loaded:
            return {}
        
        return sorted(
            self.model.feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )

# Global predictor instance
_predictor = None

def get_predictor():
    """Get singleton ML predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = MLThreatPredictor()
    return _predictor
