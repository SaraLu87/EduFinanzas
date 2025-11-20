"""
Test completo del flujo de Sara:
1. Primer reto (debe funcionar bien)
2. Segundo reto (problema: resta 10 en lugar de 5)
3. Tercer reto del siguiente tema (problema: no permite)
"""
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from django.db import connection
from progresos.services import iniciar_reto_service
from solucionarReto.services import solucionar_reto_service
from usuarios.utils import obtener_perfil_de_usuario

def obtener_retos_tema(id_tema):
    """Obtiene los retos de un tema"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_reto, nombre_reto, costo_monedas, recompensa_monedas, descripcion
            FROM retos
            WHERE id_tema = %s
            ORDER BY id_reto
        """, [id_tema])
        return cursor.fetchall()

def mostrar_estado(id_perfil, paso):
    """Muestra el estado actual del perfil"""
    perfil = obtener_perfil_de_usuario_por_id_perfil(id_perfil)
    print(f"\n{'='*80}")
    print(f"ESTADO DESPUES DE: {paso}")
    print(f"{'='*80}")
    print(f"Monedas: {perfil['monedas']}")

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.id_reto, r.nombre_reto, r.costo_monedas, p.completado
            FROM progreso p
            INNER JOIN retos r ON p.id_reto = r.id_reto
            WHERE p.id_perfil = %s
            ORDER BY p.id_progreso
        """, [id_perfil])
        progresos = cursor.fetchall()

        if progresos:
            print("\nProgresos:")
            for prog in progresos:
                estado = "COMPLETADO" if prog[3] else "INICIADO"
                print(f"  - Reto {prog[0]} ({prog[1]}): {estado}, Costo: {prog[2]}")
        else:
            print("\nSin progresos aun")

def obtener_perfil_de_usuario_por_id_perfil(id_perfil):
    """Obtiene perfil por id_perfil"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_perfil, id_usuario, nombre_perfil, edad, foto_perfil, monedas
            FROM perfiles
            WHERE id_perfil = %s
        """, [id_perfil])
        row = cursor.fetchone()
        return {
            'id_perfil': row[0],
            'id_usuario': row[1],
            'nombre_perfil': row[2],
            'edad': row[3],
            'foto_perfil': row[4],
            'monedas': row[5]
        }

def test_completo():
    print("#" * 80)
    print("TEST COMPLETO DEL FLUJO DE SARA")
    print("#" * 80)

    # Obtener datos de Sara
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.id_usuario, p.id_perfil, p.nombre_perfil, p.monedas
            FROM usuarios u
            INNER JOIN perfiles p ON u.id_usuario = p.id_usuario
            WHERE u.correo = %s
        """, ['sara.munoz.q@uniautonoma.edu.co'])

        result = cursor.fetchone()
        id_usuario = result[0]
        id_perfil = result[1]
        nombre = result[2]
        monedas_iniciales = result[3]

    print(f"\nUsuario: {nombre}")
    print(f"ID Perfil: {id_perfil}")
    print(f"Monedas iniciales: {monedas_iniciales}")

    # Obtener retos del tema 1
    retos_tema1 = obtener_retos_tema(1)
    print(f"\n{'-'*80}")
    print("RETOS DEL TEMA 1:")
    print(f"{'-'*80}")
    for reto in retos_tema1:
        print(f"ID {reto[0]}: {reto[1]} - Costo: {reto[2]}, Recompensa: {reto[3]}")

    # ==========================================
    # PASO 1: PRIMER RETO
    # ==========================================
    print(f"\n{'#'*80}")
    print("PASO 1: INICIAR Y COMPLETAR PRIMER RETO")
    print(f"{'#'*80}")

    primer_reto = retos_tema1[0]
    id_reto_1 = primer_reto[0]
    costo_1 = primer_reto[2]
    recompensa_1 = primer_reto[3]

    print(f"\nReto: {primer_reto[1]}")
    print(f"Costo: {costo_1} monedas")
    print(f"Recompensa: {recompensa_1} monedas")

    monedas_antes = obtener_perfil_de_usuario_por_id_perfil(id_perfil)['monedas']
    print(f"\nMonedas antes de iniciar: {monedas_antes}")

    # Iniciar reto
    print(f"\nIniciando reto {id_reto_1}...")
    resultado_inicio_1 = iniciar_reto_service(id_perfil, id_reto_1)

    monedas_despues_inicio = obtener_perfil_de_usuario_por_id_perfil(id_perfil)['monedas']
    print(f"Monedas despues de iniciar: {monedas_despues_inicio}")
    print(f"Monedas descontadas: {monedas_antes - monedas_despues_inicio}")

    if (monedas_antes - monedas_despues_inicio) == costo_1:
        print(f"OK Se descontaron {costo_1} monedas correctamente")
    else:
        print(f"ERROR: Se esperaban {costo_1} monedas, se descontaron {monedas_antes - monedas_despues_inicio}")

    # Completar reto (asumiendo respuesta correcta)
    with connection.cursor() as cursor:
        cursor.execute("SELECT respuestaCorrecta FROM retos WHERE id_reto = %s", [id_reto_1])
        respuesta_correcta = cursor.fetchone()[0]

    print(f"\nCompletando reto con respuesta correcta: {respuesta_correcta}")
    resultado_solucion_1 = solucionar_reto_service(id_perfil, id_reto_1, respuesta_correcta)

    monedas_despues_completar = obtener_perfil_de_usuario_por_id_perfil(id_perfil)['monedas']
    print(f"Monedas despues de completar: {monedas_despues_completar}")

    ganancia = monedas_despues_completar - monedas_despues_inicio
    print(f"Monedas ganadas: {ganancia}")

    if ganancia == recompensa_1:
        print(f"OK Se ganaron {recompensa_1} monedas correctamente")
    else:
        print(f"ERROR: Se esperaban {recompensa_1} monedas, se ganaron {ganancia}")

    mostrar_estado(id_perfil, "PRIMER RETO")

    # ==========================================
    # PASO 2: SEGUNDO RETO
    # ==========================================
    print(f"\n{'#'*80}")
    print("PASO 2: INICIAR SEGUNDO RETO (AQUI REPORTAS EL PROBLEMA)")
    print(f"{'#'*80}")

    segundo_reto = retos_tema1[1]
    id_reto_2 = segundo_reto[0]
    costo_2 = segundo_reto[2]
    recompensa_2 = segundo_reto[3]

    print(f"\nReto: {segundo_reto[1]}")
    print(f"Costo: {costo_2} monedas")
    print(f"Recompensa: {recompensa_2} monedas")

    monedas_antes_2 = obtener_perfil_de_usuario_por_id_perfil(id_perfil)['monedas']
    print(f"\nMonedas antes de iniciar: {monedas_antes_2}")

    # Iniciar segundo reto
    print(f"\nIniciando reto {id_reto_2}...")
    resultado_inicio_2 = iniciar_reto_service(id_perfil, id_reto_2)

    monedas_despues_inicio_2 = obtener_perfil_de_usuario_por_id_perfil(id_perfil)['monedas']
    print(f"Monedas despues de iniciar: {monedas_despues_inicio_2}")

    monedas_descontadas_2 = monedas_antes_2 - monedas_despues_inicio_2
    print(f"Monedas descontadas: {monedas_descontadas_2}")

    print(f"\n{'!'*80}")
    if monedas_descontadas_2 == costo_2:
        print(f"OK Se descontaron {costo_2} monedas correctamente")
    else:
        print(f"PROBLEMA ENCONTRADO!")
        print(f"  Costo esperado: {costo_2} monedas")
        print(f"  Monedas descontadas: {monedas_descontadas_2} monedas")
        print(f"  Diferencia: {monedas_descontadas_2 - costo_2} monedas de mas")
    print(f"{'!'*80}")

    mostrar_estado(id_perfil, "SEGUNDO RETO")

    # ==========================================
    # PASO 3: INTENTAR TEMA 2
    # ==========================================
    print(f"\n{'#'*80}")
    print("PASO 3: INTENTAR INICIAR RETO DEL TEMA 2")
    print(f"{'#'*80}")

    # Obtener retos del tema 2
    retos_tema2 = obtener_retos_tema(2)

    if not retos_tema2:
        print("\nERROR: No hay retos en el tema 2")
        return

    print(f"\nRETOS DEL TEMA 2:")
    for reto in retos_tema2:
        print(f"ID {reto[0]}: {reto[1]} - Costo: {reto[2]}, Recompensa: {reto[3]}")

    primer_reto_tema2 = retos_tema2[0]
    id_reto_tema2 = primer_reto_tema2[0]
    costo_tema2 = primer_reto_tema2[2]

    print(f"\nIntentando iniciar: {primer_reto_tema2[1]}")
    print(f"Costo: {costo_tema2} monedas")

    monedas_antes_tema2 = obtener_perfil_de_usuario_por_id_perfil(id_perfil)['monedas']
    print(f"Monedas disponibles: {monedas_antes_tema2}")

    if monedas_antes_tema2 < costo_tema2:
        print(f"\n{'!'*80}")
        print(f"PROBLEMA ENCONTRADO!")
        print(f"  No tienes suficientes monedas")
        print(f"  Necesitas: {costo_tema2} monedas")
        print(f"  Tienes: {monedas_antes_tema2} monedas")
        print(f"  Te faltan: {costo_tema2 - monedas_antes_tema2} monedas")
        print(f"{'!'*80}")

        print("\nPOSIBLE CAUSA:")
        print("  El segundo reto resto mas monedas de las que debia")
        print(f"  Si hubiera restado {costo_2} (correcto) en lugar de {monedas_descontadas_2}")
        print(f"  Tendrias: {monedas_antes_tema2 + (monedas_descontadas_2 - costo_2)} monedas")
    else:
        print("\nIntentando iniciar reto del tema 2...")
        try:
            resultado_tema2 = iniciar_reto_service(id_perfil, id_reto_tema2)
            print(f"OK Reto iniciado correctamente")
        except Exception as e:
            print(f"ERROR: {str(e)}")

    mostrar_estado(id_perfil, "INTENTO TEMA 2")

    # ==========================================
    # ANALISIS FINAL
    # ==========================================
    print(f"\n{'#'*80}")
    print("ANALISIS DEL PROBLEMA")
    print(f"{'#'*80}")

    print("\nRESUMEN:")
    print(f"1. Primer reto: OK")
    print(f"2. Segundo reto: Resto {monedas_descontadas_2} monedas en lugar de {costo_2}")
    print(f"3. Tercer reto (tema 2): No se puede iniciar por falta de monedas")

    print("\nCALCULO ESPERADO:")
    print(f"  Monedas iniciales: {monedas_iniciales}")
    print(f"  Reto 1: -{costo_1} + {recompensa_1} = +{recompensa_1 - costo_1}")
    print(f"  Reto 2: -{costo_2} = -{costo_2}")
    print(f"  TOTAL ESPERADO: {monedas_iniciales + (recompensa_1 - costo_1) - costo_2} monedas")

    print("\nCALCULO REAL:")
    monedas_finales = obtener_perfil_de_usuario_por_id_perfil(id_perfil)['monedas']
    print(f"  TOTAL REAL: {monedas_finales} monedas")
    print(f"  DIFERENCIA: {(monedas_iniciales + (recompensa_1 - costo_1) - costo_2) - monedas_finales} monedas")

if __name__ == '__main__':
    try:
        test_completo()
    except Exception as e:
        print(f"\nEXCEPCION: {str(e)}")
        import traceback
        traceback.print_exc()
