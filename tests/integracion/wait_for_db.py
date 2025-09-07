import time
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "db",
    "user": "root",
    "password": "password123",
    "database": "mydb"
}

if __name__ == "__main__":
    while True:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            if conn.is_connected():
                print("✅ DB lista!")
                conn.close()
                break
        except Error as e:
            print("⏳ Esperando DB...")
        time.sleep(2)
