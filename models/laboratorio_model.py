from database import db
from datetime import datetime

class Laboratorio(db.Model):
    __tablename__ = "laboratorios"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_lab = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(200))
    responsable = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    def __init__(self, nombre_lab, direccion=None, responsable=None, telefono=None):
        self.nombre_lab = nombre_lab
        self.direccion = direccion
        self.responsable = responsable
        self.telefono = telefono
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod    
    def get_all():  
        return Laboratorio.query.filter_by(deleted_at=None).all()
    
    @staticmethod
    def get_by_id(id):
        return Laboratorio.query.get(id)
    
    @staticmethod
    def search(query):
        return Laboratorio.query.filter(
            (Laboratorio.nombre_lab.ilike(f'%{query}%')) |
            (Laboratorio.responsable.ilike(f'%{query}%')) |
            (Laboratorio.telefono.ilike(f'%{query}%'))
        ).filter_by(deleted_at=None).all()
            
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        
    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()