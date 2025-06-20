from flask import render_template

def venta_index(ventas):
    return render_template('ventas/index.html', ventas=ventas)

def venta_create(clientes, productos, hoy):
    return render_template('ventas/create.html', 
                          clientes=clientes, 
                          productos=productos,
                          hoy=hoy)

def venta_show(venta):
    return render_template('ventas/detalle.html', venta=venta)