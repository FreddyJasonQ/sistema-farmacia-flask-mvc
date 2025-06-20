from flask import request, redirect, url_for, Blueprint, render_template, flash
from models.categoria_model import Categoria
from views import categoria_view
from utils.decorators import login_required, permission_required
from forms.forms import CategoriaForm

categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')

@categoria_bp.route('/')
@login_required
@permission_required('ver_categorias')  # Permiso para ver categorías
def index():
    search_query = request.args.get('search', '')
    
    if search_query:
        categorias = Categoria.search(search_query)
    else:
        categorias = Categoria.get_all()
    
    return categoria_view.index(categorias, search_query)

@categoria_bp.route('/create', methods=['GET', 'POST'])
@login_required
@permission_required('crear_categorias')
def create():
    form = CategoriaForm()
    
    if form.validate_on_submit():
        nueva_categoria = Categoria(
            categoria=form.categoria.data,
            descripcion=form.descripcion.data,
            estado=form.estado.data
        )
        nueva_categoria.save()
        flash('Categoría creada exitosamente', 'success')
        return redirect(url_for('categoria.index'))
    
    return render_template('categorias/create.html', form=form)

@categoria_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@permission_required('editar_categorias')
def edit(id):
    categoria = Categoria.get_by_id(id)
    if not categoria:
        flash('Categoría no encontrada', 'danger')
        return redirect(url_for('categoria.index'))
    
    form = CategoriaForm(obj=categoria)  # Prellenar con los datos existentes
    
    if form.validate_on_submit():
        categoria.update(
            categoria=form.categoria.data,
            descripcion=form.descripcion.data,
            estado=form.estado.data
        )
        flash('Categoría actualizada exitosamente', 'success')
        return redirect(url_for('categoria.index'))
    
    return render_template('categorias/edit.html', categoria=categoria, form=form)

@categoria_bp.route('/delete/<int:id>')
@login_required
@permission_required('eliminar_categorias')  # Permiso para eliminar categorías
def delete(id):
    categoria = Categoria.get_by_id(id)
    if categoria:
        categoria.delete()
        flash('Categoría eliminada exitosamente', 'success')
    return redirect(url_for('categoria.index'))