from django.db import connection

def solucionar_reto_service(id_perfil, id_reto, respuesta_seleccionada):
    with connection.cursor() as cursor:
        cursor.callproc('solucionar_reto', [id_perfil, id_reto, respuesta_seleccionada])
        resultado = cursor.fetchall()
        columnas = [col[0] for col in cursor.description] if cursor.description else []
    return [dict(zip(columnas, fila)) for fila in resultado] if resultado else None
