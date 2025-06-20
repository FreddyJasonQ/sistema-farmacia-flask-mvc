from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.cliente_model import Cliente
from views import cliente_view
from utils.decorators import login_required, permission_required  
from forms.forms import ClienteForm 

cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes')

@cliente_bp.route('/')
@login_required
@permission_required('ver_clientes')  # Permiso específico para ver clientes
def index():
    search_query = request.args.get('search', '')
    if search_query:
        clientes = Cliente.search(search_query)
    else:
        clientes = Cliente.get_all()
    return cliente_view.index(clientes, search_query)

@cliente_bp.route('/create', methods=['GET', 'POST'])
@login_required
@permission_required('crear_clientes')
def create():
    form = ClienteForm()
    
    if form.validate_on_submit():
        cliente = Cliente(
            nombre=form.nombre.data,
            tipo_documento=form.tipo_documento.data,
            documento=form.documento.data,
            complemento=form.complemento.data or '',
            telefono=form.telefono.data,
            estado=form.estado.data
        )
        cliente.save()
        flash('Cliente creado exitosamente', 'success')
        return redirect(url_for('cliente.index'))
    
    return render_template('clientes/create.html', form=form)

@cliente_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required('editar_clientes')
def edit(id):
    cliente = Cliente.get_by_id(id)
    if not cliente:
        flash('Cliente no encontrado', 'danger')
        return redirect(url_for('cliente.index'))
    
    form = ClienteForm(obj=cliente)  # Prellenar con datos del cliente
    
    if form.validate_on_submit():
        cliente.update(
            nombre=form.nombre.data,
            tipo_documento=form.tipo_documento.data,
            documento=form.documento.data,
            complemento=form.complemento.data or '',
            telefono=form.telefono.data,
            estado=form.estado.data
        )
        flash('Cliente actualizado exitosamente', 'success')
        return redirect(url_for('cliente.index'))
    
    return render_template('clientes/edit.html', form=form, cliente=cliente)

@cliente_bp.route('/delete/<int:id>')
@login_required
@permission_required('eliminar_clientes')  # Permiso específico para eliminar clientes
def delete(id):
    cliente = Cliente.get_by_id(id)
    if cliente:
        cliente.delete()
        flash('Cliente eliminado exitosamente', 'success')
    return redirect(url_for('cliente.index'))