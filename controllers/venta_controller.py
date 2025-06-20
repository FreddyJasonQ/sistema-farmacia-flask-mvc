from flask import Blueprint, request, redirect, url_for, flash
from models.venta_model import Venta
from models.venta_detalle_model import VentaDetalle
from models.cliente_model import Cliente
from models.producto_model import Producto
from models.usuario_model import Usuario
from views import venta_view
from database import db
from datetime import datetime
from utils.decorators import permission_required 
from flask_login import current_user 

venta_bp = Blueprint('venta', __name__, url_prefix='/ventas')

@venta_bp.route('/')
@permission_required('ver_historial_ventas')  # Permiso para ver historial
def index():
    ventas = Venta.query.filter_by(deleted_at=None).all()
    return venta_view.venta_index(ventas)

@venta_bp.route('/create', methods=['GET', 'POST'])
@permission_required('realizar_ventas')
def create():
    clientes = Cliente.query.filter_by(deleted_at=None).all()
    productos = Producto.query.filter_by(deleted_at=None, estado=True).all()
    hoy = datetime.now().strftime('%Y-%m-%d')
    
    if request.method == 'POST':
        # Asigna automáticamente el ID del usuario autenticado
        venta = Venta(
            cliente_id=request.form['cliente_id'],
            descuento=float(request.form.get('descuento', 0)),
            descripcion=request.form.get('descripcion', ''),
            fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d'),
            usuario_id=current_user.id  # Usa el usuario actual
        )
        
        # Procesar detalles
        detalles = []
        for i in range(len(request.form.getlist('producto_id[]'))):
            detalle = VentaDetalle(
                producto_id=request.form.getlist('producto_id[]')[i],
                cantidad=int(request.form.getlist('cantidad[]')[i]),
                precio=float(request.form.getlist('precio[]')[i]),
                lote=request.form.getlist('lote[]')[i],
                vencimiento=datetime.strptime(request.form.getlist('vencimiento[]')[i], '%Y-%m-%d') if request.form.getlist('vencimiento[]')[i] else None
            )
            detalles.append(detalle)
            
            # Actualizar stock del producto
            producto = Producto.query.get(detalle.producto_id)
            producto.cantidad -= detalle.cantidad
            if producto.cantidad < 0:
                flash(f'No hay suficiente stock para {producto.nombre_comercial}', 'danger')
                return redirect(url_for('venta.create'))
            db.session.add(producto)
        
        venta.detalles = detalles
        venta.calcular_totales()
        venta.save()
        
        flash('Venta registrada exitosamente', 'success')
        return redirect(url_for('venta.index'))
    
    return venta_view.venta_create(clientes, productos, hoy)

@venta_bp.route('/<int:id>')
@permission_required('ver_historial_ventas')  
def show(id):
    venta = Venta.query.get_or_404(id)
    return venta_view.venta_show(venta)

@venta_bp.route('/delete/<int:id>')
@permission_required('anular_ventas')  # Permiso específico para anular ventas
def delete(id):
    venta = Venta.query.get_or_404(id)
    venta.deleted_at = datetime.utcnow()
    
    # Revertir stock
    for detalle in venta.detalles:
        producto = Producto.query.get(detalle.producto_id)
        producto.cantidad += detalle.cantidad
        db.session.add(producto)
    
    db.session.commit()
    flash('Venta anulada exitosamente', 'success')
    return redirect(url_for('venta.index'))