from database import db
from datetime import datetime

class Caja(db.Model):
    __tablename__ = "cajas"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    fecha_apertura = db.Column(db.Date, default=datetime.utcnow)
    fecha_cierre = db.Column(db.Date)
    monto_apertura = db.Column(db.DECIMAL(10, 2), default=0.0)
    monto_cierre = db.Column(db.DECIMAL(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    usuario = db.relationship('Usuario')
    movimientos = db.relationship('MovimientoCaja', backref='caja')

    def __init__(self, usuario_id, descripcion, monto_apertura=0.0):
        self.usuario_id = usuario_id
        self.descripcion = descripcion
        self.monto_apertura = monto_apertura

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def cerrar(self, monto_cierre):
        self.fecha_cierre = datetime.utcnow().date()
        self.monto_cierre = monto_cierre
        db.session.commit()

    @staticmethod
    def get_all():
        return Caja.query.filter_by(deleted_at=None).all()
    
    @staticmethod
    def get_abiertas():
        return Caja.query.filter_by(fecha_cierre=None, deleted_at=None).all()
    
    @staticmethod
    def get_by_id(id):
        return Caja.query.get(id)
    
    def calcular_total(self):
        total = 0.0
        for movimiento in self.movimientos:
            monto = float(movimiento.monto or 0)
            if movimiento.tipo == 'ingreso':
                total += monto
            elif movimiento.tipo == 'egreso':
                total -= monto
        return total

    def calcular_ganancia(self):
        return self.calcular_total() - float(self.monto_apertura or 0)
