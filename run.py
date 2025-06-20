from flask import Flask, render_template, request
from database import db, init_app  
from flask_login import LoginManager
from models.usuario_model import Usuario
from controllers import compra_controller
from controllers import categoria_controller
from controllers import presentacion_controller
from controllers import producto_controller
from controllers import venta_controller
from controllers import cliente_controller
from controllers import caja_controller
from controllers import movimiento_controller
from controllers import reporte_controller
from controllers import dashboard_controller
from controllers import auth_controller
from controllers import usuario_controller
from controllers import rol_controller
from controllers import laboratorio_controller

app = Flask(__name__)

# Configuración de la aplicación
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ventas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clave_secreta_para_flash_messages"

# Inicializar la base de datos
# Inicializar extensiones
init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# Registrar Blueprints
app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(rol_controller.rol_bp)
app.register_blueprint(laboratorio_controller.laboratorio_bp)
app.register_blueprint(compra_controller.compra_bp)
app.register_blueprint(categoria_controller.categoria_bp)
app.register_blueprint(presentacion_controller.presentacion_bp)
app.register_blueprint(producto_controller.producto_bp)
app.register_blueprint(venta_controller.venta_bp)
app.register_blueprint(cliente_controller.cliente_bp)
app.register_blueprint(caja_controller.caja_bp)
app.register_blueprint(movimiento_controller.movimiento_bp)
app.register_blueprint(reporte_controller.reporte_bp)
app.register_blueprint(dashboard_controller.dashboard_bp)
app.register_blueprint(auth_controller.auth_bp)

@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path.startswith(path) else ''
    return dict(is_active=is_active)


if __name__ == "__main__":
    app.run(debug=True)