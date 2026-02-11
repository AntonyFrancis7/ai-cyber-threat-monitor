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
        cursor.execute("SELECT ip_address, country FROM attacks ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"DB Error: {e}")
        return None

def test_localhost_detection():
    print("\n--- Testing Localhost Detection ---")
    data = {"username": "admin", "password": "password123"}
    try:
        # Request from localhost (which is what runs this script)
        requests.post(URL, data=data)
        latest = check_db_latest()
        if latest:
            print(f"IP: {latest['ip_address']}, Country: {latest['country']}")
            if latest['country'] == "Localhost":
                print("✅ Correctly identified as 'Localhost'")
            else:
                print(f"❌ Failed. Expected 'Localhost', got '{latest['country']}'")
        else:
            print("❌ No data found in DB")
    except Exception as e:
        print(f"Request Error: {e}")

if __name__ == "__main__":
    test_localhost_detection()
