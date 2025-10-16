from django.db import connection, DatabaseError

def perfil_crear(id_usuario: int, nombre_perfil: str, foto_perfil: str):
    """Crea un nuevo perfil."""
    try:
        with connection.cursor() as cursor:
            cursor.callproc('perfil_crear', [id_usuario, nombre_perfil, foto_perfil])
            row = cursor.fetchone()
            return int(row[0]) if row else None
    except DatabaseError as e:
        raise


def perfil_listar():
    """Lista todos los perfiles junto con el correo del usuario."""
    with connection.cursor() as cursor:
        cursor.callproc('perfil_listar')
        rows = cursor.fetchall()
        return [
            {
                "id_perfil": r[0],
                "correo": r[1],
                "nombre_perfil": r[2],
                "monedas": r[3],
            } for r in rows
        ]


def perfil_ver(id_perfil: int):
    """Obtiene un perfil por su ID."""
    with connection.cursor() as cursor:
        cursor.callproc('perfil_ver', [id_perfil])
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id_perfil": row[0],
            "id_usuario": row[1],
            "nombre_perfil": row[2],
            "foto_perfil": row[3],
            "tema_actual": row[4],
            "monedas": row[5],
        }


def perfil_actualizar(id_perfil: int, nombre_perfil: str, foto_perfil: str, tema_actual: int, monedas: int) -> int:
    """Actualiza los datos de un perfil."""
    with connection.cursor() as cursor:
        cursor.callproc('perfil_actualizar', [id_perfil, nombre_perfil, foto_perfil, tema_actual, monedas])
        row = cursor.fetchone()
        return int(row[0]) if row else 0


def perfil_eliminar(id_perfil: int) -> int:
    """Elimina un perfil por su ID."""
    with connection.cursor() as cursor:
        cursor.callproc('perfil_eliminar', [id_perfil])
        row = cursor.fetchone()
        return int(row[0]) if row else 0
