from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func
from models.caja_model import Caja
from models.movimiento_caja_model import MovimientoCaja
from flask_login import current_user  # Importar current_user para autenticación
from utils.decorators import permission_required
from forms.forms import CajaForm

caja_bp = Blueprint('caja', __name__, url_prefix='/cajas')

@caja_bp.route('/')
@permission_required('ver_cajas')  # Permiso para ver cajas
def index():
    cajas = Caja.get_all()
    return render_template('cajas/index.html', cajas=cajas)

@caja_bp.route('/create', methods=['GET', 'POST'])
@permission_required('crear_cajas')
def create():
    form = CajaForm()  # Crear instancia del formulario
    
    if form.validate_on_submit():  # Validar en POST
        descripcion = form.descripcion.data
        monto_apertura = form.monto_apertura.data

        nueva_caja = Caja(
            usuario_id=current_user.id,
            descripcion=descripcion,
            monto_apertura=monto_apertura
        )
        nueva_caja.save()
        
        if monto_apertura > 0:
            movimiento = MovimientoCaja(
                caja_id=nueva_caja.id,
                tipo='ingreso',
                monto=monto_apertura,
                usuario_id=current_user.id,
                descripcion='Apertura de caja'
            )
            movimiento.save()
        
        flash('Caja creada exitosamente', 'success')
        return redirect(url_for('caja.index'))
    
    
    return render_template('cajas/create.html', form=form)

@caja_bp.route('/<int:id>/close', methods=['GET', 'POST'])
@permission_required('cerrar_cajas')  # Permiso específico para cerrar cajas
def close(id):
    caja = Caja.get_by_id(id)
    
    if not caja:
        flash('Caja no encontrada', 'danger')
        return redirect(url_for('caja.index'))
    
    if caja.estado == 'cerrada':
        flash('Esta caja ya está cerrada', 'warning')
        return redirect(url_for('caja.index'))
    
    if request.method == 'POST':
        monto_cierre = float(request.form['monto_cierre'])
        
        # Validar monto de cierre
        if monto_cierre < 0:
            flash('El monto de cierre no puede ser negativo', 'danger')
            return render_template('cajas/close.html', caja=caja, total_teorico=caja.calcular_total())
        
        # Registrar movimiento de cierre
        movimiento_cierre = MovimientoCaja(
            caja_id=caja.id,
            tipo='egreso',
            monto=caja.calcular_total(),
            usuario_id=current_user.id,
            descripcion='Cierre de caja'
        )
        movimiento_cierre.save()
        
        # Cerrar la caja
        caja.cerrar(monto_cierre, current_user.id)
        
        flash('Caja cerrada exitosamente', 'success')
        return redirect(url_for('caja.index'))
    
    total_teorico = caja.calcular_total()
    return render_template('cajas/close.html', caja=caja, total_teorico=total_teorico)

@caja_bp.route('/<int:id>')
@permission_required('ver_cajas')  
def detail(id):
    caja = Caja.get_by_id(id)
    if not caja:
        flash('Caja no encontrada', 'danger')
        return redirect(url_for('caja.index'))
    
    movimientos = MovimientoCaja.get_by_caja(id)
    
    # Cálculos 
    total_ingresos = MovimientoCaja.query.with_entities(
        func.coalesce(func.sum(MovimientoCaja.monto), 0.0)
    ).filter_by(
        caja_id=id,
        tipo='ingreso'
    ).scalar()

    total_egresos = MovimientoCaja.query.with_entities(
        func.coalesce(func.sum(MovimientoCaja.monto), 0.0)
    ).filter_by(
        caja_id=id,
        tipo='egreso'
    ).scalar()

    return render_template(
        'cajas/detail.html',
        caja=caja,
        movimientos=movimientos,
        total_ingresos=total_ingresos,
        total_egresos=total_egresos
    )