from ai_engine.feature_extractor import extract_features
from ai_engine.rule_engine import calculate_rule_score, get_country_risk_score
from ai_engine.profile_manager import update_ip_profile
from ai_engine.ml_engine import anomaly_detector

def evaluate_threat(ip, country=None):
    features = extract_features(ip)
    rule_score = calculate_rule_score(features)
    
    if country:
        rule_score += get_country_risk_score(country)
    
    # ML Scoring
    # Prediction: 1 (Normal), -1 (Anomaly)
    prediction = anomaly_detector.predict(features)
    ml_score = 100 if prediction == -1 else 0
    
    # Hybrid Scoring
    final_score = int((rule_score * 0.6) + (ml_score * 0.4))
    
    # Update IP profile
    update_ip_profile(ip, final_score)
    
    return final_score
