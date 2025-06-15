from flask import render_template

def index(laboratorios, search_query):
    return render_template('laboratorios/index.html', laboratorios=laboratorios, search_query=search_query)

def create():
    return render_template('laboratorios/create.html')

def edit(laboratorio):
    return render_template('laboratorios/edit.html', laboratorio=laboratorio)