"""
Script para probar el SP iniciar_reto
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from django.db import connection

def test_iniciar_reto():
    """Prueba el stored procedure iniciar_reto"""

    # Primero, obtener datos de prueba
    with connection.cursor() as cursor:
        # Obtener el primer perfil
        cursor.execute("SELECT id_perfil, monedas FROM perfiles LIMIT 1")
        perfil = cursor.fetchone()

        if not perfil:
            print("No hay perfiles en la base de datos")
            return

        id_perfil = perfil[0]
        monedas = perfil[1]

        print(f"Perfil de prueba: ID={id_perfil}, Monedas={monedas}")

        # Obtener el reto 9
        cursor.execute("SELECT id_reto, costo_monedas, nombre_reto FROM retos WHERE id_reto = 9")
        reto = cursor.fetchone()

        if not reto:
            print("No existe el reto con ID 9")
            return

        id_reto = reto[0]
        costo = reto[1]
        nombre = reto[2]

        print(f"Reto: ID={id_reto}, Costo={costo}, Nombre={nombre}")

        # Verificar si ya existe progreso para este reto
        cursor.execute("""
            SELECT id_progreso, completado
            FROM progreso
            WHERE id_perfil = %s AND id_reto = %s
        """, [id_perfil, id_reto])

        progreso_existente = cursor.fetchone()

        if progreso_existente:
            print(f"Ya existe progreso: ID={progreso_existente[0]}, Completado={progreso_existente[1]}")
        else:
            print("No existe progreso previo")

        # Intentar llamar al SP
        try:
            print(f"\nLlamando a iniciar_reto({id_perfil}, {id_reto})...")
            cursor.callproc('iniciar_reto', [id_perfil, id_reto])

            result = cursor.fetchone()

            if result:
                print("Resultado del SP:")
                columns = [col[0] for col in cursor.description]
                for col, val in zip(columns, result):
                    print(f"  {col}: {val}")
            else:
                print("El SP no retorno resultados")

        except Exception as e:
            print(f"ERROR al ejecutar SP: {str(e)}")

if __name__ == '__main__':
    test_iniciar_reto()
