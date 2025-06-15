from flask import request, redirect, url_for, Blueprint, render_template
from models.usuario_model import Usuario
from views import usuario_view
from datetime import datetime
from models.rol_model import Rol

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

@usuario_bp.route('/')
def index():
    search_query = request.args.get('search', '')
    
    if search_query:
        usuarios = Usuario.search(search_query)
    else:
        usuarios = Usuario.get_all()
    
    return usuario_view.list(usuarios, search_query)

@usuario_bp.route('/create', methods=['GET', 'POST'])
def create():
    roles = Rol.query.all()
    
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        carnet = request.form['carnet']
        nacimiento = datetime.strptime(request.form['nacimiento'], '%Y-%m-%d').date()
        telefono = request.form['telefono']
        email = request.form['email']
        usuario = request.form['usuario']
        password = request.form['password']
        imagen = request.form.get('imagen', None)
        rol_id = request.form['rol_id']
        
        nuevo_usuario = Usuario(
            nombres=nombres,
            apellidos=apellidos,
            carnet=carnet,
            nacimiento=nacimiento,
            telefono=telefono,
            email=email,
            usuario=usuario,
            password=password,
            imagen=imagen,
            rol_id=rol_id
        )
        nuevo_usuario.save()
        return redirect(url_for('usuario.index'))
    
    return usuario_view.create(roles)

@usuario_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    usuario = Usuario.get_by_id(id)
    roles = Rol.query.all()
    
    if not usuario:
        return "Usuario no encontrado", 404
    
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        carnet = request.form['carnet']
        nacimiento = datetime.strptime(request.form['nacimiento'], '%Y-%m-%d').date()
        telefono = request.form['telefono']
        email = request.form['email']
        usuario_form = request.form['usuario']
        imagen = request.form.get('imagen', None)
        rol_id = request.form['rol_id']
        password = request.form.get('password', None)
        
        update_data = {
            'nombres': nombres,
            'apellidos': apellidos,
            'carnet': carnet,
            'nacimiento': nacimiento,
            'telefono': telefono,
            'email': email,
            'usuario': usuario_form,
            'imagen': imagen,
            'rol_id': rol_id
        }
        
        if password:  # Solo actualizar contraseña si se proporciona
            update_data['password'] = password
            
        usuario.update(**update_data)
        return redirect(url_for('usuario.index'))
    
    return usuario_view.edit(usuario, roles)

@usuario_bp.route('/delete/<int:id>')
def delete(id):
    usuario = Usuario.get_by_id(id)
    if usuario:
        usuario.delete()
    return redirect(url_for('usuario.index'))