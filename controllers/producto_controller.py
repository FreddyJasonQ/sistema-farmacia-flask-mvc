from flask import request, redirect, url_for, Blueprint, render_template, flash
from models.producto_model import Producto
from models.categoria_model import Categoria
from models.laboratorio_model import Laboratorio
from models.presentacion_model import Presentacion
from views import producto_view
from utils.decorators import permission_required  

producto_bp = Blueprint('producto', __name__, url_prefix='/productos')

@producto_bp.route('/')
@permission_required('ver_productos')  # Permiso único para ver productos
def index():
    search_query = request.args.get('search', '')
    
    if search_query:
        productos = Producto.search(search_query)
    else:
        productos = Producto.get_all()
    
    return producto_view.index(productos, search_query)

@producto_bp.route('/create', methods=['GET', 'POST'])
@permission_required('crear_productos')  # Permiso único para crear productos
def create():
    categorias = Categoria.get_all()
    laboratorios = Laboratorio.get_all()
    presentaciones = Presentacion.get_all()
    
    if request.method == 'POST':
        nombre_comercial = request.form['nombre_comercial']
        nombre_generico = request.form['nombre_generico']
        categoria_id = request.form['categoria_id']
        laboratorio_id = request.form['laboratorio_id']
        presentacion_id = request.form['presentacion_id']
        descripcion = request.form['descripcion']
        precio_compra = request.form['precio_compra'] or 0
        precio_venta = request.form['precio_venta'] or 0
        cantidad = request.form['cantidad'] or 0
        estado = 'estado' in request.form
        codigo = request.form['codigo']
        barcode = request.form['barcode']
        imagen = request.form['imagen']  
        
        nuevo_producto = Producto(
            nombre_comercial=nombre_comercial,
            nombre_generico=nombre_generico,
            categoria_id=categoria_id,
            laboratorio_id=laboratorio_id,
            presentacion_id=presentacion_id,
            descripcion=descripcion,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            cantidad=cantidad,
            estado=estado,
            codigo=codigo,
            barcode=barcode,
            imagen=imagen
        )
        nuevo_producto.save()
        flash('Producto creado exitosamente', 'success')
        return redirect(url_for('producto.index'))
    
    return producto_view.create(categorias, laboratorios, presentaciones)

@producto_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@permission_required('editar_productos')  # Permiso único para editar productos
def edit(id):
    producto = Producto.get_by_id(id)
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('producto.index'))
    
    categorias = Categoria.get_all()
    laboratorios = Laboratorio.get_all()
    presentaciones = Presentacion.get_all()
    
    if request.method == 'POST':
        producto.update(
            nombre_comercial=request.form['nombre_comercial'],
            nombre_generico=request.form['nombre_generico'],
            categoria_id=request.form['categoria_id'],
            laboratorio_id=request.form['laboratorio_id'],
            presentacion_id=request.form['presentacion_id'],
            descripcion=request.form['descripcion'],
            precio_compra=request.form['precio_compra'] or 0,
            precio_venta=request.form['precio_venta'] or 0,
            cantidad=request.form['cantidad'] or 0,
            estado='estado' in request.form,
            codigo=request.form['codigo'],
            barcode=request.form['barcode'],
            imagen=request.form['imagen']
        )
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('producto.index'))
    
    return producto_view.edit(producto, categorias, laboratorios, presentaciones)

@producto_bp.route('/delete/<int:id>')
@permission_required('eliminar_productos')  # Permiso único para eliminar productos
def delete(id):
    producto = Producto.get_by_id(id)
    if producto:
        producto.delete()
        flash('Producto eliminado exitosamente', 'success')
    return redirect(url_for('producto.index'))