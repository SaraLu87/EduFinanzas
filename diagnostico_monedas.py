"""
Script de diagnóstico para rastrear el flujo de monedas
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from django.db import connection

def diagnostico_completo():
    """Diagnóstico completo del flujo de monedas"""

    with connection.cursor() as cursor:
        print("=" * 80)
        print("DIAGNÓSTICO COMPLETO DE MONEDAS")
        print("=" * 80)

        # 1. Estado actual del perfil
        print("\n1. ESTADO ACTUAL DEL PERFIL")
        print("-" * 80)
        cursor.execute("""
            SELECT id_perfil, id_usuario, nombre_perfil, monedas
            FROM perfiles
            WHERE id_perfil = 1
        """)
        perfil = cursor.fetchone()
        print(f"Perfil ID: {perfil[0]}")
        print(f"Usuario ID: {perfil[1]}")
        print(f"Nombre: {perfil[2]}")
        print(f"Monedas actuales: {perfil[3]}")

        # 2. Información de los retos
        print("\n2. RETOS DEL TEMA 1")
        print("-" * 80)
        cursor.execute("""
            SELECT id_reto, nombre_reto, costo_monedas, recompensa_monedas
            FROM retos
            WHERE id_tema = 1
            ORDER BY id_reto
        """)
        retos = cursor.fetchall()
        print(f"{'ID':<5} {'Nombre':<30} {'Costo':<10} {'Recompensa':<12}")
        print("-" * 80)
        for reto in retos:
            print(f"{reto[0]:<5} {reto[1]:<30} {reto[2]:<10} {reto[3]:<12}")

        # 3. Progreso del usuario
        print("\n3. PROGRESO DEL USUARIO (PERFIL 1)")
        print("-" * 80)
        cursor.execute("""
            SELECT
                p.id_progreso,
                p.id_reto,
                r.nombre_reto,
                p.completado,
                p.fecha_completado
            FROM progreso p
            INNER JOIN retos r ON p.id_reto = r.id_reto
            WHERE p.id_perfil = 1
            ORDER BY p.id_progreso
        """)
        progresos = cursor.fetchall()

        if progresos:
            print(f"{'ID Prog':<10} {'ID Reto':<10} {'Nombre Reto':<30} {'Completado':<12} {'Fecha':<20}")
            print("-" * 80)
            for prog in progresos:
                completado = "Sí" if prog[3] else "No"
                fecha = str(prog[4]) if prog[4] else "N/A"
                print(f"{prog[0]:<10} {prog[1]:<10} {prog[2]:<30} {completado:<12} {fecha:<20}")
        else:
            print("No hay progresos registrados")

        # 4. Calcular monedas esperadas
        print("\n4. ANÁLISIS DE MONEDAS")
        print("-" * 80)

        # Monedas iniciales (suponiendo que empezó con 100)
        monedas_iniciales = 100
        print(f"Monedas iniciales (estimadas): {monedas_iniciales}")

        # Calcular total gastado
        cursor.execute("""
            SELECT SUM(r.costo_monedas) AS total_gastado
            FROM progreso p
            INNER JOIN retos r ON p.id_reto = r.id_reto
            WHERE p.id_perfil = 1
        """)
        total_gastado = cursor.fetchone()[0] or 0
        print(f"Total gastado en retos: {total_gastado}")

        # Calcular total ganado (solo retos completados)
        cursor.execute("""
            SELECT SUM(r.recompensa_monedas) AS total_ganado
            FROM progreso p
            INNER JOIN retos r ON p.id_reto = r.id_reto
            WHERE p.id_perfil = 1 AND p.completado = TRUE
        """)
        total_ganado = cursor.fetchone()[0] or 0
        print(f"Total ganado (retos completados): {total_ganado}")

        # Monedas esperadas
        monedas_esperadas = monedas_iniciales - total_gastado + total_ganado
        monedas_actuales = perfil[3]
        diferencia = monedas_actuales - monedas_esperadas

        print(f"\nCálculo esperado:")
        print(f"  {monedas_iniciales} (inicial) - {total_gastado} (gastado) + {total_ganado} (ganado) = {monedas_esperadas}")
        print(f"\nMonedas actuales en BD: {monedas_actuales}")
        print(f"Diferencia: {diferencia}")

        if diferencia < 0:
            print(f"\n⚠️ ALERTA: Faltan {abs(diferencia)} monedas. Posible sobrecosto.")
        elif diferencia > 0:
            print(f"\n✓ Hay {diferencia} monedas extra.")
        else:
            print("\n✓ Las monedas coinciden perfectamente.")

        # 5. Verificar el stored procedure
        print("\n5. PRUEBA DEL STORED PROCEDURE")
        print("-" * 80)
        print("Vamos a simular iniciar el reto 9...")

        # Obtener info del reto 9
        cursor.execute("""
            SELECT id_reto, nombre_reto, costo_monedas
            FROM retos
            WHERE id_reto = 9
        """)
        reto9 = cursor.fetchone()

        if reto9:
            print(f"Reto 9: {reto9[1]}")
            print(f"Costo: {reto9[2]} monedas")
            print(f"Monedas actuales del usuario: {perfil[3]}")

            # Verificar si ya existe progreso
            cursor.execute("""
                SELECT COUNT(*) FROM progreso
                WHERE id_perfil = 1 AND id_reto = 9
            """)
            existe = cursor.fetchone()[0]

            if existe > 0:
                print("\n⚠️ Ya existe progreso para este reto. El SP NO descontará monedas.")
                print("   El SP retornará el progreso existente sin hacer cambios.")
            else:
                print("\n✓ No existe progreso. El SP descontará monedas y creará progreso nuevo.")
                print(f"   Monedas después de iniciar: {perfil[3] - reto9[2]}")
        else:
            print("No se encontró el reto 9")

        # 6. Historial detallado
        print("\n6. HISTORIAL DETALLADO POR RETO")
        print("-" * 80)
        cursor.execute("""
            SELECT
                r.id_reto,
                r.nombre_reto,
                r.costo_monedas,
                r.recompensa_monedas,
                CASE WHEN p.id_progreso IS NOT NULL THEN 'INICIADO' ELSE 'NO INICIADO' END AS estado_inicio,
                CASE WHEN p.completado = TRUE THEN 'COMPLETADO' ELSE 'PENDIENTE' END AS estado_completado
            FROM retos r
            LEFT JOIN progreso p ON r.id_reto = p.id_reto AND p.id_perfil = 1
            WHERE r.id_tema = 1
            ORDER BY r.id_reto
        """)
        historial = cursor.fetchall()

        print(f"{'Reto':<5} {'Nombre':<30} {'Costo':<8} {'Premio':<8} {'Iniciado':<15} {'Estado':<12}")
        print("-" * 80)
        for h in historial:
            print(f"{h[0]:<5} {h[1]:<30} {h[2]:<8} {h[3]:<8} {h[4]:<15} {h[5]:<12}")

if __name__ == '__main__':
    diagnostico_completo()
