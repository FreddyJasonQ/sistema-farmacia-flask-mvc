from database import db
from datetime import datetime

class Producto(db.Model):
    __tablename__ = "productos"
    
    id = db.Column(db.Integer, primary_key=True)
    imagen = db.Column(db.String(200))
    codigo = db.Column(db.String(100))
    barcode = db.Column(db.String(200))
    nombre_comercial = db.Column(db.String(200), nullable=False)
    nombre_generico = db.Column(db.String(200))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    laboratorio_id = db.Column(db.Integer, db.ForeignKey('laboratorios.id'))
    presentacion_id = db.Column(db.Integer, db.ForeignKey('presentaciones.id'))
    descripcion = db.Column(db.String(200))
    precio_compra = db.Column(db.Numeric(10,2))
    precio_venta = db.Column(db.Numeric(10,2))
    cantidad = db.Column(db.Integer, default=0)
    estado = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime)

    # Relaciones
    categoria = db.relationship('Categoria', backref='productos')
    laboratorio = db.relationship('Laboratorio', backref='productos')
    presentacion = db.relationship('Presentacion', backref='productos')

    def __init__(self, nombre_comercial, categoria_id, laboratorio_id, presentacion_id, 
                 nombre_generico=None, descripcion=None, precio_compra=0, precio_venta=0, 
                 cantidad=0, estado=True, codigo=None, barcode=None, imagen=None):
        self.nombre_comercial = nombre_comercial
        self.categoria_id = categoria_id
        self.laboratorio_id = laboratorio_id
        self.presentacion_id = presentacion_id
        self.nombre_generico = nombre_generico
        self.descripcion = descripcion
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.cantidad = cantidad
        self.estado = estado
        self.codigo = codigo
        self.barcode = barcode
        self.imagen = imagen
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod    
    def get_all():  
        return Producto.query.filter_by(deleted_at=None).all()
    
    @staticmethod
    def get_by_id(id):
        return Producto.query.get(id)
    
    @staticmethod
    def search(query):
        return Producto.query.filter(
            (Producto.nombre_comercial.ilike(f'%{query}%')) |
            (Producto.nombre_generico.ilike(f'%{query}%')) |
            (Producto.codigo.ilike(f'%{query}%')) |
            (Producto.barcode.ilike(f'%{query}%'))
        ).filter_by(deleted_at=None).all()
            
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
        
    def delete(self):
        self.deleted_at = datetime.utcnow()
        db.session.commit()