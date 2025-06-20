from flask import request, redirect, url_for, Blueprint, render_template, flash
from models.laboratorio_model import Laboratorio
from views import laboratorio_view
from utils.decorators import permission_required  
from forms.forms import LaboratorioForm

laboratorio_bp = Blueprint('laboratorio', __name__, url_prefix='/laboratorios')

@laboratorio_bp.route('/')
@permission_required('ver_laboratorios')  # Permiso para ver laboratorios
def index():
    search_query = request.args.get('search', '')
    
    if search_query:
        laboratorios = Laboratorio.search(search_query)
    else:
        laboratorios = Laboratorio.get_all()
    
    return laboratorio_view.index(laboratorios, search_query)

@laboratorio_bp.route('/create', methods=['GET', 'POST'])
@permission_required('crear_laboratorios')
def create():
    form = LaboratorioForm()
    
    if form.validate_on_submit():
        nuevo_laboratorio = Laboratorio(
            nombre_lab=form.nombre_lab.data,
            direccion=form.direccion.data,
            responsable=form.responsable.data,
            telefono=form.telefono.data
        )
        nuevo_laboratorio.save()
        flash('Laboratorio creado exitosamente', 'success')
        return redirect(url_for('laboratorio.index'))
    
    return render_template('laboratorios/create.html', form=form)

@laboratorio_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@permission_required('editar_laboratorios')
def edit(id):
    laboratorio = Laboratorio.get_by_id(id)
    if not laboratorio:
        flash('Laboratorio no encontrado', 'danger')
        return redirect(url_for('laboratorio.index'))
    
    form = LaboratorioForm(obj=laboratorio)
    
    if form.validate_on_submit():
        form.populate_obj(laboratorio)
        laboratorio.update()
        flash('Laboratorio actualizado exitosamente', 'success')
        return redirect(url_for('laboratorio.index'))
    
    return render_template('laboratorios/edit.html', form=form, laboratorio=laboratorio)

@laboratorio_bp.route('/delete/<int:id>')
@permission_required('eliminar_laboratorios')  # Permiso para eliminar laboratorios
def delete(id):
    laboratorio = Laboratorio.get_by_id(id)
    if laboratorio:
        laboratorio.delete()
        flash('Laboratorio eliminado exitosamente', 'success')
    return redirect(url_for('laboratorio.index'))