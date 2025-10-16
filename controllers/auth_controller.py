from db import get_connection
from flask import jsonify, request

# ✅ Registro de usuario + creación de perfil
def register_user():
    data = request.get_json()
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    rol = data.get("rol")
    nombre_perfil = data.get("nombre_perfil")

    if not all([correo, contrasena, rol, nombre_perfil]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Verificar si el correo ya existe
        cursor.execute("SELECT id_usuario FROM usuarios WHERE correo = %s", (correo,))
        if cursor.fetchone():
            return jsonify({"error": "El correo ya está registrado"}), 409

        # Crear usuario
        query_user = "INSERT INTO usuarios (correo, contrasena, rol) VALUES (%s, %s, %s)"
        cursor.execute(query_user, (correo, contrasena, rol))
        conn.commit()

        id_usuario = cursor.lastrowid

        # Crear perfil asociado
        query_perfil = """
            INSERT INTO perfiles (id_usuario, nombre_perfil, foto_perfil, tema_actual, monedas, saldo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_perfil, (id_usuario, nombre_perfil, None, 1, 0, 0))
        conn.commit()

        return jsonify({
            "message": "✅ Usuario y perfil creados exitosamente",
            "id_usuario": id_usuario
        }), 201

    except Exception as e:
        print("❌ Error al registrar:", e)
        return jsonify({"error": "Error al crear usuario"}), 500

    finally:
        cursor.close()
        conn.close()


# ✅ Login de usuario
def login_user():
    data = request.get_json()
    correo = data.get("correo")
    contrasena = data.get("contrasena")

    if not correo or not contrasena:
        return jsonify({"error": "Correo y contraseña son obligatorios"}), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT u.id_usuario, u.correo, u.rol, p.nombre_perfil, p.monedas, p.saldo, p.tema_actual
            FROM usuarios u
            JOIN perfiles p ON u.id_usuario = p.id_usuario
            WHERE u.correo = %s AND u.contrasena = %s
        """
        cursor.execute(query, (correo, contrasena))
        result = cursor.fetchone()

        if not result:
            return jsonify({"error": "Credenciales incorrectas"}), 401

        return jsonify({
            "message": "Inicio de sesión exitoso ✅",
            "user": result
        }), 200

    except Exception as e:
        print("❌ Error al iniciar sesión:", e)
        return jsonify({"error": "Error interno del servidor"}), 500

    finally:
        cursor.close()
        conn.close()
