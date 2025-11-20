from django.db import connection, DatabaseError
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

def retos_crear(nombre_reto, id_tema, descripcion, pregunta, img_reto=None,
                recompensa_monedas=10, costo_monedas=5,
                respuesta_uno='', respuesta_dos='', respuesta_tres='',
                respuesta_cuatro='', respuestaCorrecta=''):
    """
    Crea un nuevo reto. img_reto es opcional.
    """
    try:
        with connection.cursor() as cursor:
            cursor.callproc('retos_crear', [
                nombre_reto,
                id_tema,
                descripcion,
                pregunta,
                img_reto,
                recompensa_monedas,
                costo_monedas,
                respuesta_uno,
                respuesta_dos,
                respuesta_tres,
                respuesta_cuatro,
                respuestaCorrecta
            ])
            row = cursor.fetchone()
            return int(row[0]) if row else None
    except DatabaseError as e:
        raise


def reto_ver(id_reto: int):
    with connection.cursor() as cursor:
        cursor.callproc('reto_ver', [id_reto])
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id_reto": row[0],
            "nombre_reto": row[1],
            "id_tema": row[2],
            "descripcion": row[3],
            "pregunta": row[4],
            "img_reto": row[5],
            "recompensa_monedas": row[6],
            "costo_monedas": row[7],
            "respuesta_uno": row[8],
            "respuesta_dos": row[9],
            "respuesta_tres": row[10],
            "respuesta_cuatro": row[11],
            "respuestaCorrecta": row[12]
        }


def retos_listar():
    with connection.cursor() as cursor:
        cursor.callproc('retos_listar')
        rows = cursor.fetchall()
        return [
            {
                "id_reto": r[0],
                "nombre_reto": r[1],
                "id_tema": r[2],
                "descripcion": r[3],
                "pregunta": r[4],
                "img_reto": r[5],
                "recompensa_monedas": r[6],
                "costo_monedas": r[7],
                "respuesta_uno": r[8],
                "respuesta_dos": r[9],
                "respuesta_tres": r[10],
                "respuesta_cuatro": r[11],
                "respuestaCorrecta": r[12]
            } for r in rows
        ]


def retos_actualizar(id_reto, nombre_reto, id_tema, descripcion, pregunta, img_reto=None,
                     recompensa_monedas=10, costo_monedas=5,
                     respuesta_uno='', respuesta_dos='',
                     respuesta_tres='', respuesta_cuatro='',
                     respuestaCorrecta='') -> int:
    """
    Actualiza un reto existente. img_reto es opcional.
    """
    try:
        with connection.cursor() as cursor:
            cursor.callproc('retos_actualizar', [
                id_reto,
                nombre_reto,
                id_tema,
                descripcion,
                pregunta,
                img_reto,
                recompensa_monedas,
                costo_monedas,
                respuesta_uno,
                respuesta_dos,
                respuesta_tres,
                respuesta_cuatro,
                respuestaCorrecta
            ])
            row = cursor.fetchone()
            return int(row[0]) if row else 0
    except DatabaseError as e:
        raise


def retos_eliminar(id_reto: int) -> int:
    with connection.cursor() as cursor:
        cursor.callproc('retos_eliminar', [id_reto])
        row = cursor.fetchone()
        return int(row[0]) if row else 0


def obtener_retos_por_tema_service(id_tema: int, id_perfil: int):
    """
    Obtiene todos los retos de un tema con el progreso del usuario.
    Usa el SP obtener_retos_por_tema.
    """
    with connection.cursor() as cursor:
        cursor.callproc('obtener_retos_por_tema', [id_tema, id_perfil])
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
    return [dict(zip(columns, row)) for row in results]
