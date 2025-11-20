"""
Script para probar la serialización JSON del endpoint iniciar_reto
"""
import os
import django
import sys
import json

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduFinanzas.settings')
django.setup()

from usuarios.utils import obtener_perfil_de_usuario
from progresos.services import iniciar_reto_service
from rest_framework.renderers import JSONRenderer

def test_serialization():
    """Prueba la serialización del resultado"""

    id_usuario = 1
    id_reto = 9

    print("=== TEST DE SERIALIZACIÓN ===\n")

    try:
        # Obtener perfil
        print("1. Obteniendo perfil...")
        perfil = obtener_perfil_de_usuario(id_usuario)
        print(f"   Perfil: ID={perfil['id_perfil']}, Monedas={perfil['monedas']}")
        print(f"   Tipo de monedas: {type(perfil['monedas'])}")

        # Llamar al servicio
        print(f"\n2. Iniciando reto {id_reto}...")
        resultado = iniciar_reto_service(perfil['id_perfil'], id_reto)

        if not resultado:
            print("   ERROR: Servicio retornó None")
            return

        print("   Resultado del servicio:")
        for key, value in resultado.items():
            print(f"     {key}: {value} (tipo: {type(value).__name__})")

        # Crear dictionaries serializables (como en el endpoint)
        print("\n3. Creando dictionaries serializables...")
        progreso_serializable = {
            "id_progreso": resultado['id_progreso'],
            "id_perfil": resultado['id_perfil'],
            "id_reto": resultado['id_reto'],
            "completado": bool(resultado['completado']) if resultado['completado'] is not None else False,
            "fecha_completado": str(resultado['fecha_completado']) if resultado['fecha_completado'] else None,
            "respuesta_seleccionada": resultado['respuesta_seleccionada'] if resultado['respuesta_seleccionada'] else None
        }

        perfil_actualizado = obtener_perfil_de_usuario(id_usuario)
        perfil_serializable = {
            "id_perfil": perfil_actualizado['id_perfil'],
            "id_usuario": perfil_actualizado['id_usuario'],
            "nombre_perfil": perfil_actualizado['nombre_perfil'],
            "edad": perfil_actualizado['edad'],
            "foto_perfil": perfil_actualizado['foto_perfil'],
            "monedas": int(perfil_actualizado['monedas'])
        }

        # Crear respuesta como en el endpoint
        response_data = {
            "message": "Reto iniciado exitosamente",
            "progreso": progreso_serializable,
            "perfil": perfil_serializable
        }

        # Intentar serializar a JSON
        print("\n4. Intentando serializar a JSON...")
        json_string = json.dumps(response_data, ensure_ascii=False, indent=2)
        print("   ✓ Serialización exitosa!")

        print("\n5. JSON resultante:")
        print(json_string)

        print("\n[OK] Todos los tipos son serializables correctamente")

    except TypeError as e:
        print(f"\n[ERROR DE SERIALIZACIÓN] {str(e)}")
        import traceback
        traceback.print_exc()

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_serialization()
