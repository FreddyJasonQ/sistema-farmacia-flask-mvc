from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.compra_model import Compra
from models.compra_detalle_model import CompraDetalle
from models.laboratorio_model import Laboratorio
from models.producto_model import Producto
from views import compra_view
from database import db
from datetime import datetime, date  
from flask_login import current_user
from utils.decorators import permission_required
from forms.forms import CompraForm

compra_bp = Blueprint('compra', __name__, url_prefix='/compras')

@compra_bp.route('/')
@permission_required('ver_compras')
def index():
    compras = Compra.query.filter_by(deleted_at=None).all()
    return compra_view.compra_index(compras)

@compra_bp.route('/create', methods=['GET', 'POST'])
@permission_required('crear_compras')
def create():
    laboratorios = Laboratorio.query.filter_by(deleted_at=None).all()
    productos = Producto.query.filter_by(deleted_at=None).all()
    hoy = datetime.now().strftime('%Y-%m-%d')
    
    form = CompraForm()
    form.laboratorio_id.choices = [(lab.id, lab.nombre_lab) for lab in laboratorios]
    form.laboratorio_id.choices.insert(0, ('', 'Seleccione laboratorio'))
    
    if request.method == 'POST':
        # Validar formulario principal
        if not form.validate():
            return render_template('compras/create.html', form=form, productos=productos, hoy=hoy)
        
        # Obtener datos de detalles 
        productos_ids = request.form.getlist('producto_id[]')
        cantidades = request.form.getlist('cantidad[]')
        costos = request.form.getlist('costo[]')
        lotes = request.form.getlist('lote[]')  # Añadido
        vencimientos = request.form.getlist('vencimiento[]')  # Añadido
        
        # Validación mínima de detalles
        if not productos_ids:
            flash('Debe agregar al menos un producto', 'danger')
            return render_template('compras/create.html', form=form, productos=productos, hoy=hoy)
        
        for i, producto_id in enumerate(productos_ids):
            if not producto_id:
                flash(f'Fila {i+1}: Seleccione un producto', 'danger')
                return render_template('compras/create.html', form=form, productos=productos, hoy=hoy)
            
            if not cantidades[i] or int(cantidades[i]) < 1:
                flash(f'Fila {i+1}: Cantidad inválida', 'danger')
                return render_template('compras/create.html', form=form, productos=productos, hoy=hoy)
            
            if not costos[i] or float(costos[i]) <= 0:
                flash(f'Fila {i+1}: Costo inválido', 'danger')
                return render_template('compras/create.html', form=form, productos=productos, hoy=hoy)
            vencimiento_str = vencimientos[i]
            if vencimiento_str:
                try:
                    vencimiento_date = datetime.strptime(vencimiento_str, '%Y-%m-%d').date()
                    if vencimiento_date < date.today():
                        flash(f'La fecha de vencimiento no puede ser en el pasado', 'danger')
                        return render_template('compras/create.html', form=form, productos=productos, hoy=hoy)
                except ValueError:
                    flash(f'Fila {i+1}: Formato de fecha inválido', 'danger')
                    return render_template('compras/create.html', form=form, productos=productos, hoy=hoy)
        
        # Crear compra si todo es válido
        compra = Compra(
            laboratorio_id=form.laboratorio_id.data,
            fecha=form.fecha.data,
            comprobante_tipo=form.comprobante_tipo.data,
            comprobante_numero=form.comprobante_numero.data,
            descuento=form.descuento.data or 0,
            usuario_id=current_user.id
        )
        
        # Procesar detalles
        detalles = []
        for i in range(len(productos_ids)):
            vencimiento_str = vencimientos[i]
            # Manejar fechas 
            vencimiento = datetime.strptime(vencimiento_str, '%Y-%m-%d').date() if vencimiento_str else None
            
            detalle = CompraDetalle(
                producto_id=int(productos_ids[i]),
                cantidad_ingresada=int(cantidades[i]),
                costo=float(costos[i]),
                vencimiento=vencimiento,
                lote=lotes[i]
            )
            detalles.append(detalle)
            
            # Actualizar stock del producto
            producto = Producto.query.get(int(productos_ids[i]))
            if producto:
                producto.cantidad += int(cantidades[i])
                db.session.add(producto)
            else:
                flash(f'Producto con ID {productos_ids[i]} no encontrado', 'danger')
                return redirect(url_for('compra.create'))
        
        compra.detalles = detalles
        compra.calcular_totales()
        db.session.add(compra)
        db.session.commit()
        
        flash('Compra registrada exitosamente', 'success')
        return redirect(url_for('compra.index'))
    
    # En GET, establecer fecha actual
    form.fecha.data = datetime.now().date()  # Corregido
    return render_template('compras/create.html', form=form, laboratorios=laboratorios, productos=productos, hoy=hoy)

@compra_bp.route('/<int:id>')
@permission_required('ver_compras')
def show(id):
    compra = Compra.query.get_or_404(id)
    return compra_view.compra_show(compra)

@compra_bp.route('/delete/<int:id>')
@permission_required('anular_compras')
def delete(id):
    compra = Compra.query.get_or_404(id)
    
    # Verificar si la compra ya está anulada
    if compra.deleted_at:
        flash('Esta compra ya fue anulada anteriormente', 'warning')
        return redirect(url_for('compra.index'))
    
    compra.deleted_at = datetime.utcnow()
    
    # Revertir stock solo si los productos aún existen
    for detalle in compra.detalles:
        producto = Producto.query.get(detalle.producto_id)
        if producto:
            producto.cantidad -= detalle.cantidad_ingresada
            # Asegurar que el stock no sea negativo
            if producto.cantidad < 0:
                producto.cantidad = 0
            db.session.add(producto)
        else:
            # Si el producto ya no existe, solo registrar un mensaje
            flash(f'El producto con ID {detalle.producto_id} ya no existe. No se pudo revertir el stock', 'warning')
    
    db.session.commit()
    flash('Compra anulada exitosamente', 'success')
    return redirect(url_for('compra.index'))