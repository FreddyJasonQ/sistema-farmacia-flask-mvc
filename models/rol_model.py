from database import db
from datetime import datetime

# Tabla de relación entre roles y permisos
role_has_permissions = db.Table(
    'role_has_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)

class Rol(db.Model):
    __tablename__ = "roles"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    guard_name = db.Column(db.String(255), default='web')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    permisos = db.relationship(
        'Permiso', 
        secondary=role_has_permissions, 
        backref=db.backref('roles', lazy='dynamic')
    )

    def __init__(self, name, guard_name='web'):
        self.name = name
        self.guard_name = guard_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def tiene_permiso(self, permiso_name):
        if "Administrador" in [p.name for p in self.permisos]:
            return True
        return permiso_name in [p.name for p in self.permisos]
    
    @staticmethod
    def get_all():
        return Rol.query.all()

    @staticmethod
    def get_by_id(id):
        return Rol.query.get(id)
    
    @staticmethod
    def search(query):
        return Rol.query.filter(Rol.name.ilike(f'%{query}%')).all()