from flask import Blueprint
from controllers.reto_controller import obtener_retos, crear_reto

reto_bp = Blueprint("reto_bp", __name__)

# ✅ Obtener todos los retos
@reto_bp.route("/api/retos", methods=["GET"])
def get_retos():
    return obtener_retos()

# ✅ Crear un reto
@reto_bp.route("/api/retos", methods=["POST"])
def post_reto():
    return crear_reto()
