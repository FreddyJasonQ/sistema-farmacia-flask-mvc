from database import db
from datetime import datetime

class MovimientoCaja(db.Model):
    __tablename__ = "cajas_movimientos"
    
    TIPOS = ['ingreso', 'egreso']
    
    id = db.Column(db.Integer, primary_key=True)
    caja_id = db.Column(db.Integer, db.ForeignKey('cajas.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    tipo = db.Column(db.String(20), nullable=False)
    monto = db.Column(db.DECIMAL(10, 2), nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow().date())
    descripcion = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    usuario = db.relationship('Usuario')

    def __init__(self, caja_id, tipo, monto, usuario_id, descripcion=""):
        self.caja_id = caja_id
        self.tipo = tipo
        self.monto = monto
        self.usuario_id = usuario_id
        self.descripcion = descripcion

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_by_tipo(tipo):
        return MovimientoCaja.query.filter_by(tipo=tipo, deleted_at=None).all()
    
    @staticmethod
    def get_by_caja(caja_id):
        return MovimientoCaja.query.filter_by(caja_id=caja_id, deleted_at=None).all()