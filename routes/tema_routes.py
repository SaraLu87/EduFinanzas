from flask import Blueprint
from controllers.tema_controller import obtener_temas, crear_tema

tema_bp = Blueprint("tema_bp", __name__)

# ✅ Obtener todos los temas
@tema_bp.route("/api/temas", methods=["GET"])
def get_temas():
    return obtener_temas()

# ✅ Crear un tema
@tema_bp.route("/api/temas", methods=["POST"])
def post_tema():
    return crear_tema()
