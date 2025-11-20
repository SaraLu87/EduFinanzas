import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from usuarios.services import usuario_ver


class User:
    """
    Clase simple para representar un usuario autenticado.
    Actúa como wrapper para los datos del usuario que vienen del servicio.
    """
    def __init__(self, user_data):
        self.id_usuario = user_data.get("id_usuario")
        self.correo = user_data.get("correo")
        self.rol = user_data.get("rol")
        self.fecha_registro = user_data.get("fecha_registro")
        self.is_authenticated = True  # Siempre es True para usuarios autenticados

    def __str__(self):
        return f"{self.correo} ({self.rol})"


class JWTAuthentication(BaseAuthentication):
    """
    Autenticación personalizada con JWT para DRF
    """
    def authenticate(self, request):
        # Obtener el header Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None  # No hay token → DRF sigue con otras clases

        # Quitar el prefijo "Bearer "
        token = auth_header.replace("Bearer ", "")

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("El token ha expirado")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Token inválido")

        # Buscar el usuario en tu servicio
        usuario_data = usuario_ver(payload.get("id_usuario"))
        if not usuario_data:
            raise exceptions.AuthenticationFailed("Usuario no encontrado")

        # Crear objeto User con los datos del usuario
        usuario = User(usuario_data)

        # DRF espera (user, auth)
        # user → objeto que represente al usuario
        # auth → el token o payload
        return usuario, payload
