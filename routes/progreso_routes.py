from flask import Blueprint
from controllers.progreso_controller import obtener_progreso, actualizar_progreso

progreso_bp = Blueprint("progreso_bp", __name__)

# ✅ Obtener progreso por perfil
@progreso_bp.route("/api/progreso/<int:id_perfil>", methods=["GET"])
def get_progreso(id_perfil):
    return obtener_progreso(id_perfil)

# ✅ Actualizar progreso
@progreso_bp.route("/api/progreso/actualizar", methods=["POST"])
def post_progreso():
    return actualizar_progreso()
