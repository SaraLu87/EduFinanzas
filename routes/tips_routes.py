from flask import Blueprint
from controllers.tips_controller import obtener_tips, crear_tip

tips_bp = Blueprint("tips_bp", __name__)

# ✅ Obtener tips por perfil
@tips_bp.route("/api/tips/<int:id_perfil>", methods=["GET"])
def get_tips(id_perfil):
    return obtener_tips(id_perfil)

# ✅ Crear un nuevo tip
@tips_bp.route("/api/tips", methods=["POST"])
def post_tip():
    return crear_tip()
