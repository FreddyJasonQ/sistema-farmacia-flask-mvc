from flask import render_template

def list(roles, permisos, search_query):
    return render_template('roles/index.html', roles=roles, permisos=permisos, search_query=search_query)

def create(permisos):
    # Crear un rol vacío para evitar errores en la plantilla
    rol = None
    return render_template('roles/create.html', permisos=permisos, rol=rol)

def edit(rol, permisos, permisos_seleccionados):
    return render_template('roles/edit.html', rol=rol, permisos=permisos, permisos_seleccionados=permisos_seleccionados)