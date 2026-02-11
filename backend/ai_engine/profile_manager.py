import mysql.connector
from database.connection import get_db_connection
from datetime import datetime

def update_ip_profile(ip_address, risk_score):
    """
    Updates or inserts the IP profile based on the latest attack.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if IP exists
        cursor.execute("SELECT total_attempts, threat_level, is_blocked FROM ip_profile WHERE ip_address = %s", (ip_address,))
        result = cursor.fetchone()

        if result:
            total_attempts, current_threat_level, is_blocked = result
            total_attempts += 1
            
            # Determine new threat level
            new_threat_level = calculate_threat_level(risk_score)
            
            # Determine if should be blocked
            if risk_score > 80 or total_attempts > 100:
                is_blocked = True

            update_query = """
                UPDATE ip_profile
                SET total_attempts = %s, last_attempt = %s, threat_level = %s, is_blocked = %s
                WHERE ip_address = %s
            """
            cursor.execute(update_query, (total_attempts, datetime.now(), new_threat_level, is_blocked, ip_address))
        
        else:
            # Insert new profile
            total_attempts = 1
            threat_level = calculate_threat_level(risk_score)
            is_blocked = False
            
            if risk_score > 80:
                is_blocked = True

            insert_query = """
                INSERT INTO ip_profile (ip_address, total_attempts, last_attempt, threat_level, is_blocked)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (ip_address, total_attempts, datetime.now(), threat_level, is_blocked))

        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error updating IP profile: {err}")
    finally:
        cursor.close()
        conn.close()

def calculate_threat_level(risk_score):
    if risk_score <= 30:
        return "Low"
    elif risk_score <= 70:
        return "Medium"
    else:
        return "High"
