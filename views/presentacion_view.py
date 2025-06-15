from flask import render_template

def index(presentaciones, search_query):
    return render_template('presentaciones/index.html', presentaciones=presentaciones, search_query=search_query)

def create():
    return render_template('presentaciones/create.html')

def edit(presentacion):
    return render_template('presentaciones/edit.html', presentacion=presentacion)