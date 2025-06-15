# models/venta_detalle_model.py
from database import db
from datetime import datetime

class VentaDetalle(db.Model):
    __tablename__ = "ventas_detalles"
    
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.Numeric(10,2))
    vencimiento = db.Column(db.Date)
    lote = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Relaciones
    producto = db.relationship('Producto', backref='ventas_detalles')

    @property
    def subtotal(self):
        return self.cantidad * self.precio