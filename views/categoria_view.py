from flask import render_template

def index(categorias, search_query):
    return render_template('categorias/index.html', categorias=categorias, search_query=search_query)

def create():
    return render_template('categorias/create.html')

def edit(categoria):
    return render_template('categorias/edit.html', categoria=categoria)