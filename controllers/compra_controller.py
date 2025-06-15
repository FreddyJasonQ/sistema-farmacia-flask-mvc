from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.compra_model import Compra
from models.compra_detalle_model import CompraDetalle
from models.laboratorio_model import Laboratorio
from models.producto_model import Producto
from views import compra_view
from database import db
from datetime import datetime

compra_bp = Blueprint('compra', __name__, url_prefix='/compras')

@compra_bp.route('/')
def index():
    compras = Compra.query.filter_by(deleted_at=None).all()
    return compra_view.compra_index(compras)

@compra_bp.route('/create', methods=['GET', 'POST'])
def create():
    laboratorios = Laboratorio.query.filter_by(deleted_at=None).all()
    productos = Producto.query.filter_by(deleted_at=None).all()
    hoy = datetime.now().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        # Crear compra principal
        compra = Compra(
            laboratorio_id=request.form['laboratorio_id'],
            fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d'),
            comprobante_tipo=request.form['comprobante_tipo'],
            comprobante_numero=request.form['comprobante_numero'],
            descuento=float(request.form.get('descuento', 0)),
            usuario_id=1  # Obtener de sesión
        )
        
        # Procesar detalles
        detalles = []
        for i in range(len(request.form.getlist('producto_id[]'))):
            detalle = CompraDetalle(
                producto_id=request.form.getlist('producto_id[]')[i],
                cantidad_ingresada=int(request.form.getlist('cantidad[]')[i]),
                costo=float(request.form.getlist('costo[]')[i]),
                vencimiento=datetime.strptime(request.form.getlist('vencimiento[]')[i], '%Y-%m-%d') if request.form.getlist('vencimiento[]')[i] else None,
                lote=request.form.getlist('lote[]')[i]
            )
            detalles.append(detalle)
            
            # Actualizar stock del producto
            producto = Producto.query.get(detalle.producto_id)
            producto.cantidad += detalle.cantidad_ingresada
            db.session.add(producto)
        
        compra.detalles = detalles
        compra.calcular_totales()
        compra.save()
        
        flash('Compra registrada exitosamente', 'success')
        return redirect(url_for('compra.index'))
    
    return compra_view.compra_create(laboratorios, productos, hoy)

@compra_bp.route('/<int:id>')
def show(id):
    compra = Compra.query.get_or_404(id)
    return compra_view.compra_show(compra)

@compra_bp.route('/delete/<int:id>')
def delete(id):
    compra = Compra.query.get_or_404(id)
    compra.deleted_at = datetime.utcnow()
    
    # Revertir stock
    for detalle in compra.detalles:
        producto = Producto.query.get(detalle.producto_id)
        producto.cantidad -= detalle.cantidad_ingresada
        db.session.add(producto)
    
    db.session.commit()
    flash('Compra anulada exitosamente', 'success')
    return redirect(url_for('compra.index'))