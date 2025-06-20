from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.movimiento_caja_model import MovimientoCaja
from models.caja_model import Caja
from utils.decorators import permission_required  

movimiento_bp = Blueprint('movimiento', __name__, url_prefix='/movimientos')

@movimiento_bp.route('/ingresos', methods=['GET', 'POST'])
@permission_required('registrar_ingresos')  # Permiso para registrar ingresos
def ingresos():
    cajas = Caja.get_abiertas()
    
    if request.method == 'POST':
        caja_id = int(request.form['caja_id'])
        monto = float(request.form['monto'])
        descripcion = request.form['descripcion']
        usuario_id = session.get('user_id')
        
        movimiento = MovimientoCaja(
            caja_id=caja_id,
            tipo='ingreso',
            monto=monto,
            usuario_id=usuario_id,
            descripcion=descripcion
        )
        movimiento.save()
        
        flash('Ingreso registrado exitosamente', 'success')
        return redirect(url_for('movimiento.ingresos'))
    
    ingresos = MovimientoCaja.get_by_tipo('ingreso')
    return render_template('movimientos/ingresos.html', cajas=cajas, ingresos=ingresos)

@movimiento_bp.route('/egresos', methods=['GET', 'POST'])
@permission_required('registrar_egresos')  # Permiso para registrar egresos
def egresos():
    cajas = Caja.get_abiertas()
    
    if request.method == 'POST':
        caja_id = int(request.form['caja_id'])
        monto = float(request.form['monto'])
        descripcion = request.form['descripcion']
        usuario_id = session.get('user_id')
        
        movimiento = MovimientoCaja(
            caja_id=caja_id,
            tipo='egreso',
            monto=monto,
            usuario_id=usuario_id,
            descripcion=descripcion
        )
        movimiento.save()
        
        flash('Egreso registrado exitosamente', 'success')
        return redirect(url_for('movimiento.egresos'))
    
    egresos = MovimientoCaja.get_by_tipo('egreso')
    return render_template('movimientos/egresos.html', cajas=cajas, egresos=egresos)