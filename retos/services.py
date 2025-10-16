from django.db import connection, DatabaseError

def retos_crear(tipo_pregunta, nombre_reto, id_tema, descripcion, recompensa_monedas,
                respuesta_uno, respuesta_dos, respuesta_tres, respuesta_cuatro, respuestaCorrecta):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('crear_reto', [
                tipo_pregunta, nombre_reto, id_tema, descripcion,
                recompensa_monedas, respuesta_uno, respuesta_dos,
                respuesta_tres, respuesta_cuatro, respuestaCorrecta
            ])
            row = cursor.fetchone()
            return int(row[0]) if row else None
    except DatabaseError as e:
        raise

def reto_ver(id_reto: int):
    with connection.cursor() as cursor:
        cursor.callproc('ver_reto', [id_reto])
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id_reto": row[0],
            "tipo_pregunta": row[1],
            "nombre_reto": row[2],
            "id_tema": row[3],
            "descripcion": row[4],
            "recompensa_monedas": row[5],
            "respuesta_uno": row[6],
            "respuesta_dos": row[7],
            "respuesta_tres": row[8],
            "respuesta_cuatro": row[9],
            "respuestaCorrecta": row[10],
        }

def retos_listar():
    with connection.cursor() as cursor:
        cursor.callproc('listar_reto')
        rows = cursor.fetchall()
        return [
            {
                "id_reto": r[0],
                "tipo_pregunta": r[1],
                "nombre_reto": r[2],
                "id_tema": r[3],
                "descripcion": r[4],
                "recompensa_monedas": r[5],
                "respuesta_uno": r[6],
                "respuesta_dos": r[7],
                "respuesta_tres": r[8],
                "respuesta_cuatro": r[9],
                "respuestaCorrecta": r[10],
            } for r in rows
        ]

def retos_actualizar(id_reto, tipo_pregunta, nombre_reto, id_tema, descripcion,
                     recompensa_monedas, respuesta_uno, respuesta_dos,
                     respuesta_tres, respuesta_cuatro, respuestaCorrecta) -> int:
    with connection.cursor() as cursor:
        cursor.callproc('actualizar_reto', [
            id_reto, tipo_pregunta, nombre_reto, id_tema, descripcion,
            recompensa_monedas, respuesta_uno, respuesta_dos,
            respuesta_tres, respuesta_cuatro, respuestaCorrecta
        ])
        row = cursor.fetchone()
        return int(row[0]) if row else 0

def retos_eliminar(id_reto: int) -> int:
    with connection.cursor() as cursor:
        cursor.callproc('eliminar_reto', [id_reto])
        row = cursor.fetchone()
        return int(row[0]) if row else 0

