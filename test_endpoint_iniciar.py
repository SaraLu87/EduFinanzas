"""
Script para probar el endpoint de iniciar reto
"""
import os
import django
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from usuarios.utils import obtener_perfil_de_usuario
from progresos.services import iniciar_reto_service

def test_endpoint():
    """Simula la lógica del endpoint"""

    # Simular que el usuario con id_usuario=1 está autenticado
    id_usuario = 1
    id_reto = 9

    print(f"Probando iniciar reto {id_reto} para usuario {id_usuario}")
    print("=" * 60)

    try:
        # Paso 1: Obtener perfil
        print("\n1. Obteniendo perfil del usuario...")
        perfil = obtener_perfil_de_usuario(id_usuario)

        if not perfil:
            print("ERROR: Perfil no encontrado")
            return

        print(f"   Perfil encontrado: ID={perfil['id_perfil']}, Monedas={perfil['monedas']}")

        # Paso 2: Llamar al servicio
        print(f"\n2. Llamando a iniciar_reto_service({perfil['id_perfil']}, {id_reto})...")
        resultado = iniciar_reto_service(perfil['id_perfil'], id_reto)

        if not resultado:
            print("ERROR: El servicio retorno None")
            return

        print("   Resultado del servicio:")
        for key, value in resultado.items():
            print(f"     {key}: {value}")

        # Paso 3: Obtener perfil actualizado
        print("\n3. Obteniendo perfil actualizado...")
        perfil_actualizado = obtener_perfil_de_usuario(id_usuario)
        print(f"   Monedas actualizadas: {perfil_actualizado['monedas']}")

        print("\n[OK] Proceso completado exitosamente")

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_endpoint()
