from flask import Blueprint, jsonify
from database.connection import get_db_connection

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/stats/total-attacks", methods=["GET"])
def total_attacks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM attacks")
        total = cursor.fetchone()[0]
        return jsonify({"total_attacks": total})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

@analytics_bp.route("/stats/top-ips", methods=["GET"])
def top_ips():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT ip_address, COUNT(*) as count 
            FROM attacks 
            GROUP BY ip_address 
            ORDER BY count DESC 
            LIMIT 10
        """
        cursor.execute(query)
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

@analytics_bp.route("/stats/top-countries", methods=["GET"])
def top_countries():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT country, COUNT(*) as count 
            FROM attacks 
            WHERE country IS NOT NULL
            GROUP BY country 
            ORDER BY count DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

@analytics_bp.route("/stats/high-risk", methods=["GET"])
def high_risk_attacks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM attacks WHERE risk_score > 70 ORDER BY created_at DESC LIMIT 50"
        cursor.execute(query)
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

@analytics_bp.route("/stats/attacks-per-hour", methods=["GET"])
def attacks_per_hour():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # MySQL syntax for date formatting
        query = """
            SELECT DATE_FORMAT(created_at, '%Y-%m-%d %H:00:00') as hour, COUNT(*) as count
            FROM attacks
            GROUP BY hour
            ORDER BY hour DESC
            LIMIT 24
        """
        cursor.execute(query)
        data = cursor.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
