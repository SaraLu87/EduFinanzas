"""
Test rápido: Intentar iniciar el reto 8 de nuevo
"""
import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from progresos.services import iniciar_reto_service
from usuarios.utils import obtener_perfil_de_usuario

print("=" * 80)
print("TEST: SEGUNDO INTENTO DE INICIAR RETO 8")
print("=" * 80)

perfil_antes = obtener_perfil_de_usuario(1)
monedas_antes = perfil_antes['monedas']
print(f"Monedas antes: {monedas_antes}")

print("\nLlamando iniciar_reto_service(1, 8)...")
resultado = iniciar_reto_service(1, 8)

if resultado:
    print(f"Resultado: Progreso ID {resultado['id_progreso']}")

    perfil_despues = obtener_perfil_de_usuario(1)
    monedas_despues = perfil_despues['monedas']
    print(f"Monedas despues: {monedas_despues}")

    diferencia = monedas_antes - monedas_despues
    print(f"Monedas descontadas: {diferencia}")

    print("\n" + "=" * 80)
    if diferencia == 0:
        print("EXITO: NO se descontaron monedas adicionales!")
        print("El SP funciona correctamente - retorna progreso existente sin descontar")
    else:
        print(f"ERROR: Se descontaron {diferencia} monedas adicionales")
    print("=" * 80)
else:
    print("ERROR: El servicio retorno None")
