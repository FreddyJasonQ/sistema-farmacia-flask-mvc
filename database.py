from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        from models.permiso_model import Permiso
        Permiso.create_base_permissions()
        Permiso.initialize_system_permissions()