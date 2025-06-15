from flask import render_template

def list(usuarios, search_query):
    return render_template('usuarios/index.html', usuarios=usuarios, search_query=search_query)

# Para la función create
def create(roles):
    # Crear un usuario vacío para evitar errores en la plantilla
    usuario = None
    return render_template('usuarios/create.html', roles=roles, usuario=usuario)

# Para la función edit
def edit(usuario, roles):  # Aceptar usuario y roles
    return render_template('usuarios/edit.html', usuario=usuario, roles=roles)