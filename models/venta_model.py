from database import db
from datetime import datetime

class Venta(db.Model):
    __tablename__ = "ventas"
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    total = db.Column(db.Numeric(10,2), default=0.0)
    descuento = db.Column(db.Numeric(10,2), default=0.0)
    total_neto = db.Column(db.Numeric(10,2), default=0.0)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Relaciones
    cliente = db.relationship('Cliente', backref='ventas')
    usuario = db.relationship('Usuario', backref='ventas')
    detalles = db.relationship('VentaDetalle', backref='venta', cascade='all, delete-orphan')

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Venta.query.get(id)

    def calcular_totales(self):
        self.total = sum(detalle.subtotal for detalle in self.detalles)
        self.total_neto = self.total - self.descuento