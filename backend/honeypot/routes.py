from flask import Blueprint, request, jsonify
from database.connection import get_db_connection
from ai_engine.threat_engine import evaluate_threat


honeypot_bp = Blueprint("honeypot", __name__)

from services.geoip_service import geoip_service

@honeypot_bp.route("/login", methods=["POST"])
def fake_login():
    ip = get_client_ip()
    username = request.form.get("username")
    password = request.form.get("password")
    user_agent = request.headers.get("User-Agent")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # STEP 1: Detect SQL Injection
        attack_type = "Normal"
        injection_patterns = ["'", "--", "UNION", "SELECT", "OR 1=1"]
        
        # Safe lower-case check
        u_check = (username or "").lower()
        p_check = (password or "").lower()

        for pattern in injection_patterns:
            if pattern.lower() in u_check or pattern.lower() in p_check:
                attack_type = "SQL Injection"
                break

        # STEP 2: Get Country and Insert attack
        if is_private_ip(ip):
            country = "Localhost"
        else:
            country = geoip_service.get_country(ip) or "Unknown"
        
        insert_query = """
            INSERT INTO attacks (ip_address, username_attempted, password_attempted, user_agent, country, attack_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (ip, username, password, user_agent, country, attack_type))
        conn.commit()

        # STEP 2: Calculate risk score
        risk_score = evaluate_threat(ip, country=country)

        # STEP 3: Update the same inserted row
        update_query = """
            UPDATE attacks
            SET risk_score = %s
            WHERE id = LAST_INSERT_ID()
        """

        cursor.execute(update_query, (risk_score,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    return request.remote_addr

def is_private_ip(ip):
    if ip.startswith("127."): return True
    if ip.startswith("10."): return True
    if ip.startswith("192.168."): return True
    if ip.startswith("172."):
        # Check 172.16.x.x to 172.31.x.x
        parts = ip.split(".")
        if len(parts) > 1 and 16 <= int(parts[1]) <= 31:
            return True
    return False
