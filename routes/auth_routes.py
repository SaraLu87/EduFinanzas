from flask import Blueprint, jsonify
from controllers.auth_controller import register_user, login_user
from db import get_connection

auth_bp = Blueprint("auth_bp", __name__)

# ✅ Ruta de prueba de conexión
@auth_bp.route("/api/test-db", methods=["GET"])
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS total_usuarios FROM usuarios;")
        result = cursor.fetchone()
        conn.close()

        return jsonify({
            "status": "ok",
            "message": "Conexión exitosa a la base de datos MySQL 🎉",
            "data": result
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ✅ Registro de usuario
@auth_bp.route("/api/register", methods=["POST"])
def register():
    return register_user()


# ✅ Login de usuario
@auth_bp.route("/api/login", methods=["POST"])
def login():
    return login_user()
