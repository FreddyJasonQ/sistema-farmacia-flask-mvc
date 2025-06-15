# models/compra_detalle_model.py
from database import db
from datetime import datetime

class CompraDetalle(db.Model):
    __tablename__ = "compras_detalles"
    
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    cantidad_ingresada = db.Column(db.Integer)
    costo = db.Column(db.Numeric(10,2))
    vencimiento = db.Column(db.Date)
    lote = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Relaciones
    producto = db.relationship('Producto', backref='compras_detalles')

    @property
    def subtotal(self):
        return self.cantidad_ingresada * self.costo