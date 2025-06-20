from flask import render_template

# Vistas para Caja
def index(cajas):
    return render_template('cajas/index.html', cajas=cajas)

def create():
    return render_template('cajas/create.html')

def close(caja, total_teorico):
    return render_template('cajas/close.html', caja=caja, total_teorico=total_teorico)

def detail(caja, movimientos):
    # Calcular total de egresos para la vista de detalle
    total_egresos = sum(m.monto for m in movimientos if m.tipo == 'egreso')
    return render_template('cajas/detail.html', caja=caja, movimientos=movimientos, total_egresos=total_egresos)

# Vistas para Movimientos de Caja
def ingresos(cajas, ingresos):
    return render_template('movimientos/ingresos.html', cajas=cajas, ingresos=ingresos)

def egresos(cajas, egresos):
    return render_template('movimientos/egresos.html', cajas=cajas, egresos=egresos)