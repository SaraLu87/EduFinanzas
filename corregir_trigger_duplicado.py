"""
Corregir el bug del trigger duplicado
El trigger trg_restar_monedas_al_jugar_reto está restando monedas
cuando el SP iniciar_reto ya lo hace
"""
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from django.db import connection

def corregir_trigger():
    print("#" * 80)
    print("CORRECCIÓN: ELIMINAR TRIGGER DUPLICADO")
    print("#" * 80)

    with connection.cursor() as cursor:
        print("\n1. VERIFICAR TRIGGERS ACTUALES")
        print("-" * 80)

        cursor.execute("SHOW TRIGGERS")
        triggers = cursor.fetchall()

        print("\nTriggers encontrados:")
        for trigger in triggers:
            print(f"  - {trigger[0]} ({trigger[1]} {trigger[2]} ON {trigger[3]})")

        print("\n2. ELIMINAR TRIGGER PROBLEMA: trg_restar_monedas_al_jugar_reto")
        print("-" * 80)

        cursor.execute("DROP TRIGGER IF EXISTS trg_restar_monedas_al_jugar_reto")
        print("OK Trigger eliminado")

        print("\n3. VERIFICAR TRIGGERS DESPUÉS DE LA CORRECCIÓN")
        print("-" * 80)

        cursor.execute("SHOW TRIGGERS")
        triggers_despues = cursor.fetchall()

        print("\nTriggers restantes:")
        for trigger in triggers_despues:
            print(f"  - {trigger[0]} ({trigger[1]} {trigger[2]} ON {trigger[3]})")

        print("\n4. EXPLICACIÓN")
        print("-" * 80)
        print("""
PROBLEMA:
  El trigger trg_restar_monedas_al_jugar_reto se ejecutaba en BEFORE INSERT
  sobre la tabla progreso, y restaba las monedas del perfil.

  Pero el stored procedure iniciar_reto YA resta las monedas antes de hacer
  el INSERT en progreso.

  Resultado: Las monedas se restaban DOS VECES.

SOLUCIÓN:
  Eliminar el trigger trg_restar_monedas_al_jugar_reto para que solo el SP
  sea responsable de restar las monedas.

  El SP iniciar_reto ya tiene toda la lógica necesaria:
  - Verifica si hay progreso existente
  - Verifica monedas suficientes
  - Resta monedas solo si es necesario
  - Inserta el registro de progreso

TRIGGERS QUE SE MANTIENEN:
  - trg_sumar_monedas_al_completar_reto: Para sumar recompensa al completar
  - devolver_monedas_progreso: Para devolver monedas al eliminar progreso
        """)

        print("\n" + "#" * 80)
        print("CORRECCIÓN COMPLETADA")
        print("#" * 80)

if __name__ == '__main__':
    corregir_trigger()
