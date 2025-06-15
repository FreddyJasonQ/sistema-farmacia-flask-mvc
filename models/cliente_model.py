from database import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = "clientes"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    tipo_documento = db.Column(db.String(20))
    documento = db.Column(db.String(20))
    complemento = db.Column(db.String(10))
    telefono = db.Column(db.String(15))
    estado = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Cliente.query.filter_by(deleted_at=None).all()
    
    @staticmethod
    def get_by_id(id):
        return Cliente.query.get(id)
    
    @staticmethod
    def search(query):
        return Cliente.query.filter(
            (Cliente.nombre.ilike(f'%{query}%')) |
            (Cliente.documento.ilike(f'%{query}%'))
        ).filter_by(deleted_at=None).all()
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        
    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()