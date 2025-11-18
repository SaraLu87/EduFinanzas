import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from usuarios.services import usuario_ver

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
        usuario = usuario_ver(payload.get("id_usuario"))
        if not usuario:
            raise exceptions.AuthenticationFailed("Usuario no encontrado")

        # DRF espera (user, auth)
        # user → objeto que represente al usuario
        # auth → el token o payload
        print(usuario, payload, "  LUNA")
        return usuario, payload
