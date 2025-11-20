"""
Crear una versión de debug del SP que imprime valores
"""
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from django.db import connection

def crear_sp_debug():
    with connection.cursor() as cursor:
        # Eliminar SP de debug si existe
        cursor.execute("DROP PROCEDURE IF EXISTS iniciar_reto_debug")

        # Crear SP de debug con SELECT para ver valores
        sp_debug = """
CREATE PROCEDURE iniciar_reto_debug(
    IN p_id_perfil INT,
    IN p_id_reto INT
)
BEGIN
    DECLARE v_costo INT;
    DECLARE v_monedas_actuales INT;
    DECLARE v_progreso_existente INT;
    DECLARE v_id_progreso INT;

    -- Obtener costo del reto
    SELECT costo_monedas INTO v_costo
    FROM retos
    WHERE id_reto = p_id_reto;

    -- Obtener monedas del perfil
    SELECT monedas INTO v_monedas_actuales
    FROM perfiles
    WHERE id_perfil = p_id_perfil;

    -- Verificar progreso existente
    SELECT COUNT(*) INTO v_progreso_existente
    FROM progreso
    WHERE id_perfil = p_id_perfil AND id_reto = p_id_reto;

    -- RETORNAR VALORES PARA DEBUG
    SELECT
        p_id_perfil AS param_id_perfil,
        p_id_reto AS param_id_reto,
        v_costo AS variable_costo,
        v_monedas_actuales AS variable_monedas_actuales,
        v_progreso_existente AS variable_progreso_existente;
END
"""

        cursor.execute(sp_debug)
        print("SP iniciar_reto_debug creado exitosamente")

        # Llamar al SP de debug
        print("\n" + "=" * 80)
        print("LLAMANDO A iniciar_reto_debug(15, 8)")
        print("=" * 80)

        cursor.callproc('iniciar_reto_debug', [15, 8])
        result = cursor.fetchone()

        if result:
            columns = [col[0] for col in cursor.description]
            print("\nValores dentro del SP:")
            for col, val in zip(columns, result):
                print(f"  {col}: {val}")

if __name__ == '__main__':
    crear_sp_debug()
