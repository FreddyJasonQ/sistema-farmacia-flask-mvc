from flask import Flask, render_template, redirect, url_for, request
from database import db, init_app  # Importamos db e init_app
from controllers import compra_controller
from models.producto_model import Producto
from controllers import categoria_controller
from controllers import presentacion_controller
from controllers import producto_controller
from controllers import venta_controller
from controllers import (
    usuario_controller, 
    rol_controller,
    laboratorio_controller,
    producto_controller,

)

app = Flask(__name__)

# Configuración de la aplicación
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ventas.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clave_secreta_para_flash_messages"

# Inicializar la base de datos
init_app(app)  # Usamos la función init_app para configurar db con la app

# Registrar Blueprints
app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(rol_controller.rol_bp)
app.register_blueprint(laboratorio_controller.laboratorio_bp)
app.register_blueprint(compra_controller.compra_bp)
app.register_blueprint(categoria_controller.categoria_bp)
app.register_blueprint(presentacion_controller.presentacion_bp)
app.register_blueprint(producto_controller.producto_bp)
app.register_blueprint(venta_controller.venta_bp)


@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path.startswith(path) else ''
    return dict(is_active=is_active)

@app.route('/')
def home():
    return render_template('dashboard/index.html')

# Manejo de errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run(debug=True)