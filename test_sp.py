"""
Script para verificar si los stored procedures existen
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from django.db import connection

def verificar_stored_procedures():
    """Verifica si los stored procedures existen"""
    with connection.cursor() as cursor:
        # Verificar procedimientos almacenados
        cursor.execute("""
            SELECT ROUTINE_NAME
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_SCHEMA = 'juego_finanzas'
            AND ROUTINE_TYPE = 'PROCEDURE'
            AND ROUTINE_NAME IN ('verificar_tema_completado', 'obtener_progreso_por_temas')
        """)

        procedures = cursor.fetchall()

        print("=== STORED PROCEDURES ENCONTRADOS ===")
        if procedures:
            for proc in procedures:
                print(f"✓ {proc[0]}")
        else:
            print("❌ No se encontraron los stored procedures necesarios")

        print("\n=== TODOS LOS STORED PROCEDURES EN LA BD ===")
        cursor.execute("""
            SELECT ROUTINE_NAME
            FROM INFORMATION_SCHEMA.ROUTINES
            WHERE ROUTINE_SCHEMA = 'juego_finanzas'
            AND ROUTINE_TYPE = 'PROCEDURE'
            ORDER BY ROUTINE_NAME
        """)

        all_procedures = cursor.fetchall()
        for proc in all_procedures:
            print(f"  - {proc[0]}")

if __name__ == '__main__':
    verificar_stored_procedures()
