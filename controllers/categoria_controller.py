from flask import request, redirect, url_for, Blueprint, render_template, flash
from models.categoria_model import Categoria
from views import categoria_view

categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')

@categoria_bp.route('/')
def index():
    search_query = request.args.get('search', '')
    
    if search_query:
        categorias = Categoria.search(search_query)
    else:
        categorias = Categoria.get_all()
    
    return categoria_view.index(categorias, search_query)

@categoria_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        estado = 'estado' in request.form  # Checkbox
        
        nueva_categoria = Categoria(
            categoria=categoria,
            descripcion=descripcion,
            estado=estado
        )
        nueva_categoria.save()
        flash('Categoría creada exitosamente', 'success')
        return redirect(url_for('categoria.index'))
    return categoria_view.create()

@categoria_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    categoria = Categoria.get_by_id(id)
    if not categoria:
        flash('Categoría no encontrada', 'danger')
        return redirect(url_for('categoria.index'))
    
    if request.method == 'POST':
        categoria.update(
            categoria=request.form['categoria'],
            descripcion=request.form['descripcion'],
            estado='estado' in request.form
        )
        flash('Categoría actualizada exitosamente', 'success')
        return redirect(url_for('categoria.index'))
    
    return categoria_view.edit(categoria)

@categoria_bp.route('/delete/<int:id>')
def delete(id):
    categoria = Categoria.get_by_id(id)
    if categoria:
        categoria.delete()
        flash('Categoría eliminada exitosamente', 'success')
    return redirect(url_for('categoria.index'))