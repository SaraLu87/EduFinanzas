from flask import jsonify, request
from db import get_connection

# ✅ Obtener tips de un perfil
def obtener_tips(id_perfil):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM tips_periodicas WHERE id_perfil = %s", (id_perfil,))
        tips = cursor.fetchall()
        return jsonify({
            "message": "Tips obtenidos correctamente ✅",
            "tips": tips
        }), 200

    except Exception as e:
        print("❌ Error al obtener tips:", e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        cursor.close()
        conn.close()


# ✅ Crear nuevo tip
def crear_tip():
    data = request.get_json()
    id_perfil = data.get("id_perfil")
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    if not id_perfil or not nombre:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO tips_periodicas (id_perfil, nombre, descripcion)
            VALUES (%s, %s, %s)
        """, (id_perfil, nombre, descripcion))
        conn.commit()
        return jsonify({"message": "Tip agregado correctamente 💡"}), 201

    except Exception as e:
        print("❌ Error al agregar tip:", e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        cursor.close()
        conn.close()
