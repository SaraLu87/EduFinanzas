"""
Script para crear los stored procedures de progreso por temas
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from django.db import connection

def crear_stored_procedures():
    """Crea los stored procedures necesarios"""

    # SP 1: verificar_tema_completado
    sp1 = """
DROP PROCEDURE IF EXISTS verificar_tema_completado;
"""

    sp1_create = """
CREATE PROCEDURE verificar_tema_completado(
    IN p_id_tema INT,
    IN p_id_perfil INT
)
BEGIN
    DECLARE v_total_retos INT DEFAULT 0;
    DECLARE v_retos_completados INT DEFAULT 0;
    DECLARE v_esta_completado BOOLEAN DEFAULT FALSE;

    -- Contar total de retos del tema
    SELECT COUNT(*) INTO v_total_retos
    FROM retos
    WHERE id_tema = p_id_tema;

    -- Contar retos completados por el usuario en este tema
    SELECT COUNT(*) INTO v_retos_completados
    FROM progreso p
    INNER JOIN retos r ON p.id_reto = r.id_reto
    WHERE r.id_tema = p_id_tema
      AND p.id_perfil = p_id_perfil
      AND p.completado = TRUE;

    -- Determinar si el tema esta completado
    IF v_total_retos > 0 AND v_retos_completados = v_total_retos THEN
        SET v_esta_completado = TRUE;
    END IF;

    -- Retornar estadisticas
    SELECT
        p_id_tema AS id_tema,
        v_total_retos AS total_retos,
        v_retos_completados AS retos_completados,
        v_esta_completado AS esta_completado;
END
"""

    # SP 2: obtener_progreso_por_temas
    sp2 = """
DROP PROCEDURE IF EXISTS obtener_progreso_por_temas;
"""

    sp2_create = """
CREATE PROCEDURE obtener_progreso_por_temas(
    IN p_id_perfil INT
)
BEGIN
    SELECT
        t.id_tema,
        t.nombre AS nombre_tema,
        COUNT(r.id_reto) AS total_retos,
        COALESCE(SUM(CASE WHEN p.completado = TRUE THEN 1 ELSE 0 END), 0) AS retos_completados,
        CASE
            WHEN COUNT(r.id_reto) > 0 AND
                 COALESCE(SUM(CASE WHEN p.completado = TRUE THEN 1 ELSE 0 END), 0) = COUNT(r.id_reto)
            THEN TRUE
            ELSE FALSE
        END AS esta_completado
    FROM temas t
    LEFT JOIN retos r ON t.id_tema = r.id_tema
    LEFT JOIN progreso p ON r.id_reto = p.id_reto AND p.id_perfil = p_id_perfil
    GROUP BY t.id_tema, t.nombre
    ORDER BY t.id_tema ASC;
END
"""

    try:
        with connection.cursor() as cursor:
            print("Eliminando SP verificar_tema_completado si existe...")
            cursor.execute(sp1)

            print("Creando SP verificar_tema_completado...")
            cursor.execute(sp1_create)

            print("Eliminando SP obtener_progreso_por_temas si existe...")
            cursor.execute(sp2)

            print("Creando SP obtener_progreso_por_temas...")
            cursor.execute(sp2_create)

            print("\n[OK] Stored procedures creados exitosamente!")

            # Verificar
            cursor.execute("""
                SELECT ROUTINE_NAME
                FROM INFORMATION_SCHEMA.ROUTINES
                WHERE ROUTINE_SCHEMA = 'juego_finanzas'
                AND ROUTINE_TYPE = 'PROCEDURE'
                AND ROUTINE_NAME IN ('verificar_tema_completado', 'obtener_progreso_por_temas')
            """)

            procedures = cursor.fetchall()
            print("\nProcedimientos creados:")
            for proc in procedures:
                print(f"  - {proc[0]}")

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")

if __name__ == '__main__':
    crear_stored_procedures()
