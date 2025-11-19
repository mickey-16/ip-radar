"""
TICE - Threat Intelligence Correlation Engine
Main Flask Application
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from io import BytesIO
from dotenv import load_dotenv
from config import config
from core.correlator import ThreatCorrelator
from utils.helpers import validate_ip, is_private_ip, sanitize_input
from ml.predictor import get_predictor
from reports.pdf_generator import PDFReportGenerator

# Load environment variables first
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Enable CORS
CORS(app)

# Initialize Threat Correlator
correlator = ThreatCorrelator(app.config)

# Initialize ML Predictor
ml_predictor = get_predictor()

# Initialize PDF Report Generator
pdf_generator = PDFReportGenerator()

@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Render dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_ip():
    """
    Analyze IP address endpoint
    
    Request JSON:
        {
            "ip_address": "8.8.8.8",
            "use_cache": true
        }
    
    Returns:
        JSON with threat intelligence profile
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data or 'ip_address' not in data:
            return jsonify({
                'error': 'Missing ip_address parameter'
            }), 400
        
        # Sanitize and validate IP
        ip_address = sanitize_input(data['ip_address'])
        
        if not validate_ip(ip_address):
            return jsonify({
                'error': 'Invalid IP address format'
            }), 400
        
        # Check if private IP
        if is_private_ip(ip_address):
            return jsonify({
                'error': 'Cannot analyze private IP addresses',
                'ip_address': ip_address,
                'is_private': True
            }), 400
        
        # Get cache preference (disabled by default for fresh data)
        use_cache = data.get('use_cache', False)
        
        # Analyze IP
        profile = correlator.analyze_ip(ip_address, use_cache=use_cache)
        
        # Get ML prediction if available
        ml_prediction = ml_predictor.predict_from_profile(profile)
        
        # Add ML prediction to response
        response = profile.to_dict()
        response['ml_prediction'] = ml_prediction
        
        # Return threat profile
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({
            'error': 'Internal server error during analysis',
            'details': str(e)
        }), 500

@app.route('/api/summary/<ip_address>', methods=['GET'])
def get_summary(ip_address):
    """
    Get quick summary for an IP address
    
    Args:
        ip_address: IP address in URL path
        
    Returns:
        JSON with summarized threat data
    """
    try:
        # Sanitize and validate IP
        ip_address = sanitize_input(ip_address)
        
        if not validate_ip(ip_address):
            return jsonify({
                'error': 'Invalid IP address format'
            }), 400
        
        # Get summary
        summary = correlator.get_quick_summary(ip_address)
        
        return jsonify(summary), 200
        
    except Exception as e:
        print(f"Summary error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'TICE',
        'version': '1.0.0'
    }), 200

@app.route('/api/ml-predict', methods=['POST'])
def ml_predict():
    """
    Fast ML-based threat prediction endpoint
    Uses pre-trained ML model without API calls
    
    Request JSON:
        {
            "ip_address": "8.8.8.8"
        }
    
    Returns:
        ML prediction with threat score and risk level
    """
    try:
        data = request.get_json()
        
        if not data or 'ip_address' not in data:
            return jsonify({
                'error': 'Missing ip_address parameter'
            }), 400
        
        ip_address = sanitize_input(data['ip_address'])
        
        if not validate_ip(ip_address):
            return jsonify({
                'error': 'Invalid IP address format'
            }), 400
        
        # Quick analysis (using cache if available, otherwise fetch minimal data)
        profile = correlator.analyze_ip(ip_address, use_cache=True)
        
        # Get ML prediction
        ml_prediction = ml_predictor.predict_from_profile(profile)
        
        if not ml_prediction.get('available'):
            return jsonify({
                'error': 'ML model not available',
                'message': ml_prediction.get('message', 'Model not trained'),
                'ip_address': ip_address
            }), 503
        
        # Return combined result
        return jsonify({
            'ip_address': ip_address,
            'ml_prediction': ml_prediction,
            'api_verification': {
                'threat_score': profile.threat_score,
                'risk_level': profile.risk_level,
                'is_malicious': profile.is_malicious,
                'confidence': profile.confidence
            },
            'geolocation': profile.geolocation,
            'network_info': profile.network_info,
            'comparison': {
                'score_difference': abs(ml_prediction['predicted_threat_score'] - profile.threat_score),
                'agreement': ml_prediction['is_malicious'] == profile.is_malicious
            }
        }), 200
        
    except Exception as e:
        print(f"ML Prediction error: {e}")
        return jsonify({
            'error': 'Internal server error during ML prediction',
            'details': str(e)
        }), 500

@app.route('/api/ml-info', methods=['GET'])
def ml_info():
    """Get ML model information and feature importance"""
    if not ml_predictor.is_loaded:
        return jsonify({
            'available': False,
            'message': 'ML model not trained yet'
        }), 200
    
    feature_importance = ml_predictor.get_feature_importance()
    
    return jsonify({
        'available': True,
        'model_type': 'Random Forest',
        'feature_importance': [
            {'feature': feature, 'importance': round(importance, 4)}
            for feature, importance in feature_importance
        ],
        'features_used': [f[0] for f in feature_importance]
    }), 200

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get public configuration information"""
    return jsonify({
        'api_sources': {
            'abuseipdb': bool(app.config['ABUSEIPDB_API_KEY']),
            'virustotal': bool(app.config['VIRUSTOTAL_API_KEY']),
            'ipgeolocation': bool(app.config['IPGEOLOCATION_API_KEY']),
            'greynoise': bool(app.config['GREYNOISE_API_KEY']),
            'shodan': bool(app.config['SHODAN_API_KEY'])
        },
        'scoring_weights': app.config['SCORING_WEIGHTS'],
        'risk_levels': app.config['RISK_LEVELS']
    }), 200

@app.route('/api/download-report/<ip_address>', methods=['GET'])
def download_report(ip_address):
    """
    Download PDF report for an IP address
    
    Args:
        ip_address: IP address in URL path
        
    Returns:
        PDF file download
    """
    try:
        # Sanitize and validate IP
        ip_address = sanitize_input(ip_address)
        
        if not validate_ip(ip_address):
            return jsonify({
                'error': 'Invalid IP address format'
            }), 400
        
        # Check if private IP
        if is_private_ip(ip_address):
            return jsonify({
                'error': 'Cannot generate report for private IP addresses',
                'ip_address': ip_address
            }), 400
        
        # Analyze IP (always fetch fresh data - no cache)
        profile = correlator.analyze_ip(ip_address, use_cache=False)
        
        # Get ML prediction if available
        ml_prediction = ml_predictor.predict_from_profile(profile)
        
        # Prepare data for PDF
        profile_data = profile.to_dict()
        profile_data['ml_prediction'] = ml_prediction
        
        # Generate PDF
        pdf_bytes = pdf_generator.generate_report(profile_data)
        
        # Create BytesIO object
        pdf_buffer = BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        
        # Generate filename
        filename = f"TICE-Report-{ip_address.replace('.', '-')}.pdf"
        
        # Return PDF as downloadable file
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"PDF generation error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': 'Internal server error during PDF generation',
            'details': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('cache', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Run the application
    print("=" * 50)
    print("🛡️  TICE - Threat Intelligence Correlation Engine")
    print("=" * 50)
    print(f"Environment: {env}")
    print(f"Debug Mode: {app.config['DEBUG']}")
    print(f"Server: http://{app.config['HOST']}:{app.config['PORT']}")
    print("=" * 50)
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
