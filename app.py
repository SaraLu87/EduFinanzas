from flask import Flask, jsonify
from flask_cors import CORS
from routes.auth_routes import auth_bp  # 👈 importa tu blueprint
from routes.perfil_routes import perfil_bp
from routes.tema_routes import tema_bp
from routes.reto_routes import reto_bp
from routes.progreso_routes import progreso_bp
from routes.tips_routes import tips_bp

app = Flask(__name__)
CORS(app)

# ✅ Registrar el blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(tema_bp)
app.register_blueprint(reto_bp)
app.register_blueprint(progreso_bp)
app.register_blueprint(tips_bp)

# ✅ Ruta base de prueba
@app.route("/api/test", methods=["GET"])
def test_server():
    return jsonify({"message": "Servidor Flask activo 🚀"})

if __name__ == "__main__":
    app.run(port=3001, debug=True)
