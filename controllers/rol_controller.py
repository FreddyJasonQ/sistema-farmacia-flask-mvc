from flask import request, redirect, url_for, Blueprint, render_template, flash
from models.rol_model import Rol
from models.permiso_model import Permiso
from database import db
from views import rol_view
from utils.decorators import permission_required 

rol_bp = Blueprint('rol', __name__, url_prefix='/roles')

def is_protected_role(rol_name):
    return rol_name in ['Administrador', 'Ventas']

def get_all_permissions():
    """Obtiene todos los permisos disponibles"""
    return Permiso.get_all()

def assign_admin_permissions(rol):
    """Asigna todos los permisos al rol Administrador"""
    if rol.name == 'Administrador':
        # Asignar todos los permisos existentes
        all_permissions = Permiso.query.all()
        rol.permisos = all_permissions
    return rol

def assign_sales_permissions(rol):
    """Asigna permisos específicos al rol Ventas"""
    sales_permissions = [
        "realizar_ventas",
        "anular_ventas",
        "ver_historial_ventas",
        "ver_clientes",
        "ver_productos",
        "generar_reportes_ventas"
    ]
    
    for perm_name in sales_permissions:
        perm = Permiso.get_by_name(perm_name)
        if perm:
            if perm not in rol.permisos:
                rol.permisos.append(perm)
    return rol

@rol_bp.route('/')
@permission_required('ver_roles')  # Permiso para ver roles
def index():
    search_query = request.args.get('search', '')
    roles = Rol.query.filter(Rol.name.ilike(f'%{search_query}%')).all()
    permisos = Permiso.get_all()
    
    return rol_view.list(roles, permisos, search_query)

@rol_bp.route('/create', methods=['GET', 'POST'])
@permission_required('crear_roles')  # Permiso para crear roles
def create():
    permisos = get_all_permissions()
    
    if request.method == 'POST':
        name = request.form['name']
        guard_name = request.form['guard_name'] or 'web'
        selected_perms = request.form.getlist('permisos')
        
        if is_protected_role(name):
            flash('No puedes crear un rol con nombre protegido', 'danger')
            return redirect(url_for('rol.create'))
        
        nuevo_rol = Rol(name=name, guard_name=guard_name)
        db.session.add(nuevo_rol)
        
        # Asignar permisos seleccionados
        for perm_id in selected_perms:
            perm = Permiso.get_by_id(perm_id)
            if perm:
                nuevo_rol.permisos.append(perm)
        
        # Asignación automática para roles especiales
        if name == "Administrador":
            nuevo_rol = assign_admin_permissions(nuevo_rol)
        elif name == "Ventas":
            nuevo_rol = assign_sales_permissions(nuevo_rol)
        
        db.session.commit()
        flash('Rol creado exitosamente', 'success')
        return redirect(url_for('rol.index'))
    
    return rol_view.create(permisos)

@rol_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@permission_required('editar_roles')  # Permiso para editar roles
def edit(id):
    rol = Rol.get_by_id(id)
    if not rol:
        flash('Rol no encontrado', 'danger')
        return redirect(url_for('rol.index'))
    
    if request.method == 'POST' and is_protected_role(rol.name):
        flash('No puedes modificar un rol protegido', 'danger')
        return redirect(url_for('rol.index'))
    
    permisos = get_all_permissions()
    permisos_seleccionados = [p.id for p in rol.permisos]
    
    if request.method == 'POST':
        # No permitir cambiar nombre de roles protegidos
        if not is_protected_role(rol.name):
            rol.name = request.form['name']
        
        rol.guard_name = request.form['guard_name'] or 'web'
        selected_perms = request.form.getlist('permisos')
        
        # Actualizar permisos solo para roles no protegidos
        if not is_protected_role(rol.name):
            rol.permisos = []
            for perm_id in selected_perms:
                perm = Permiso.get_by_id(perm_id)
                if perm:
                    rol.permisos.append(perm)
        else:
            # Actualización automática para roles protegidos
            if rol.name == "Administrador":
                rol = assign_admin_permissions(rol)
            elif rol.name == "Ventas":
                rol = assign_sales_permissions(rol)
        
        db.session.commit()
        flash('Rol actualizado exitosamente', 'success')
        return redirect(url_for('rol.index'))
    
    return rol_view.edit(rol, permisos, permisos_seleccionados)

@rol_bp.route('/delete/<int:id>')
@permission_required('eliminar_roles')  # Permiso para eliminar roles
def delete(id):
    rol = Rol.get_by_id(id)
    if rol:
        if is_protected_role(rol.name):
            flash('No se puede eliminar un rol protegido', 'danger')
        else:
            # Eliminar relaciones primero
            rol.permisos = []
            db.session.delete(rol)
            db.session.commit()
            flash('Rol eliminado exitosamente', 'success')
    return redirect(url_for('rol.index'))