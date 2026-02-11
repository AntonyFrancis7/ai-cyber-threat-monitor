HIGH_RISK_COUNTRIES = {"Russia", "China", "North Korea", "Iran", "Unknown"}

def calculate_rule_score(features):
    risk = 0

    if features["attempts_last_1min"] > 5:
        risk += 40

    if features["attempts_last_10min"] > 15:
        risk += 30

    if features["total_attempts"] > 50:
        risk += 30

    return risk

def get_country_risk_score(country):
    if country in HIGH_RISK_COUNTRIES:
        return 10
    return 0
