from flask import jsonify, request
from db import get_connection


# ✅ Obtener todos los retos
def obtener_retos():
    conn = get_connection()
    cursor = conn.cursor()  # no dictionary=True para manejar ambos casos

    try:
        cursor.execute("""
            SELECT r.*, t.nombre AS tema_nombre
            FROM retos r
            JOIN temas t ON r.id_tema = t.id_tema
        """)
        resultados = cursor.fetchall()

        retos = []
        for fila in resultados:
            # Si la fila es diccionario (MySQL Connector con dictionary=True)
            if isinstance(fila, dict):
                retos.append({
                    "id_reto": fila.get("id_reto"),
                    "tipo": fila.get("tipo", ""),
                    "pregunta": fila.get("pregunta", ""),
                    "id_tema": fila.get("id_tema"),
                    "tema_nombre": fila.get("tema_nombre", ""),
                    "descripcion": fila.get("descripcion", ""),
                    "recompensa_monedas": fila.get("recompensa_monedas", 0),
                    "respuesta_uno": fila.get("respuesta_uno", ""),
                    "respuesta_dos": fila.get("respuesta_dos", ""),
                    "respuesta_tres": fila.get("respuesta_tres", ""),
                    "respuesta_cuatro": fila.get("respuesta_cuatro", ""),
                    "respuestaCorrecta": fila.get("respuestaCorrecta", "")
                })
            else:
                # Si es tupla
                retos.append({
                    "id_reto": fila[0],
                    "tipo": fila[1],
                    "pregunta": fila[2],
                    "id_tema": fila[3],
                    "descripcion": fila[4],
                    "recompensa_monedas": fila[5],
                    "respuesta_uno": fila[6],
                    "respuesta_dos": fila[7],
                    "respuesta_tres": fila[8],
                    "respuesta_cuatro": fila[9],
                    "respuestaCorrecta": fila[10],
                    "tema_nombre": fila[11]
                })

        return jsonify({
            "message": "Retos obtenidos correctamente ✅",
            "retos": retos
        }), 200

    except Exception as e:
        import traceback
        print("❌ Error al obtener retos:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()



# ✅ Crear un nuevo reto
def crear_reto():
    data = request.get_json()
    tipo = data.get("tipo_pregunta")
    nombre = data.get("nombre_reto")
    id_tema = data.get("id_tema")
    descripcion = data.get("descripcion")
    recompensa = data.get("recompensa_monedas", 0)
    respuestas = [
        data.get("respuesta_uno"),
        data.get("respuesta_dos"),
        data.get("respuesta_tres"),
        data.get("respuesta_cuatro")
    ]
    correcta = data.get("respuestaCorrecta")

    if not nombre or not id_tema or not correcta:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO retos (tipo_pregunta, nombre_reto, id_tema, descripcion, recompensa_monedas,
                               respuesta_uno, respuesta_dos, respuesta_tres, respuesta_cuatro, respuestaCorrecta)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (tipo, nombre, id_tema, descripcion, recompensa, *respuestas, correcta))
        conn.commit()
        return jsonify({"message": "Reto creado correctamente 🎯"}), 201

    except Exception as e:
        print("❌ Error al crear reto:", e)
        return jsonify({"error": "Error interno"}), 500

    finally:
        cursor.close()
        conn.close()
