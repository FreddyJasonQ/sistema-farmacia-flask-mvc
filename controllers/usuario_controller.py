from flask import request, redirect, url_for, Blueprint
from models.usuario_model import Usuario
from werkzeug.security import generate_password_hash
from utils.decorators import permission_required  
from flask_login import login_required, current_user
from views import usuario_view
from datetime import datetime
from models.rol_model import Rol
from forms.forms import UsuarioCreateForm, UsuarioEditForm

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

@usuario_bp.route('/')
@permission_required('ver_usuarios')  
def index():
    search_query = request.args.get('search', '')
    
    if search_query:
        usuarios = Usuario.search(search_query)
    else:
        usuarios = Usuario.get_all()
    
    return usuario_view.list(usuarios, search_query)

@usuario_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    roles = Rol.query.all()
    form = UsuarioCreateForm()
    form.rol_id.choices = [(rol.id, rol.name) for rol in roles]
    
    if form.validate_on_submit():
        nuevo_usuario = Usuario(
            nombres=form.nombres.data,
            apellidos=form.apellidos.data,
            carnet=form.carnet.data,
            nacimiento=form.nacimiento.data,
            telefono=form.telefono.data,
            email=form.email.data,
            usuario=form.usuario.data,
            password=generate_password_hash(form.password.data),
            imagen=form.imagen.data,
            rol_id=form.rol_id.data
        )
        nuevo_usuario.save()
        return redirect(url_for('usuario.index'))
    
    return usuario_view.create(roles, form=form)

@usuario_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    usuario = Usuario.get_by_id(id)
    roles = Rol.query.all()
    
    if not usuario:
        return "Usuario no encontrado", 404
    
    form = UsuarioEditForm(obj=usuario)
    form.rol_id.choices = [(rol.id, rol.name) for rol in roles]
    form.usuario_actual = usuario  # Pasar usuario actual para validaciones
    
    if form.validate_on_submit():
        update_data = {
            'nombres': form.nombres.data,
            'apellidos': form.apellidos.data,
            'carnet': form.carnet.data,
            'nacimiento': form.nacimiento.data,
            'telefono': form.telefono.data,
            'email': form.email.data,
            'usuario': form.usuario.data,
            'imagen': form.imagen.data,
            'rol_id': form.rol_id.data
        }
        
        if form.password.data:
            update_data['password'] = generate_password_hash(form.password.data)
            
        usuario.update(**update_data)
        return redirect(url_for('usuario.index'))
    
    return usuario_view.edit(usuario, roles, form=form)

@usuario_bp.route('/delete/<int:id>')
@permission_required('eliminar_usuarios')  # Permiso específico para eliminación
def delete(id):
    usuario = Usuario.get_by_id(id)
    if usuario:
        usuario.delete()
    return redirect(url_for('usuario.index'))