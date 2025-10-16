from flask import Blueprint
from controllers.usuarios_controller import update_usuario

usuarios_bp = Blueprint("usuarios", __name__)
usuarios_bp.route("/<int:id_usuario>", methods=["PUT"])(update_usuario)
