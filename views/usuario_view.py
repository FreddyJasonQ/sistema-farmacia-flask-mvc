from flask import render_template

def list(usuarios, search_query):
    return render_template('usuarios/index.html', usuarios=usuarios, search_query=search_query)

def create(roles, form):
    return render_template('usuarios/create.html', roles=roles, form=form)

def edit(usuario, roles, form):
    return render_template('usuarios/edit.html', usuario=usuario, roles=roles, form=form)