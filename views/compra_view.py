from flask import render_template

def compra_index(compras):
    return render_template('compras/index.html', compras=compras)

def compra_create(laboratorios, productos, hoy):
    return render_template('compras/create.html', 
                          laboratorios=laboratorios, 
                          productos=productos,
                          hoy=hoy)

def compra_show(compra):
    return render_template('compras/detalle.html', compra=compra)