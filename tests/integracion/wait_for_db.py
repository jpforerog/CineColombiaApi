import os
import time

def wait_db():
    host = os.getenv("DB_HOST", "db")
    port = int(os.getenv("DB_PORT", 3306))
    user = os.getenv("DB_USER", "test_user")
    password = os.getenv("DB_PASS", "test_pass")
    db = os.getenv("DB_NAME", "peliculas_db")

    for i in range(30):
        try:
            import pymysql
            conn = pymysql.connect(host=host, port=port, user=user, password=password, database=db)
            conn.close()
            print("DB lista")
            return
        except Exception as e:
            print(f"Intento {i+1}: DB no lista ({e}), esperando 2s...")
            time.sleep(2)
    raise RuntimeError("No se pudo conectar a la base de datos en el tiempo esperado")

if __name__ == "__main__":
    wait_db()
