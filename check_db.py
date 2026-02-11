
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="threat_monitor"
    )

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DESCRIBE ip_profile")
    columns = [row[0] for row in cursor.fetchall()]
    print(f"Table 'ip_profile' exists with columns: {columns}")
    
    # Check if country column exists in attacks
    cursor.execute("DESCRIBE attacks")
    attack_columns = [row[0] for row in cursor.fetchall()]
    if 'country' in attack_columns:
        print("Column 'country' exists in 'attacks' table.")
    else:
        print("Column 'country' MISSING in 'attacks' table.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
