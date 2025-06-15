from flask import render_template

def index(productos, search_query):
    return render_template('productos/index.html', productos=productos, search_query=search_query)

def create(categorias, laboratorios, presentaciones):
    return render_template('productos/create.html', 
                          categorias=categorias, 
                          laboratorios=laboratorios, 
                          presentaciones=presentaciones)

def edit(producto, categorias, laboratorios, presentaciones):
    return render_template('productos/edit.html', 
                          producto=producto,
                          categorias=categorias, 
                          laboratorios=laboratorios, 
                          presentaciones=presentaciones)