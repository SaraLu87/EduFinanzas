from django.db import connection, DatabaseError


def tip_crear(nombre: str, descripcion: str, id_perfil: int = None):
    """
    Crea un nuevo tip periódico usando el procedimiento almacenado 'tip_crear'
    Si no se proporciona id_perfil, se usa 1 por defecto (perfil administrador)
    """
    try:
        # Si no hay id_perfil, usar 1 como valor por defecto (perfil admin/sistema)
        if id_perfil is None:
            id_perfil = 1

        with connection.cursor() as cursor:
            cursor.callproc('tip_crear', [id_perfil, nombre, descripcion])
            row = cursor.fetchone()
            return int(row[0]) if row else None
    except DatabaseError as e:
        raise


def tip_ver(id_recompensa: int):
    """
    Obtiene un tip periódico por su ID
    """
    with connection.cursor() as cursor:
        cursor.callproc('tip_ver', [id_recompensa])
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id_recompensa": row[0],
            "id_perfil": row[1],
            "nombre": row[2],
            "descripcion": row[3],
        }


def tip_listar():
    """
    Lista todos los tips periódicos con información del perfil asociado
    """
    with connection.cursor() as cursor:
        cursor.callproc('tip_listar')
        rows = cursor.fetchall()
        return [
            {
                "id_recompensa": r[0],
                "nombre_perfil": r[1],
                "nombre": r[2],
                "descripcion": r[3],
            } for r in rows
        ]


def tip_actualizar(id_recompensa: int, nombre: str, descripcion: str) -> int:
    """
    Actualiza un tip periódico existente
    """
    with connection.cursor() as cursor:
        cursor.callproc('tip_actualizar', [id_recompensa, nombre, descripcion])
        row = cursor.fetchone()
        return int(row[0]) if row else 0


def tip_eliminar(id_recompensa: int) -> int:
    """
    Elimina un tip periódico por su ID
    """
    with connection.cursor() as cursor:
        cursor.callproc('tip_eliminar', [id_recompensa])
        row = cursor.fetchone()
        return int(row[0]) if row else 0
