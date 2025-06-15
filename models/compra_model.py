# models/compra_model.py
from database import db
from datetime import datetime

class Compra(db.Model):
    __tablename__ = "compras"
    
    id = db.Column(db.Integer, primary_key=True)
    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    comprobante_tipo = db.Column(db.String(60))
    comprobante_numero = db.Column(db.String(40))
    subtotal = db.Column(db.Numeric(10,2), default=0.0)
    descuento = db.Column(db.Numeric(10,2), default=0.0)
    total = db.Column(db.Numeric(10,2), default=0.0)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Relaciones
    laboratorio = db.relationship('Laboratorio', backref='compras')
    usuario = db.relationship('Usuario', backref='compras')
    detalles = db.relationship('CompraDetalle', backref='compra', cascade='all, delete-orphan')

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Compra.query.get(id)

    def calcular_totales(self):
        self.subtotal = sum(detalle.subtotal for detalle in self.detalles)
        self.total = self.subtotal - self.descuento