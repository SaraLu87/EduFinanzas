from flask import jsonify, request
from db import get_connection


# ✅ Obtener todos los temas

def obtener_temas():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id_tema, nombre, descripcion FROM temas")
        resultados = cursor.fetchall()

        # Detectar automáticamente si son tuplas o diccionarios
        temas = []
        for fila in resultados:
            if isinstance(fila, dict):
                temas.append({
                    "id_tema": fila["id_tema"],
                    "nombre": fila["nombre"],
                    "descripcion": fila["descripcion"]
                })
            else:
                temas.append({
                    "id_tema": fila[0],
                    "nombre": fila[1],
                    "descripcion": fila[2]
                })

        return jsonify({
            "message": "Temas obtenidos correctamente ✅",
            "temas": temas
        }), 200

    except Exception as e:
        import traceback
        print("❌ Error al obtener temas:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()



# ✅ Crear un nuevo tema
def crear_tema():
    data = request.get_json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    if not nombre:
        return jsonify({"error": "El nombre del tema es obligatorio"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO temas (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))
        conn.commit()
        return jsonify({"message": "Tema creado correctamente 🎯"}), 201

    except Exception as e:
        print("❌ Error al crear tema:", e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        cursor.close()
        conn.close()
