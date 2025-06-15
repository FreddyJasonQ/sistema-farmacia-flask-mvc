from flask import render_template

def index(clientes, search_query):
    return render_template('clientes/index.html', clientes=clientes, search_query=search_query)

def create():
    return render_template('clientes/create.html')

def edit(cliente):
    return render_template('clientes/edit.html', cliente=cliente)