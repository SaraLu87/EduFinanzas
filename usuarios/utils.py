"""
Utilidades para trabajar con JWT y autenticación de usuario
"""
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def extraer_usuario_de_token(request):
    """
    Extrae el id_usuario del token JWT en el header Authorization

    Args:
        request: Request object de DRF

    Returns:
        int: id_usuario extraído del token

    Raises:
        AuthenticationFailed: Si el token no existe o es inválido
    """
    # Obtener el header Authorization
    auth_header = request.headers.get('Authorization', '')

    if not auth_header:
        raise AuthenticationFailed('Token no proporcionado')

    # El formato esperado es: "Bearer <token>"
    try:
        token = auth_header.split(' ')[1]
    except IndexError:
        raise AuthenticationFailed('Formato de token inválido')

    # Decodificar el token
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        id_usuario = payload.get('id_usuario')

        if not id_usuario:
            raise AuthenticationFailed('Token no contiene id_usuario')

        return int(id_usuario)

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token expirado')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Token inválido')


def obtener_perfil_de_usuario(id_usuario):
    """
    Obtiene el perfil asociado a un id_usuario usando el SP

    Args:
        id_usuario (int): ID del usuario

    Returns:
        dict: Datos del perfil o None si no existe
    """
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.callproc('obtener_perfil_por_usuario', [id_usuario])
        columns = [col[0] for col in cursor.description]
        result = cursor.fetchone()

    if result:
        return dict(zip(columns, result))
    return None
