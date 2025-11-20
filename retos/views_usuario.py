"""
Views para funcionalidades de retos para usuarios autenticados
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import DatabaseError
from usuarios.utils import extraer_usuario_de_token, obtener_perfil_de_usuario
from .services import obtener_retos_por_tema_service
from progresos.services import iniciar_reto_service


class RetosPorTemaView(APIView):
    """
    Endpoint para obtener todos los retos de un tema con progreso del usuario
    GET /api/temas/<id_tema>/retos/
    """

    def get(self, request, id_tema):
        """Obtiene retos del tema con progreso del usuario autenticado"""
        try:
            # Extraer id_usuario del token
            id_usuario = extraer_usuario_de_token(request)

            # Obtener perfil asociado
            perfil = obtener_perfil_de_usuario(id_usuario)

            if not perfil:
                return Response(
                    {"detail": "Perfil no encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Obtener retos con progreso
            retos = obtener_retos_por_tema_service(int(id_tema), perfil['id_perfil'])

            return Response(retos, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )


class IniciarRetoView(APIView):
    """
    Endpoint para iniciar/comprar un reto
    POST /api/retos/<id_reto>/iniciar/

    Body:
        No requiere body, el id_perfil se obtiene del token
    """

    def post(self, request, id_reto):
        """Inicia un reto descontando monedas del perfil"""
        try:
            # Extraer id_usuario del token
            id_usuario = extraer_usuario_de_token(request)

            # Obtener perfil asociado
            perfil = obtener_perfil_de_usuario(id_usuario)

            if not perfil:
                return Response(
                    {"detail": "Perfil no encontrado"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Llamar al servicio que ejecuta el SP iniciar_reto
            resultado = iniciar_reto_service(perfil['id_perfil'], int(id_reto))

            if not resultado:
                return Response(
                    {"detail": "Error al iniciar reto"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Convertir valores None y fechas a formatos serializables
            progreso_serializable = {
                "id_progreso": resultado['id_progreso'],
                "id_perfil": resultado['id_perfil'],
                "id_reto": resultado['id_reto'],
                "completado": bool(resultado['completado']) if resultado['completado'] is not None else False,
                "fecha_completado": str(resultado['fecha_completado']) if resultado['fecha_completado'] else None,
                "respuesta_seleccionada": resultado['respuesta_seleccionada'] if resultado['respuesta_seleccionada'] else None
            }

            # Obtener perfil actualizado con las monedas descontadas
            perfil_actualizado = obtener_perfil_de_usuario(id_usuario)

            # Asegurar que el perfil también sea serializable
            perfil_serializable = {
                "id_perfil": perfil_actualizado['id_perfil'],
                "id_usuario": perfil_actualizado['id_usuario'],
                "nombre_perfil": perfil_actualizado['nombre_perfil'],
                "edad": perfil_actualizado['edad'],
                "foto_perfil": perfil_actualizado['foto_perfil'],
                "monedas": int(perfil_actualizado['monedas'])
            }

            return Response(
                {
                    "message": "Reto iniciado exitosamente",
                    "progreso": progreso_serializable,
                    "perfil": perfil_serializable
                },
                status=status.HTTP_201_CREATED
            )

        except DatabaseError as e:
            # Error de SQL (por ejemplo, monedas insuficientes)
            error_msg = str(e)
            if "Monedas insuficientes" in error_msg:
                return Response(
                    {"detail": "No tienes suficientes monedas para iniciar este reto"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                {"detail": f"Error de base de datos: {error_msg}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            # Logging detallado del error
            import traceback
            error_traceback = traceback.format_exc()
            print(f"ERROR en IniciarRetoView: {type(e).__name__}: {str(e)}")
            print(f"Traceback:\n{error_traceback}")

            return Response(
                {"detail": f"{type(e).__name__}: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
