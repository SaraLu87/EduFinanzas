"""
Script para ejecutar los stored procedures en la base de datos MySQL
"""
import mysql.connector
import os

# Configuración de conexión
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456789',
    'database': 'juego_finanzas'
}

def ejecutar_script_sql(archivo_sql):
    """Ejecuta un archivo SQL completo"""
    try:
        # Leer el archivo SQL
        with open(archivo_sql, 'r', encoding='utf-8') as f:
            sql_script = f.read()

        # Conectar a MySQL
        print("Conectando a la base de datos...")
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Dividir el script en statements individuales
        # Necesitamos procesar los delimiters manualmente
        statements = []
        current_statement = []
        delimiter = ';'

        for line in sql_script.split('\n'):
            line = line.strip()

            # Cambiar delimiter
            if line.startswith('DELIMITER'):
                new_delimiter = line.split()[-1]
                delimiter = new_delimiter
                continue

            # Saltar comentarios y líneas vacías
            if not line or line.startswith('--'):
                continue

            current_statement.append(line)

            # Si la línea termina con el delimiter actual
            if line.endswith(delimiter):
                statement = ' '.join(current_statement)
                # Remover el delimiter del final
                statement = statement[:-len(delimiter)].strip()
                if statement and not statement.startswith('USE'):
                    statements.append(statement)
                current_statement = []

        # Ejecutar cada statement
        print(f"\nEjecutando {len(statements)} statements...\n")
        for i, statement in enumerate(statements, 1):
            try:
                # Mostrar solo el inicio del statement
                preview = statement[:80] + '...' if len(statement) > 80 else statement
                print(f"{i}. Ejecutando: {preview}")

                cursor.execute(statement)
                conn.commit()
                print(f"   ✓ Completado\n")

            except mysql.connector.Error as err:
                print(f"   ✗ Error: {err}\n")
                # Continuar con el siguiente statement

        # Verificar procedimientos creados
        print("\n" + "="*60)
        print("VERIFICANDO STORED PROCEDURES CREADOS:")
        print("="*60 + "\n")

        cursor.execute("""
            SELECT ROUTINE_NAME, CREATED, LAST_ALTERED
            FROM information_schema.ROUTINES
            WHERE ROUTINE_SCHEMA = 'juego_finanzas'
            AND ROUTINE_TYPE = 'PROCEDURE'
            AND ROUTINE_NAME IN (
                'obtener_perfil_por_usuario',
                'iniciar_reto',
                'obtener_retos_por_tema',
                'solucionar_reto',
                'calcular_progreso_usuario'
            )
            ORDER BY ROUTINE_NAME
        """)

        results = cursor.fetchall()

        if results:
            print(f"✓ Se encontraron {len(results)} procedimientos:\n")
            for row in results:
                nombre, created, altered = row
                print(f"  • {nombre}")
                print(f"    Creado: {created}")
                print(f"    Modificado: {altered}\n")
        else:
            print("✗ No se encontraron los procedimientos esperados\n")

        cursor.close()
        conn.close()

        print("="*60)
        print("PROCESO COMPLETADO")
        print("="*60)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo_sql}")
    except mysql.connector.Error as err:
        print(f"Error de MySQL: {err}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    archivo = "stored_procedures_user_features.sql"
    print("="*60)
    print("EJECUTANDO STORED PROCEDURES")
    print("="*60)
    print(f"Archivo: {archivo}\n")
    ejecutar_script_sql(archivo)
