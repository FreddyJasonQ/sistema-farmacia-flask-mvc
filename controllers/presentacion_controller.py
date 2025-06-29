from flask import request, redirect, url_for, Blueprint, render_template, flash
from models.presentacion_model import Presentacion
from views import presentacion_view
from utils.decorators import permission_required  

presentacion_bp = Blueprint('presentacion', __name__, url_prefix='/presentaciones')

@presentacion_bp.route('/')
@permission_required('ver_presentaciones')  # Permiso para ver presentaciones
def index():
    search_query = request.args.get('search', '')
    
    if search_query:
        presentaciones = Presentacion.search(search_query)
    else:
        presentaciones = Presentacion.get_all()
    
    return presentacion_view.index(presentaciones, search_query)

@presentacion_bp.route('/create', methods=['GET', 'POST'])
@permission_required('crear_presentaciones')  # Permiso para crear presentaciones
def create():
    if request.method == 'POST':
        presentacion = request.form['presentacion']
        descripcion = request.form['descripcion']
        estado = 'estado' in request.form
        
        nueva_presentacion = Presentacion(
            presentacion=presentacion,
            descripcion=descripcion,
            estado=estado
        )
        nueva_presentacion.save()
        flash('Presentación creada exitosamente', 'success')
        return redirect(url_for('presentacion.index'))
    return presentacion_view.create()

@presentacion_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@permission_required('editar_presentaciones')  # Permiso para editar presentaciones
def edit(id):
    presentacion = Presentacion.get_by_id(id)
    if not presentacion:
        flash('Presentación no encontrada', 'danger')
        return redirect(url_for('presentacion.index'))
    
    if request.method == 'POST':
        presentacion.update(
            presentacion=request.form['presentacion'],
            descripcion=request.form['descripcion'],
            estado='estado' in request.form
        )
        flash('Presentación actualizada exitosamente', 'success')
        return redirect(url_for('presentacion.index'))
    
    return presentacion_view.edit(presentacion)

@presentacion_bp.route('/delete/<int:id>')
@permission_required('eliminar_presentaciones')  # Permiso para eliminar presentaciones
def delete(id):
    presentacion = Presentacion.get_by_id(id)
    if presentacion:
        presentacion.delete()
        flash('Presentación eliminada exitosamente', 'success')
    return redirect(url_for('presentacion.index'))