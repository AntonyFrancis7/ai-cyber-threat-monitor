from database.connection import get_db_connection

def extract_features(ip):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Attempts in last 1 minute
    cursor.execute("""
        SELECT COUNT(*) FROM attacks
        WHERE ip_address = %s
        AND created_at >= NOW() - INTERVAL 1 MINUTE
    """, (ip,))
    
    attempts_last_1min = cursor.fetchone()[0]

    # Attempts in last 10 minutes
    cursor.execute("""
        SELECT COUNT(*) FROM attacks
        WHERE ip_address = %s
        AND created_at >= NOW() - INTERVAL 10 MINUTE
    """, (ip,))
    
    attempts_last_10min = cursor.fetchone()[0]

    # Total attempts
    cursor.execute("""
        SELECT COUNT(*) FROM attacks
        WHERE ip_address = %s
    """, (ip,))
    
    total_attempts = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "attempts_last_1min": attempts_last_1min,
        "attempts_last_10min": attempts_last_10min,
        "total_attempts": total_attempts
    }
