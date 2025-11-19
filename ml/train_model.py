"""
ML Model Training Script
Trains Random Forest classifier for IP threat prediction
"""
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder
import json

class ThreatPredictionModel:
    """ML Model for predicting IP threat levels"""
    
    def __init__(self):
        self.classifier = None  # For malicious/benign classification
        self.regressor = None  # For threat score prediction
        self.label_encoders = {}
        self.feature_names = []
        self.feature_importance = {}
        
    def prepare_features(self, df, is_training=True):
        """Prepare features for ML model"""
        # Select features
        feature_columns = [
            'country_code', 'is_hosting', 'is_vpn', 'is_proxy', 'is_tor',
            'abuseipdb_score', 'virustotal_score', 'ipapi_score',
            'num_categories', 'reports_count'
        ]
        
        X = df[feature_columns].copy()
        
        # Encode categorical features
        categorical_columns = ['country_code']
        
        for col in categorical_columns:
            if is_training:
                # Create and fit label encoder
                le = LabelEncoder()
                # Handle unknown categories
                unique_values = X[col].fillna('UNKNOWN').astype(str).unique()
                le.fit(list(unique_values) + ['UNKNOWN'])
                self.label_encoders[col] = le
            
            # Transform
            X[col] = X[col].fillna('UNKNOWN').astype(str)
            # Handle unseen categories
            X[col] = X[col].apply(lambda x: x if x in self.label_encoders[col].classes_ else 'UNKNOWN')
            X[col] = self.label_encoders[col].transform(X[col])
        
        # Fill missing values
        X = X.fillna(0)
        
        # Convert boolean to int
        bool_columns = ['is_hosting', 'is_vpn', 'is_proxy', 'is_tor']
        for col in bool_columns:
            X[col] = X[col].astype(int)
        
        self.feature_names = feature_columns
        return X
    
    def train(self, csv_file):
        """Train both classification and regression models"""
        print("=" * 60)
        print("🤖 Training ML Models")
        print("=" * 60)
        
        # Load data
        df = pd.read_csv(csv_file)
        print(f"\n📊 Loaded {len(df)} samples")
        print(f"   - Malicious: {len(df[df['label'] == 'malicious'])}")
        print(f"   - Benign: {len(df[df['label'] == 'benign'])}")
        
        # Prepare features and targets
        X = self.prepare_features(df, is_training=True)
        y_class = (df['label'] == 'malicious').astype(int)  # Binary classification
        y_score = df['threat_score']  # Regression
        
        # Split data
        X_train, X_test, y_class_train, y_class_test, y_score_train, y_score_test = train_test_split(
            X, y_class, y_score, test_size=0.2, random_state=42, stratify=y_class
        )
        
        print(f"\n📈 Training set: {len(X_train)} samples")
        print(f"📊 Test set: {len(X_test)} samples")
        
        # Train classifier
        print("\n🎯 Training Classification Model...")
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.classifier.fit(X_train, y_class_train)
        
        # Evaluate classifier
        y_pred_class = self.classifier.predict(X_test)
        print("\n📊 Classification Results:")
        print(classification_report(y_class_test, y_pred_class, 
                                     target_names=['Benign', 'Malicious']))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_class_test, y_pred_class))
        
        # Train regressor
        print("\n🎯 Training Regression Model (Threat Score)...")
        self.regressor = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.regressor.fit(X_train, y_score_train)
        
        # Evaluate regressor
        y_pred_score = self.regressor.predict(X_test)
        mae = mean_absolute_error(y_score_test, y_pred_score)
        r2 = r2_score(y_score_test, y_pred_score)
        print(f"\n📊 Regression Results:")
        print(f"   Mean Absolute Error: {mae:.2f}")
        print(f"   R² Score: {r2:.3f}")
        
        # Feature importance
        self.feature_importance = dict(zip(
            self.feature_names,
            self.classifier.feature_importances_
        ))
        
        print("\n🔍 Top Feature Importance:")
        for feature, importance in sorted(self.feature_importance.items(), 
                                          key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {feature}: {importance:.4f}")
        
        return {
            'classifier_accuracy': self.classifier.score(X_test, y_class_test),
            'regressor_mae': mae,
            'regressor_r2': r2
        }
    
    def predict(self, ip_metadata):
        """Predict threat level for an IP"""
        # Convert to DataFrame
        df = pd.DataFrame([ip_metadata])
        
        # Prepare features
        X = self.prepare_features(df, is_training=False)
        
        # Predict classification
        is_malicious_prob = self.classifier.predict_proba(X)[0][1]  # Probability of being malicious
        is_malicious = self.classifier.predict(X)[0]
        
        # Predict threat score
        threat_score = self.regressor.predict(X)[0]
        threat_score = max(0, min(100, threat_score))  # Clamp to 0-100
        
        # Determine risk level
        if threat_score <= 20:
            risk_level = 'low'
        elif threat_score <= 50:
            risk_level = 'medium'
        elif threat_score <= 75:
            risk_level = 'high'
        else:
            risk_level = 'critical'
        
        return {
            'predicted_threat_score': round(threat_score, 2),
            'predicted_risk_level': risk_level,
            'is_malicious': bool(is_malicious),
            'malicious_probability': round(is_malicious_prob * 100, 2),
            'confidence': round(max(is_malicious_prob, 1 - is_malicious_prob) * 100, 2)
        }
    
    def save(self, output_dir):
        """Save trained model"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Save models
        joblib.dump(self.classifier, output_dir / 'classifier.pkl')
        joblib.dump(self.regressor, output_dir / 'regressor.pkl')
        joblib.dump(self.label_encoders, output_dir / 'label_encoders.pkl')
        
        # Save metadata
        metadata = {
            'feature_names': self.feature_names,
            'feature_importance': self.feature_importance
        }
        with open(output_dir / 'model_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n✅ Model saved to: {output_dir}")
    
    def load(self, model_dir):
        """Load trained model"""
        model_dir = Path(model_dir)
        
        self.classifier = joblib.load(model_dir / 'classifier.pkl')
        self.regressor = joblib.load(model_dir / 'regressor.pkl')
        self.label_encoders = joblib.load(model_dir / 'label_encoders.pkl')
        
        with open(model_dir / 'model_metadata.json', 'r') as f:
            metadata = json.load(f)
            self.feature_names = metadata['feature_names']
            self.feature_importance = metadata['feature_importance']
        
        print(f"✅ Model loaded from: {model_dir}")

if __name__ == '__main__':
    # Train model
    model = ThreatPredictionModel()
    
    training_data = Path(__file__).parent / 'training_data.csv'
    if not training_data.exists():
        print("❌ Training data not found!")
        print("   Run: python ml/collect_training_data.py")
        exit(1)
    
    # Train
    metrics = model.train(training_data)
    
    # Save
    model_dir = Path(__file__).parent / 'models'
    model.save(model_dir)
    
    print("\n" + "=" * 60)
    print("✅ Training Complete!")
    print("=" * 60)
