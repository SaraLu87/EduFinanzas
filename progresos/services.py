from django.db import connection

def progreso_crear(p_id_perfil, p_id_reto, p_completado, p_fecha_completado):
    """
    Llama al procedimiento almacenado `progresos_crear`
    para insertar un nuevo registro en la tabla progreso.
    """
    with connection.cursor() as cursor:
        cursor.callproc('progresos_crear', [
            p_id_perfil,
            p_id_reto,
            p_completado,
            p_fecha_completado
        ])
        result = cursor.fetchall()
    # Retorna el id del nuevo progreso
    return result[0][0] if result else None


def progreso_ver(p_id):
    """
    Obtiene un progreso específico por su ID usando `progreso_ver`.
    """
    with connection.cursor() as cursor:
        cursor.callproc('progreso_ver', [p_id])
        columns = [col[0] for col in cursor.description]
        result = cursor.fetchone()
    if result:
        return dict(zip(columns, result))
    return None


def progreso_listar():
    """
    Retorna todos los progresos registrados usando `progresos_listar`.
    """
    with connection.cursor() as cursor:
        cursor.callproc('progresos_listar')
        columns = [col[0] for col in cursor.description]
        results = cursor.fetchall()
    return [dict(zip(columns, row)) for row in results]


def progreso_actualizar(p_id, p_id_perfil, p_id_reto, p_completado, p_fecha_completado):
    """
    Actualiza un progreso existente llamando a `progresos_actualizar`.
    Retorna el número de filas afectadas.
    """
    with connection.cursor() as cursor:
        cursor.callproc('progresos_actualizar', [
            p_id,
            p_id_perfil,
            p_id_reto,
            p_completado,
            p_fecha_completado
        ])
        result = cursor.fetchall()
    return result[0][0] if result else 0


def progreso_eliminar(p_id):
    """
    Elimina un progreso por su ID usando `progresos_eliminar`.
    Retorna el número de filas afectadas.
    """
    with connection.cursor() as cursor:
        cursor.callproc('progresos_eliminar', [p_id])
        result = cursor.fetchall()
    return result[0][0] if result else 0
