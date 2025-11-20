"""
Debug del stored procedure iniciar_reto
Vamos a ejecutarlo paso a paso manualmente para ver qué está pasando
"""
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from django.db import connection

def debug_sp():
    print("=" * 80)
    print("DEBUG: STORED PROCEDURE iniciar_reto")
    print("=" * 80)

    id_perfil = 15
    id_reto = 8

    with connection.cursor() as cursor:
        print(f"\nParametros: id_perfil={id_perfil}, id_reto={id_reto}")

        # Paso 1: Obtener costo del reto
        print("\nPASO 1: Obtener costo del reto")
        cursor.execute("SELECT id_reto, nombre_reto, costo_monedas FROM retos WHERE id_reto = %s", [id_reto])
        reto = cursor.fetchone()
        print(f"  Reto encontrado: ID={reto[0]}, Nombre='{reto[1]}', Costo={reto[2]}")

        # Paso 2: Obtener monedas del perfil
        print("\nPASO 2: Obtener monedas del perfil")
        cursor.execute("SELECT id_perfil, monedas FROM perfiles WHERE id_perfil = %s", [id_perfil])
        perfil = cursor.fetchone()
        print(f"  Perfil encontrado: ID={perfil[0]}, Monedas={perfil[1]}")

        # Paso 3: Verificar progreso existente
        print("\nPASO 3: Verificar progreso existente")
        cursor.execute("""
            SELECT COUNT(*) FROM progreso
            WHERE id_perfil = %s AND id_reto = %s
        """, [id_perfil, id_reto])
        progreso_existente = cursor.fetchone()[0]
        print(f"  Progreso existente: {progreso_existente}")

        if progreso_existente > 0:
            print("\n  => EL SP DEBERIA RETORNAR EL PROGRESO EXISTENTE SIN DESCONTAR MONEDAS")
            cursor.execute("""
                SELECT id_progreso, id_perfil, id_reto, completado
                FROM progreso
                WHERE id_perfil = %s AND id_reto = %s
            """, [id_perfil, id_reto])
            prog = cursor.fetchone()
            print(f"     Progreso ID={prog[0]}, Perfil={prog[1]}, Reto={prog[2]}, Completado={prog[3]}")
        else:
            print("\n  => EL SP DEBERIA CREAR NUEVO PROGRESO Y DESCONTAR MONEDAS")
            print(f"     Descontar: {reto[2]} monedas")
            print(f"     Monedas despues: {perfil[1] - reto[2]}")

        # Ahora llamemos al SP real y veamos qué hace
        print("\n" + "=" * 80)
        print("LLAMANDO AL SP REAL")
        print("=" * 80)

        # Guardar monedas antes
        monedas_antes = perfil[1]

        cursor.callproc('iniciar_reto', [id_perfil, id_reto])
        result = cursor.fetchone()

        print(f"\nResultado del SP:")
        if result:
            columns = [col[0] for col in cursor.description]
            for col, val in zip(columns, result):
                print(f"  {col}: {val}")

        # Verificar monedas despues
        cursor.execute("SELECT monedas FROM perfiles WHERE id_perfil = %s", [id_perfil])
        monedas_despues = cursor.fetchone()[0]

        print(f"\nMonedas antes: {monedas_antes}")
        print(f"Monedas despues: {monedas_despues}")
        print(f"Monedas descontadas: {monedas_antes - monedas_despues}")

        print("\n" + "=" * 80)
        print("ANALISIS")
        print("=" * 80)

        if progreso_existente > 0:
            if monedas_antes == monedas_despues:
                print("OK El SP no desconto monedas (progreso ya existia)")
            else:
                print(f"ERROR El SP desconto {monedas_antes - monedas_despues} monedas cuando no debia")
        else:
            if (monedas_antes - monedas_despues) == reto[2]:
                print(f"OK El SP desconto {reto[2]} monedas correctamente")
            else:
                print(f"ERROR El SP desconto {monedas_antes - monedas_despues} monedas, esperaba {reto[2]}")

if __name__ == '__main__':
    debug_sp()
