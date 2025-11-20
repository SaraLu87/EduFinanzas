"""
Views para funcionalidades de perfil de usuario autenticado
Estos endpoints extraen el perfil del token JWT
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from usuarios.utils import extraer_usuario_de_token, obtener_perfil_de_usuario
from usuarios.services import usuarios_actualizar
from .services import perfil_actualizar
from progresos.services import calcular_progreso_usuario_service, obtener_progreso_por_temas_service


class PerfilMeView(APIView):
    """
    Endpoint para obtener el perfil del usuario autenticado
    GET /api/perfil/me/
    """

    def get(self, request):
        """Obtiene el perfil del usuario desde el token JWT"""
        try:
            # Extraer id_usuario del token
            id_usuario = extraer_usuario_de_token(request)

            # Obtener perfil asociado
            perfil = obtener_perfil_de_usuario(id_usuario)

            if not perfil:
                return Response(
                    {"detail": "Perfil no encontrado para este usuario"},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(perfil, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )


class PerfilMeUpdateView(APIView):
    """
    Endpoint para actualizar el perfil del usuario autenticado
    PUT /api/perfil/me/update/
    Permite actualizar: nombre_perfil y/o contraseña
    """

    def put(self, request):
        """Actualiza el perfil y/o contraseña del usuario"""
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

            id_perfil = perfil['id_perfil']

            # Extraer datos del request
            nombre_perfil = request.data.get('nombre_perfil')
            contrasena = request.data.get('contrasena')

            # Actualizar nombre_perfil si se proporciona
            if nombre_perfil:
                perfil_actualizar(
                    id_perfil=id_perfil,
                    nombre_perfil=nombre_perfil,
                    foto_perfil=perfil['foto_perfil'],
                    edad=perfil['edad'],
                    monedas=perfil['monedas']
                )

            # Actualizar contraseña si se proporciona
            if contrasena:
                from usuarios.services import usuario_ver
                usuario = usuario_ver(id_usuario)

                if not usuario:
                    return Response(
                        {"detail": "Usuario no encontrado"},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Actualizar contraseña
                usuarios_actualizar(
                    id_usuario=id_usuario,
                    correo=usuario['correo'],
                    rol=usuario['rol'],
                    contrasena=contrasena
                )

            # Retornar perfil actualizado
            perfil_actualizado = obtener_perfil_de_usuario(id_usuario)
            return Response(
                {
                    "message": "Perfil actualizado exitosamente",
                    "perfil": perfil_actualizado
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"detail": f"Error al actualizar perfil: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProgresoMeView(APIView):
    """
    Endpoint para obtener el progreso general del usuario autenticado
    GET /api/perfil/me/progreso/
    """

    def get(self, request):
        """Calcula y retorna el progreso del usuario"""
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

            # Calcular progreso usando el SP
            progreso = calcular_progreso_usuario_service(perfil['id_perfil'])

            if progreso is None:
                return Response(
                    {"detail": "Error al calcular progreso"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(progreso, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ProgresoTemasView(APIView):
    """
    Endpoint para obtener el progreso por temas del usuario autenticado
    GET /api/perfil/me/progreso-temas/
    Retorna un array con el progreso de cada tema:
    - id_tema
    - nombre_tema
    - total_retos
    - retos_completados
    - esta_completado (boolean)
    """

    def get(self, request):
        """Obtiene el progreso por temas del usuario"""
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

            # Obtener progreso por temas usando el SP
            progreso_temas = obtener_progreso_por_temas_service(perfil['id_perfil'])

            return Response(progreso_temas, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
