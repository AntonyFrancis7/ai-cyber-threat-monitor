import requests
import mysql.connector

# Configuration
URL = "http://localhost:5000/login"
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "threat_monitor"
}

def check_db_latest():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM attacks ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"DB Error: {e}")
        return None

def test_normal_login():
    print("\n--- Testing Normal Login ---")
    data = {"username": "admin", "password": "password123"}
    try:
        requests.post(URL, data=data)
        latest = check_db_latest()
        if latest and latest['attack_type'] == "Normal":
            print("✅ Normal Login: Correctly identified as 'Normal'")
        else:
            print(f"❌ Normal Login: Failed. Got {latest.get('attack_type') if latest else 'None'}")
    except Exception as e:
        print(f"Request Error: {e}")

def test_sql_injection():
    print("\n--- Testing SQL Injection ---")
    payloads = [
        ("admin' OR '1'='1", "pass"),
        ("admin", "' OR '1'='1"),
        ("admin", "UNION SELECT"),
        ("admin --", "pass")
    ]
    
    for user, pwd in payloads:
        data = {"username": user, "password": pwd}
        try:
            requests.post(URL, data=data)
            latest = check_db_latest()
            print(f"Payload: User='{user}', Pass='{pwd}' -> Type: {latest.get('attack_type') if latest else 'None'}")
            if latest and latest['attack_type'] == "SQL Injection":
                print("✅ Correctly identified as 'SQL Injection'")
            else:
                print("❌ Failed detection")
        except Exception as e:
            print(f"Request Error: {e}")

if __name__ == "__main__":
    print("Running Verification Tests...")
    test_normal_login()
    test_sql_injection()
