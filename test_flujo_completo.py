"""
Test automatizado del flujo completo de iniciar reto
Prueba:
1. Iniciar un reto nuevo → Descuenta monedas
2. Intentar iniciar el mismo reto → NO descuenta monedas adicionales
3. Verificar que las monedas son correctas
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from django.db import connection
from progresos.services import iniciar_reto_service
from usuarios.utils import obtener_perfil_de_usuario

def test_flujo_completo():
    print("=" * 80)
    print("TEST: FLUJO COMPLETO DE INICIAR RETO")
    print("=" * 80)

    id_usuario = 1
    id_reto = 8  # Reto 2 del tema 1

    with connection.cursor() as cursor:
        # Estado inicial
        print("\n1. ESTADO INICIAL")
        print("-" * 80)
        perfil_inicial = obtener_perfil_de_usuario(id_usuario)
        monedas_iniciales = perfil_inicial['monedas']
        print(f"Monedas iniciales: {monedas_iniciales}")

        # Obtener costo del reto
        cursor.execute("SELECT nombre_reto, costo_monedas FROM retos WHERE id_reto = %s", [id_reto])
        reto = cursor.fetchone()
        nombre_reto = reto[0]
        costo_reto = reto[1]
        print(f"Reto seleccionado: {nombre_reto}")
        print(f"Costo: {costo_reto} monedas")

        # Verificar si ya existe progreso
        cursor.execute("""
            SELECT COUNT(*) FROM progreso
            WHERE id_perfil = %s AND id_reto = %s
        """, [perfil_inicial['id_perfil'], id_reto])
        progreso_existente = cursor.fetchone()[0]

        if progreso_existente > 0:
            print(f"\nADVERTENCIA: Ya existe progreso para este reto")
            print("Eliminando progreso anterior para hacer la prueba limpia...")
            cursor.execute("""
                DELETE FROM progreso
                WHERE id_perfil = %s AND id_reto = %s
            """, [perfil_inicial['id_perfil'], id_reto])
            print("Progreso eliminado. Gracias al trigger, las monedas fueron devueltas.")

            # Verificar monedas después de eliminar
            perfil_despues_eliminar = obtener_perfil_de_usuario(id_usuario)
            monedas_despues_eliminar = perfil_despues_eliminar['monedas']
            print(f"Monedas despues de eliminar: {monedas_despues_eliminar}")
            monedas_iniciales = monedas_despues_eliminar

        # TEST 1: Primera vez - Debe descontar monedas
        print("\n2. TEST 1: INICIAR RETO POR PRIMERA VEZ")
        print("-" * 80)
        print(f"Llamando iniciar_reto_service({perfil_inicial['id_perfil']}, {id_reto})...")

        resultado1 = iniciar_reto_service(perfil_inicial['id_perfil'], id_reto)

        if resultado1:
            print(f"OK Progreso creado: ID {resultado1['id_progreso']}")

            # Verificar monedas
            perfil_despues = obtener_perfil_de_usuario(id_usuario)
            monedas_despues = perfil_despues['monedas']
            monedas_descontadas = monedas_iniciales - monedas_despues

            print(f"\nMonedas antes: {monedas_iniciales}")
            print(f"Monedas despues: {monedas_despues}")
            print(f"Monedas descontadas: {monedas_descontadas}")

            if monedas_descontadas == costo_reto:
                print(f"OK Se descontaron exactamente {costo_reto} monedas")
            else:
                print(f"ERROR: Se esperaban {costo_reto} monedas, pero se descontaron {monedas_descontadas}")
                return False
        else:
            print("ERROR: El servicio retorno None")
            return False

        # TEST 2: Segunda vez - NO debe descontar monedas
        print("\n3. TEST 2: INTENTAR INICIAR EL MISMO RETO DE NUEVO")
        print("-" * 80)
        print(f"Llamando iniciar_reto_service({perfil_inicial['id_perfil']}, {id_reto}) otra vez...")

        monedas_antes_segundo_intento = monedas_despues
        resultado2 = iniciar_reto_service(perfil_inicial['id_perfil'], id_reto)

        if resultado2:
            print(f"OK El servicio retorno progreso existente: ID {resultado2['id_progreso']}")

            # Verificar que NO descontó monedas
            perfil_final = obtener_perfil_de_usuario(id_usuario)
            monedas_finales = perfil_final['monedas']

            print(f"\nMonedas antes del segundo intento: {monedas_antes_segundo_intento}")
            print(f"Monedas despues del segundo intento: {monedas_finales}")

            if monedas_finales == monedas_antes_segundo_intento:
                print(f"OK NO se descontaron monedas adicionales")
            else:
                diferencia = monedas_antes_segundo_intento - monedas_finales
                print(f"ERROR: Se descontaron {diferencia} monedas adicionales!")
                return False
        else:
            print("ERROR: El servicio retorno None en el segundo intento")
            return False

        # TEST 3: Verificar que son el mismo progreso
        print("\n4. TEST 3: VERIFICAR QUE ES EL MISMO PROGRESO")
        print("-" * 80)
        if resultado1['id_progreso'] == resultado2['id_progreso']:
            print(f"OK Ambas llamadas retornaron el mismo progreso (ID {resultado1['id_progreso']})")
        else:
            print(f"ERROR: Se crearon dos progresos diferentes!")
            print(f"  Primer intento: ID {resultado1['id_progreso']}")
            print(f"  Segundo intento: ID {resultado2['id_progreso']}")
            return False

        # Resumen final
        print("\n5. RESUMEN FINAL")
        print("-" * 80)
        print(f"Monedas iniciales: {monedas_iniciales}")
        print(f"Costo del reto: {costo_reto}")
        print(f"Monedas finales: {monedas_finales}")
        print(f"Total descontado: {monedas_iniciales - monedas_finales}")

        if (monedas_iniciales - monedas_finales) == costo_reto:
            print("\nOK TODAS LAS PRUEBAS PASARON!")
            print("El sistema funciona correctamente:")
            print("  - Descuenta monedas solo la primera vez")
            print("  - No descuenta monedas en intentos posteriores")
            print("  - Retorna el mismo progreso existente")
            return True
        else:
            print("\nERROR: El total descontado no coincide con el costo del reto")
            return False

if __name__ == '__main__':
    try:
        exito = test_flujo_completo()
        print("\n" + "=" * 80)
        if exito:
            print("RESULTADO: EXITO")
        else:
            print("RESULTADO: FALLO")
        print("=" * 80)
    except Exception as e:
        print(f"\nEXCEPCION: {str(e)}")
        import traceback
        traceback.print_exc()
