import pymysql
from pymysql.cursors import DictCursor

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",        # tu usuario de MySQL
        password="Bicho777#",  # cambia esto
        database="juego_finanzas_version_2",  # cambia por el nombre de tu base
        cursorclass=DictCursor
    )

# 🔍 prueba inmediata
if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ Conexión exitosa a la base de datos MySQL")
        conn.close()
    except Exception as e:
        print("❌ Error al conectar:", e)
