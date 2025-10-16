from flask import jsonify, request
from db import get_connection

def update_usuario(id_usuario):
    data = request.get_json()
    nombre_perfil = data.get("nombre_perfil")
    correo = data.get("correo")

    if not nombre_perfil or not correo:
        return jsonify({"message": "Faltan campos"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE usuarios u
            JOIN perfiles p ON u.id_usuario = p.id_usuario
            SET u.correo = %s, p.nombre_perfil = %s
            WHERE u.id_usuario = %s
        """, (correo, nombre_perfil, id_usuario))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "Usuario no encontrado"}), 404

        return jsonify({"message": "Perfil actualizado correctamente"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
