from flask import Blueprint
from controllers.perfil_controller import (
    obtener_perfil,
    editar_perfil,
    agregar_monedas,
    actualizar_saldo,
    eliminar_perfil
)

perfil_bp = Blueprint("perfil_bp", __name__)

# ✅ Obtener perfil
@perfil_bp.route("/api/perfil/<int:id_usuario>", methods=["GET"])
def get_perfil(id_usuario):
    return obtener_perfil(id_usuario)

# ✅ Editar perfil (nombre o correo)
@perfil_bp.route("/api/perfil/editar/<int:id_usuario>", methods=["PUT"])
def edit_perfil(id_usuario):
    return editar_perfil(id_usuario)

# ✅ Agregar monedas
@perfil_bp.route("/api/monedas/agregar", methods=["POST"])
def add_coins():
    return agregar_monedas()

# ✅ Actualizar saldo
@perfil_bp.route("/api/saldo/actualizar", methods=["POST"])
def update_balance():
    return actualizar_saldo()

# ✅ Eliminar perfil
@perfil_bp.route("/api/perfil/<int:id_usuario>", methods=["DELETE"])
def delete_perfil(id_usuario):
    return eliminar_perfil(id_usuario)
