from flask import request, redirect, url_for, Blueprint, render_template, flash
from models.laboratorio_model import Laboratorio
from views import laboratorio_view

laboratorio_bp = Blueprint('laboratorio', __name__, url_prefix='/laboratorios')

@laboratorio_bp.route('/')
def index():
    search_query = request.args.get('search', '')
    
    if search_query:
        laboratorios = Laboratorio.search(search_query)
    else:
        laboratorios = Laboratorio.get_all()
    
    return laboratorio_view.index(laboratorios, search_query)

@laboratorio_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre_lab = request.form['nombre_lab']
        direccion = request.form['direccion']
        responsable = request.form['responsable']
        telefono = request.form['telefono']
        
        nuevo_laboratorio = Laboratorio(
            nombre_lab=nombre_lab,
            direccion=direccion,
            responsable=responsable,
            telefono=telefono
        )
        nuevo_laboratorio.save()
        flash('Laboratorio creado exitosamente', 'success')
        return redirect(url_for('laboratorio.index'))
    return laboratorio_view.create()

@laboratorio_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    laboratorio = Laboratorio.get_by_id(id)
    if not laboratorio:
        flash('Laboratorio no encontrado', 'danger')
        return redirect(url_for('laboratorio.index'))
    
    if request.method == 'POST':
        laboratorio.update(
            nombre_lab=request.form['nombre_lab'],
            direccion=request.form['direccion'],
            responsable=request.form['responsable'],
            telefono=request.form['telefono']
        )
        flash('Laboratorio actualizado exitosamente', 'success')
        return redirect(url_for('laboratorio.index'))
    
    return laboratorio_view.edit(laboratorio)

@laboratorio_bp.route('/delete/<int:id>')
def delete(id):
    laboratorio = Laboratorio.get_by_id(id)
    if laboratorio:
        laboratorio.delete()
        flash('Laboratorio eliminado exitosamente', 'success')
    return redirect(url_for('laboratorio.index'))