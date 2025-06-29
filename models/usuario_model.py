from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models.rol_model import Rol

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    imagen = db.Column(db.String(255), nullable=True)
    nombres = db.Column(db.String(255), nullable=False)
    apellidos = db.Column(db.String(150), nullable=False)
    carnet = db.Column(db.String(15), nullable=False)
    nacimiento = db.Column(db.Date, nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    usuario = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    remember_token = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    rol = db.relationship('Rol', backref='usuarios')

    def __init__(self, nombres, apellidos, carnet, nacimiento, telefono, 
                 email, usuario, password, rol_id, imagen=None):
        self.nombres = nombres
        self.apellidos = apellidos
        self.carnet = carnet
        self.nacimiento = nacimiento
        self.telefono = telefono
        self.email = email
        self.usuario = usuario
        self.password = self.hash_password(password)
        self.rol_id = rol_id
        self.imagen = imagen
        
    @staticmethod        
    def hash_password(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod    
    def get_all():  
        return Usuario.query.filter_by(deleted_at=None).all()
    
    @staticmethod
    def get_by_id(id):
        return Usuario.query.get(id)
    
    @staticmethod
    def search(query):
        return Usuario.query.filter(
            (Usuario.nombres.ilike(f'%{query}%')) |
            (Usuario.apellidos.ilike(f'%{query}%')) |
            (Usuario.email.ilike(f'%{query}%')) |
            (Usuario.usuario.ilike(f'%{query}%')) |
            (Usuario.rol.has(Rol.name.ilike(f'%{query}%')))  
        ).filter_by(deleted_at=None).all()
            
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'password' and value:  # Solo si hay nueva contraseña
                setattr(self, key, self.hash_password(value))
            elif key == 'nacimiento' and isinstance(value, str):  # Convertir si es string
                setattr(self, key, datetime.strptime(value, '%Y-%m-%d').date())
            else:
                setattr(self, key, value)
        db.session.commit()
        
    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()
        
    # Métodos Flask-Login
    def get_id(self):
        return str(self.id)
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    # Métodos de contraseña
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_rol(self):
        return self.rol.name if self.rol else None

    def has_permission(self, permission_name):
        """Verifica si el usuario tiene un permiso específico"""
        # Administrador tiene todos los permisos
        if self.rol and self.rol.name == 'Administrador':
            return True
            
        # Buscar permiso en el rol
        if self.rol:
            for permiso in self.rol.permisos:
                if permiso.name == permission_name:
                    return True
        return False
    
    def is_admin(self):
        """Verifica si el usuario tiene rol de Administrador"""
        return self.rol and self.rol.name == 'Administrador'
    
    def has_permission(self, permission_name):
        """Verifica si el usuario tiene un permiso específico"""
        # Administradores tienen todos los permisos
        if self.is_admin():
            return True
            
        # Para otros roles, verificar permisos asignados
        if self.rol:
            return any(perm.name == permission_name for perm in self.rol.permisos)
        return False