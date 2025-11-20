"""
Script para:
1. Crear el trigger que devuelve monedas al borrar progreso
2. Corregir las monedas actuales del perfil 1
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from django.db import connection

def crear_trigger():
    """Crea el trigger para devolver monedas"""
    with connection.cursor() as cursor:
        print("=" * 80)
        print("CREANDO TRIGGER PARA DEVOLVER MONEDAS")
        print("=" * 80)

        # Eliminar trigger si existe
        cursor.execute("DROP TRIGGER IF EXISTS devolver_monedas_progreso")
        print("Trigger anterior eliminado (si existia)")

        # Crear trigger
        trigger_sql = """
CREATE TRIGGER devolver_monedas_progreso
AFTER DELETE ON progreso
FOR EACH ROW
BEGIN
    DECLARE v_costo INT;

    -- Solo devolver monedas si el reto NO estaba completado
    IF OLD.completado IS NULL OR OLD.completado = FALSE THEN
        -- Obtener el costo del reto eliminado
        SELECT costo_monedas INTO v_costo
        FROM retos
        WHERE id_reto = OLD.id_reto;

        -- Devolver las monedas al perfil
        UPDATE perfiles
        SET monedas = monedas + v_costo
        WHERE id_perfil = OLD.id_perfil;
    END IF;
END
"""
        cursor.execute(trigger_sql)
        print("Trigger 'devolver_monedas_progreso' creado exitosamente")

        # Verificar
        cursor.execute("""
            SELECT TRIGGER_NAME, EVENT_MANIPULATION, ACTION_TIMING
            FROM INFORMATION_SCHEMA.TRIGGERS
            WHERE TRIGGER_SCHEMA = 'juego_finanzas'
            AND TRIGGER_NAME = 'devolver_monedas_progreso'
        """)
        result = cursor.fetchone()
        if result:
            print(f"Verificado: {result[0]} ({result[2]} {result[1]})")
        else:
            print("ERROR: No se pudo verificar el trigger")

def calcular_monedas_correctas():
    """Calcula cuántas monedas debería tener el perfil 1"""
    with connection.cursor() as cursor:
        print("\n" + "=" * 80)
        print("CALCULANDO MONEDAS CORRECTAS")
        print("=" * 80)

        # Monedas iniciales (según el SP perfil_crear)
        monedas_iniciales = 0
        print(f"Monedas iniciales: {monedas_iniciales}")

        # Total gastado en todos los progresos actuales
        cursor.execute("""
            SELECT SUM(r.costo_monedas) AS total_gastado
            FROM progreso p
            INNER JOIN retos r ON p.id_reto = r.id_reto
            WHERE p.id_perfil = 1
        """)
        total_gastado = cursor.fetchone()[0] or 0
        print(f"Total gastado (progresos actuales): {total_gastado}")

        # Total ganado en retos completados
        cursor.execute("""
            SELECT SUM(r.recompensa_monedas) AS total_ganado
            FROM progreso p
            INNER JOIN retos r ON p.id_reto = r.id_reto
            WHERE p.id_perfil = 1 AND p.completado = TRUE
        """)
        total_ganado = cursor.fetchone()[0] or 0
        print(f"Total ganado (retos completados): {total_ganado}")

        # Calcular monedas correctas
        monedas_correctas = monedas_iniciales - total_gastado + total_ganado
        print(f"\nMonedas correctas: {monedas_iniciales} - {total_gastado} + {total_ganado} = {monedas_correctas}")

        # Monedas actuales
        cursor.execute("SELECT monedas FROM perfiles WHERE id_perfil = 1")
        monedas_actuales = cursor.fetchone()[0]
        print(f"Monedas actuales: {monedas_actuales}")

        diferencia = monedas_actuales - monedas_correctas
        print(f"Diferencia: {diferencia}")

        return monedas_correctas, monedas_actuales

def corregir_monedas(monedas_correctas):
    """Corrige las monedas del perfil 1"""
    with connection.cursor() as cursor:
        print("\n" + "=" * 80)
        print("CORRIGIENDO MONEDAS")
        print("=" * 80)

        # Actualizar monedas
        cursor.execute("""
            UPDATE perfiles
            SET monedas = %s
            WHERE id_perfil = 1
        """, [monedas_correctas])

        # Verificar
        cursor.execute("SELECT monedas FROM perfiles WHERE id_perfil = 1")
        nuevas_monedas = cursor.fetchone()[0]
        print(f"Monedas actualizadas: {nuevas_monedas}")

        if nuevas_monedas == monedas_correctas:
            print("OK Correccion exitosa!")
        else:
            print("ERROR: No se pudo corregir las monedas")

def main():
    print("\n" + "#" * 80)
    print("# SCRIPT DE CORRECCION DE MONEDAS")
    print("#" * 80 + "\n")

    try:
        # Paso 1: Crear trigger
        crear_trigger()

        # Paso 2: Calcular monedas correctas
        monedas_correctas, monedas_actuales = calcular_monedas_correctas()

        # Paso 3: Preguntar si quiere corregir
        if monedas_correctas != monedas_actuales:
            print("\n" + "!" * 80)
            print("ADVERTENCIA: Las monedas actuales no coinciden con el calculo esperado")
            print("!" * 80)
            respuesta = input(f"\nDeseas actualizar de {monedas_actuales} a {monedas_correctas} monedas? (s/n): ")

            if respuesta.lower() == 's':
                corregir_monedas(monedas_correctas)
            else:
                print("\nCorreccion cancelada")
        else:
            print("\nOK Las monedas ya son correctas. No se necesita correccion.")

        print("\n" + "#" * 80)
        print("# PROCESO COMPLETADO")
        print("#" * 80 + "\n")

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
