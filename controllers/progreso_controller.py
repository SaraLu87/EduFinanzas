from flask import jsonify, request
from db import get_connection

# ✅ Obtener progreso de un perfil
def obtener_progreso(id_perfil):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT p.id_progreso, p.completado, p.fecha_completado, r.nombre_reto, r.recompensa_monedas
            FROM progreso p
            JOIN retos r ON p.id_reto = r.id_reto
            WHERE p.id_perfil = %s
        """, (id_perfil,))
        progreso = cursor.fetchall()
        return jsonify({
            "message": "Progreso obtenido correctamente ✅",
            "progreso": progreso
        }), 200

    except Exception as e:
        print("❌ Error al obtener progreso:", e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        cursor.close()
        conn.close()


# ✅ Actualizar progreso (marcar como completado)
def actualizar_progreso():
    data = request.get_json()
    id_perfil = data.get("id_perfil")
    id_reto = data.get("id_reto")
    respuesta = data.get("respuesta_seleccionada")

    if not id_perfil or not id_reto:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE progreso
            SET completado = TRUE, fecha_completado = NOW(), respuesta_seleccionada = %s
            WHERE id_perfil = %s AND id_reto = %s
        """, (respuesta, id_perfil, id_reto))
        conn.commit()

        return jsonify({"message": "Progreso actualizado correctamente ✅"}), 200

    except Exception as e:
        print("❌ Error al actualizar progreso:", e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        cursor.close()
        conn.close()
