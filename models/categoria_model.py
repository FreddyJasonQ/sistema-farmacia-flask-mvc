from database import db
from datetime import datetime

class Categoria(db.Model):
    __tablename__ = "categorias"
    
    id = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    estado = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    def __init__(self, categoria, descripcion=None, estado=True):
        self.categoria = categoria
        self.descripcion = descripcion
        self.estado = estado
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod    
    def get_all():  
        return Categoria.query.filter_by(deleted_at=None).all()
    
    @staticmethod
    def get_by_id(id):
        return Categoria.query.get(id)
    
    @staticmethod
    def search(query):
        return Categoria.query.filter(
            (Categoria.categoria.ilike(f'%{query}%')) |
            (Categoria.descripcion.ilike(f'%{query}%'))
        ).filter_by(deleted_at=None).all()
            
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        
    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()