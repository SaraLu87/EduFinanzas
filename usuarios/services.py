import jwt
from django.conf import settings
from django.db import connection, DatabaseError
from django.contrib.auth.models import User
from .serializers import UsuarioSerializer
from .models import Usuarios

u = User()

def usuarios_crear(correo: str, contrasena: str, rol: str):
    """
    Crea un nuevo usuario en la base de datos.
    Llama al procedimiento almacenado 'usuarios_crear'.
    """
    try:
        with connection.cursor() as cursor:
            u.set_password(contrasena)
            hash_con = u.password
            cursor.callproc('usuarios_crear', [correo, hash_con, rol])
            # Puedes devolver el último ID insertado
            cursor.execute("SELECT LAST_INSERT_ID();")
            row = cursor.fetchone()
            id_usuario = int(row[0]) if row else None
        
        usuario_id = Usuarios.objects.get(id_usuario=id_usuario)
        payload = {
            "id_usuario": usuario_id.id_usuario,
            "correo": usuario_id.correo
            # Sin expiración
        }

        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        serializer = UsuarioSerializer(usuario_id)
        
        return {
            "token": token,
            "usuario": serializer.data 
        }
    except DatabaseError as e:
        raise


def usuario_ver(id_usuario: int):
    """
    Obtiene un usuario por su ID.
    """
    with connection.cursor() as cursor:
        cursor.callproc('usuario_ver', [id_usuario])
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id_usuario": row[0],
            "correo": row[1],
            "rol": row[2],
            "fecha_registro": row[3],
        }


def usuarios_listar():
    """
    Lista todos los usuarios registrados.
    """
    with connection.cursor() as cursor:
        cursor.callproc('usuarios_listar')
        rows = cursor.fetchall()
        return [
            {
                "id_usuario": r[0],
                "correo": r[1],
                "rol": r[2],
                "fecha_registro": r[3],
            } for r in rows
        ]


def usuarios_actualizar(id_usuario: int, correo: str, contrasena: str, rol: str) -> int:
    """
    Actualiza los datos de un usuario existente.
    """
    with connection.cursor() as cursor:
        cursor.callproc('usuarios_actualizar', [id_usuario, correo, contrasena, rol])
        cursor.execute("SELECT ROW_COUNT();")
        row = cursor.fetchone()
        return int(row[0]) if row else 0


def usuarios_eliminar(id_usuario: int) -> int:
    """
    Elimina un usuario por su ID.
    """
    with connection.cursor() as cursor:
        cursor.callproc('usuarios_eliminar', [id_usuario])
        cursor.execute("SELECT ROW_COUNT();")
        row = cursor.fetchone()
        return int(row[0]) if row else 0
