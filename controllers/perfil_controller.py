from flask import jsonify, request
from db import get_connection

# ✅ Obtener perfil de usuario
def obtener_perfil(id_usuario):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT u.id_usuario, u.correo, u.rol, p.nombre_perfil, p.foto_perfil, p.monedas, p.saldo, p.tema_actual
            FROM usuarios u
            JOIN perfiles p ON u.id_usuario = p.id_usuario
            WHERE u.id_usuario = %s
        """
        cursor.execute(query, (id_usuario,))
        perfil = cursor.fetchone()

        if not perfil:
            return jsonify({"error": "Perfil no encontrado"}), 404

        return jsonify({
            "message": "Perfil obtenido correctamente ✅",
            "perfil": perfil
        }), 200

    except Exception as e:
        print("❌ Error al obtener perfil:", e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        cursor.close()
        conn.close()
        
# # ✅ Eliminar perfil con cascada
# def eliminar_perfil(id_usuario):
#     conn = get_connection()
#     cursor = conn.cursor()

#     try:
#         # Iniciar transacción
#         cursor.execute("START TRANSACTION")

#         # Eliminar registros relacionados en progreso
#         cursor.execute("DELETE FROM progreso WHERE id_usuario = %s", (id_usuario,))

#         # Eliminar perfil
#         cursor.execute("DELETE FROM perfiles WHERE id_usuario = %s", (id_usuario,))

#         # Eliminar usuario
#         cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))

#         conn.commit()

#         return jsonify({"message": "Perfil y datos asociados eliminados correctamente ✅"}), 200

#     except Exception as e:
#         conn.rollback()
#         print("❌ Error al eliminar perfil:", e)
#         return jsonify({"error": "Error interno al eliminar"}), 500

#     finally:
#         cursor.close()
#         conn.close()

# ✅ Editar nombre o correo
def editar_perfil(id_usuario):
    data = request.get_json()
    nuevo_nombre = data.get("nombre_perfil")
    nuevo_correo = data.get("correo")

    if not nuevo_nombre and not nuevo_correo:
        return jsonify({"error": "Debes enviar al menos un campo para actualizar"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Actualizar correo si se envía
        if nuevo_correo:
            cursor.execute("UPDATE usuarios SET correo = %s WHERE id_usuario = %s", (nuevo_correo, id_usuario))

        # Actualizar nombre si se envía
        if nuevo_nombre:
            cursor.execute("UPDATE perfiles SET nombre_perfil = %s WHERE id_usuario = %s", (nuevo_nombre, id_usuario))

        conn.commit()

        return jsonify({"message": "Perfil actualizado correctamente ✅"}), 200

    except Exception as e:
        print("❌ Error al editar perfil:", e)
        return jsonify({"error": "Error interno al actualizar"}), 500

    finally:
        cursor.close()
        conn.close()


# ✅ Agregar monedas
def agregar_monedas():
    data = request.get_json()
    id_usuario = data.get("id_usuario")
    cantidad = data.get("cantidad")

    if not id_usuario or cantidad is None:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE perfiles SET monedas = monedas + %s WHERE id_usuario = %s", (cantidad, id_usuario))
        conn.commit()

        return jsonify({"message": f"Se agregaron {cantidad} monedas correctamente 🪙"}), 200

    except Exception as e:
        print("❌ Error al agregar monedas:", e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        cursor.close()
        conn.close()


# ✅ Actualizar saldo (ejemplo: en juegos financieros)
def actualizar_saldo():
    data = request.get_json()
    id_usuario = data.get("id_usuario")
    saldo = data.get("nuevo_saldo")

    if not id_usuario or saldo is None:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE perfiles SET saldo = %s WHERE id_usuario = %s", (saldo, id_usuario))
        conn.commit()

        return jsonify({"message": "Saldo actualizado correctamente 💰"}), 200

    except Exception as e:
        print("❌ Error al actualizar saldo:", e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        cursor.close()
        conn.close()

# ✅ Eliminar perfil con cascada
def eliminar_perfil(id_usuario):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Iniciar transacción
        cursor.execute("START TRANSACTION")

        # Eliminar registros relacionados en progreso
        cursor.execute("DELETE FROM progreso WHERE id_usuario = %s", (id_usuario,))

        # Eliminar perfil
        cursor.execute("DELETE FROM perfiles WHERE id_usuario = %s", (id_usuario,))

        # Eliminar usuario
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))

        conn.commit()

        return jsonify({"message": "Perfil y datos asociados eliminados correctamente ✅"}), 200

    except Exception as e:
        conn.rollback()
        print("❌ Error al eliminar perfil:", e)
        return jsonify({"error": "No se pudo eliminar el perfil debido a restricciones de seguridad. "}), 403

    finally:
        cursor.close()
        conn.close()