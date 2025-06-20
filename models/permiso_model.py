from database import db
from datetime import datetime

class Permiso(db.Model):
    __tablename__ = "permissions"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(255))  # Añade este campo
    guard_name = db.Column(db.String(255), default='web')
    protected = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Actualiza el constructor para incluir description
    def __init__(self, name, description=None, guard_name='web', protected=False):
        self.name = name
        self.description = description
        self.guard_name = guard_name
        self.protected = protected
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod    
    def get_all():  
        return Permiso.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Permiso.query.get(id)
    
    @staticmethod
    def get_by_name(name):
        return Permiso.query.filter_by(name=name).first()
    
    @staticmethod
    def create_base_permissions():
        base_permissions = [
            ("Administrador", "Acceso completo al sistema", True),
            ("Ventas", "Permisos para operaciones de venta", True)
        ]
        
        for name, description, protected in base_permissions:
            if not Permiso.get_by_name(name):
                perm = Permiso(name=name, description=description, protected=protected)
                db.session.add(perm)
        db.session.commit()

    @staticmethod
    def initialize_system_permissions():
        system_permissions = [
            ("ver_usuarios", "Ver listado de usuarios"),
            ("crear_usuarios", "Crear nuevos usuarios"),
            ("editar_usuarios", "Editar usuarios existentes"),
            ("eliminar_usuarios", "Eliminar usuarios"),
            
            ("realizar_ventas", "Registrar nuevas ventas"),
            ("anular_ventas", "Anular ventas registradas"),
            ("ver_historial_ventas", "Ver historial de ventas"),
            
            ("ver_productos", "Ver listado de productos"),
            ("crear_productos", "Crear nuevos productos"),
            ("editar_productos", "Editar productos existentes"),
            ("eliminar_productos", "Eliminar productos"),
            
            ("ver_presentaciones", "Ver listado de presentaciones"),
            ("crear_presentaciones", "Crear nuevas presentaciones"),
            ("editar_presentaciones", "Editar presentaciones existentes"),
            ("eliminar_presentaciones", "Eliminar presentaciones"),
            
            ("registrar_ingresos", "Registrar ingresos de caja"),
            ("registrar_egresos", "Registrar egresos de caja"),
            ("ver_ingresos", "Ver historial de ingresos"),
            ("ver_egresos", "Ver historial de egresos"),
            
            ("ver_laboratorios", "Ver listado de laboratorios"),
            ("crear_laboratorios", "Crear nuevos laboratorios"),
            ("editar_laboratorios", "Editar laboratorios existentes"),
            ("eliminar_laboratorios", "Eliminar laboratorios"),
            
            ("ver_compras", "Ver historial de compras"),
            ("crear_compras", "Registrar nuevas compras"),
            ("anular_compras", "Anular compras registradas"),
            
            ("ver_cajas", "Ver listado de cajas y detalles"),
            ("crear_cajas", "Abrir nuevas cajas"),
            ("cerrar_cajas", "Cerrar cajas abiertas"),
            ("registrar_ingresos", "Registrar ingresos de caja"),
            ("registrar_egresos", "Registrar egresos de caja"),
            
            ("ver_clientes", "Ver listado de clientes"),
            ("crear_clientes", "Crear nuevos clientes"),
            ("editar_clientes", "Editar clientes existentes"),
            ("eliminar_clientes", "Eliminar clientes"),
            
            ("ver_categorias", "Ver listado de categorías"),
            ("crear_categorias", "Crear nuevas categorías"),
            ("editar_categorias", "Editar categorías existentes"),
            ("eliminar_categorias", "Eliminar categorías"),
            
            ("ver_reportes_ventas", "ver reportes de ventas")
        ]
        
        for name, description in system_permissions:
            if not Permiso.get_by_name(name):
                perm = Permiso(name=name, description=description)
                db.session.add(perm)
        db.session.commit()