from django.db import connection, DatabaseError

def temas_crear(nombre: str, descripcion: str, precio: int):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('temas_crear', [nombre, descripcion, precio])
            row = cursor.fetchone()
            return int(row[0]) if row else None
    except DatabaseError as e:
        raise


def tema_ver(id_tema: int):
    with connection.cursor() as cursor:
        cursor.callproc('tema_ver', [id_tema])
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id_tema": row[0],
            "nombre": row[1],
            "descripcion": row[2],
            "precio": row[3],
        }


def temas_listar():
    with connection.cursor() as cursor:
        cursor.callproc('temas_listar')
        rows = cursor.fetchall()
        return [
            {
                "id_tema": r[0],
                "nombre": r[1],
                "descripcion": r[2],
                "precio": r[3],
            } for r in rows
        ]


def temas_actualizar(id_tema: int, nombre: str, descripcion: str, precio: int) -> int:
    with connection.cursor() as cursor:
        cursor.callproc('temas_actualizar', [id_tema, nombre, descripcion, precio])
        row = cursor.fetchone()
        return int(row[0]) if row else 0


def temas_eliminar(id_tema: int) -> int:
    with connection.cursor() as cursor:
        cursor.callproc('temas_eliminar', [id_tema])
        row = cursor.fetchone()
        return int(row[0]) if row else 0
