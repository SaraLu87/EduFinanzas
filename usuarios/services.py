from django.db import connection, DatabaseError

def usuarios_crear(correo: str, contrasena: str, rol: str):
    """
    Crea un nuevo usuario en la base de datos.
    Llama al procedimiento almacenado 'usuarios_crear'.
    """
    try:
        with connection.cursor() as cursor:
            cursor.callproc('usuarios_crear', [correo, contrasena, rol])
            # Puedes devolver el último ID insertado
            cursor.execute("SELECT LAST_INSERT_ID();")
            row = cursor.fetchone()
            return int(row[0]) if row else None
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
