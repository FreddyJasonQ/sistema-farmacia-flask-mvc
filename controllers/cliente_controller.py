from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.cliente_model import Cliente
from views import cliente_view

cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes')

@cliente_bp.route('/')
def index():
    search_query = request.args.get('search', '')
    if search_query:
        clientes = Cliente.search(search_query)
    else:
        clientes = Cliente.get_all()
    return cliente_view.index(clientes, search_query)

@cliente_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo_documento = request.form['tipo_documento']
        documento = request.form['documento']
        complemento = request.form.get('complemento', '')
        telefono = request.form['telefono']
        estado = 'estado' in request.form
        
        cliente = Cliente(
            nombre=nombre,
            tipo_documento=tipo_documento,
            documento=documento,
            complemento=complemento,
            telefono=telefono,
            estado=estado
        )
        cliente.save()
        flash('Cliente creado exitosamente', 'success')
        return redirect(url_for('cliente.index'))
    return cliente_view.create()

@cliente_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cliente = Cliente.get_by_id(id)
    if not cliente:
        flash('Cliente no encontrado', 'danger')
        return redirect(url_for('cliente.index'))
    
    if request.method == 'POST':
        cliente.update(
            nombre=request.form['nombre'],
            tipo_documento=request.form['tipo_documento'],
            documento=request.form['documento'],
            complemento=request.form.get('complemento', ''),
            telefono=request.form['telefono'],
            estado='estado' in request.form
        )
        flash('Cliente actualizado exitosamente', 'success')
        return redirect(url_for('cliente.index'))
    
    return cliente_view.edit(cliente)

@cliente_bp.route('/delete/<int:id>')
def delete(id):
    cliente = Cliente.get_by_id(id)
    if cliente:
        cliente.delete()
        flash('Cliente eliminado exitosamente', 'success')
    return redirect(url_for('cliente.index'))