# controllers/reporte_controller.py
from flask import Blueprint, render_template, request, jsonify
from models.venta_model import Venta
from models.venta_detalle_model import VentaDetalle
from models.producto_model import Producto
from models.categoria_model import Categoria
from models.usuario_model import Usuario
from datetime import datetime, timedelta
import json

reporte_bp = Blueprint('reporte', __name__, url_prefix='/reportes')

@reporte_bp.route('/ventas', methods=['GET', 'POST'])
def reporte_ventas():
    # Obtener parámetros de filtro
    fecha_inicio = request.form.get('fechaInicio', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    fecha_fin = request.form.get('fechaFin', datetime.now().strftime('%Y-%m-%d'))
    categoria_id = request.form.get('categoria', '')
    vendedor_id = request.form.get('vendedor', '')

    # Convertir a objetos datetime para consulta
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)  # Incluir todo el día fin

    # Consulta base de ventas
    ventas_query = Venta.query.filter(
        Venta.fecha >= fecha_inicio_dt,
        Venta.fecha <= fecha_fin_dt,
        Venta.deleted_at.is_(None)
    )

    # filtros adicionales
    if categoria_id:
        ventas_query = ventas_query.join(Venta.detalles).join(VentaDetalle.producto).filter(
            Producto.categoria_id == categoria_id
        )
    
    if vendedor_id:
        ventas_query = ventas_query.filter(Venta.usuario_id == vendedor_id)

    ventas = ventas_query.all()

    # Calcular métricas
    total_ventas = sum(venta.total_neto for venta in ventas)
    promedio_venta = total_ventas / len(ventas) if ventas else 0
    clientes_atendidos = len(set(venta.cliente_id for venta in ventas))
    productos_vendidos = sum(
        detalle.cantidad 
        for venta in ventas 
        for detalle in venta.detalles
    )

    # Datos para gráficos
    datos_tendencia = calcular_tendencia_ventas(ventas, fecha_inicio_dt, fecha_fin_dt)
    datos_categorias = calcular_ventas_por_categoria(ventas)

    # Top productos
    top_cantidad, top_valor = calcular_top_productos(ventas)

    # Obtener opciones para filtros
    categorias = Categoria.query.all()
    vendedores = Usuario.query.all()

    return render_template('reportes/ventas.html',
                           fecha_inicio=fecha_inicio,
                           fecha_fin=fecha_fin,
                           categoria_seleccionada=int(categoria_id) if categoria_id else '',
                           vendedor_seleccionado=int(vendedor_id) if vendedor_id else '',
                           total_ventas=total_ventas,
                           promedio_venta=promedio_venta,
                           clientes_atendidos=clientes_atendidos,
                           productos_vendidos=productos_vendidos,
                           datos_tendencia=json.dumps(datos_tendencia),
                           datos_categorias=json.dumps(datos_categorias),
                           ventas=ventas,
                           categorias=categorias,
                           vendedores=vendedores,
                           top_cantidad=top_cantidad[:5],
                           top_valor=top_valor[:5],
                           fecha_generacion=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
   
def calcular_tendencia_ventas(ventas, fecha_inicio, fecha_fin):
    # Crear un diccionario con todos los días en el rango
    tendencia = {}
    current_date = fecha_inicio
    while current_date <= fecha_fin:
        tendencia[current_date.strftime('%Y-%m-%d')] = 0
        current_date += timedelta(days=1)
    
    # Agregar ventas a los días correspondientes
    for venta in ventas:
        fecha = venta.fecha.strftime('%Y-%m-%d')
        if fecha in tendencia:
            tendencia[fecha] += float(venta.total_neto)
    
    return {
        'labels': list(tendencia.keys()),
        'data': list(tendencia.values())
    }

def calcular_ventas_por_categoria(ventas):
    categorias_ventas = {}
    for venta in ventas:
        for detalle in venta.detalles:
            categoria = detalle.producto.categoria.categoria if detalle.producto.categoria else 'Sin categoría'
            subtotal = float(detalle.subtotal)
            
            if categoria in categorias_ventas:
                categorias_ventas[categoria] += subtotal
            else:
                categorias_ventas[categoria] = subtotal
    
    return {
        'labels': list(categorias_ventas.keys()),
        'data': list(categorias_ventas.values())
    }

def calcular_top_productos(ventas):
    productos_cantidad = {}
    productos_valor = {}
    
    for venta in ventas:
        for detalle in venta.detalles:
            producto_id = detalle.producto_id
            producto_nombre = detalle.producto.nombre_comercial
            cantidad = detalle.cantidad
            subtotal = float(detalle.subtotal)
            
            # Por cantidad
            if producto_id in productos_cantidad:
                productos_cantidad[producto_id]['cantidad'] += cantidad
            else:
                productos_cantidad[producto_id] = {
                    'nombre': producto_nombre,
                    'cantidad': cantidad
                }
            
            # Por valor
            if producto_id in productos_valor:
                productos_valor[producto_id] += subtotal
            else:
                productos_valor[producto_id] = subtotal
    
    # Ordenar y formatear resultados
    top_cantidad = sorted(
        [{'nombre': p['nombre'], 'cantidad': p['cantidad']} 
         for p in productos_cantidad.values()],
        key=lambda x: x['cantidad'],
        reverse=True
    )
    
    top_valor = sorted(
        [{'nombre': productos_cantidad[id]['nombre'], 'total': total} 
         for id, total in productos_valor.items()],
        key=lambda x: x['total'],
        reverse=True
    )
    
    return top_cantidad, top_valor# controllers/reporte_controller.py
from flask import Blueprint, render_template, request, jsonify
from models.venta_model import Venta
from models.venta_detalle_model import VentaDetalle
from models.producto_model import Producto
from models.categoria_model import Categoria
from models.usuario_model import Usuario
from datetime import datetime, timedelta
import json

reporte_bp = Blueprint('reporte', __name__, url_prefix='/reportes')

@reporte_bp.route('/ventas', methods=['GET', 'POST'])
def reporte_ventas():
    # Obtener parámetros de filtro
    fecha_inicio = request.form.get('fechaInicio', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    fecha_fin = request.form.get('fechaFin', datetime.now().strftime('%Y-%m-%d'))
    categoria_id = request.form.get('categoria', '')
    vendedor_id = request.form.get('vendedor', '')

    # Convertir a objetos datetime para consulta
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)  # Incluir todo el día fin

    # Consulta base de ventas
    ventas_query = Venta.query.filter(
        Venta.fecha >= fecha_inicio_dt,
        Venta.fecha <= fecha_fin_dt,
        Venta.deleted_at.is_(None)
    )

    # Aplicar filtros adicionales
    if categoria_id:
        ventas_query = ventas_query.join(Venta.detalles).join(VentaDetalle.producto).filter(
            Producto.categoria_id == categoria_id
        )
    
    if vendedor_id:
        ventas_query = ventas_query.filter(Venta.usuario_id == vendedor_id)

    ventas = ventas_query.all()

    # Calcular métricas
    total_ventas = sum(venta.total_neto for venta in ventas)
    promedio_venta = total_ventas / len(ventas) if ventas else 0
    clientes_atendidos = len(set(venta.cliente_id for venta in ventas))
    productos_vendidos = sum(
        detalle.cantidad 
        for venta in ventas 
        for detalle in venta.detalles
    )

    # Datos para gráficos
    datos_tendencia = calcular_tendencia_ventas(ventas, fecha_inicio_dt, fecha_fin_dt)
    datos_categorias = calcular_ventas_por_categoria(ventas)

    # Top productos
    top_cantidad, top_valor = calcular_top_productos(ventas)

    # Obtener opciones para filtros
    categorias = Categoria.query.all()
    vendedores = Usuario.query.all()

    return render_template('reportes/ventas.html',
                           fecha_inicio=fecha_inicio,
                           fecha_fin=fecha_fin,
                           categoria_seleccionada=int(categoria_id) if categoria_id else '',
                           vendedor_seleccionado=int(vendedor_id) if vendedor_id else '',
                           total_ventas=total_ventas,
                           promedio_venta=promedio_venta,
                           clientes_atendidos=clientes_atendidos,
                           productos_vendidos=productos_vendidos,
                           datos_tendencia=json.dumps(datos_tendencia),
                           datos_categorias=json.dumps(datos_categorias),
                           ventas=ventas,
                           categorias=categorias,
                           vendedores=vendedores,
                           top_cantidad=top_cantidad[:5],
                           top_valor=top_valor[:5],
                           fecha_generacion=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
   
def calcular_tendencia_ventas(ventas, fecha_inicio, fecha_fin):
    # Crear un diccionario con todos los días en el rango
    tendencia = {}
    current_date = fecha_inicio
    while current_date <= fecha_fin:
        tendencia[current_date.strftime('%Y-%m-%d')] = 0
        current_date += timedelta(days=1)
    
    # Agregar ventas a los días correspondientes
    for venta in ventas:
        fecha = venta.fecha.strftime('%Y-%m-%d')
        if fecha in tendencia:
            tendencia[fecha] += float(venta.total_neto)
    
    return {
        'labels': list(tendencia.keys()),
        'data': list(tendencia.values())
    }

def calcular_ventas_por_categoria(ventas):
    categorias_ventas = {}
    for venta in ventas:
        for detalle in venta.detalles:
            categoria = detalle.producto.categoria.categoria if detalle.producto.categoria else 'Sin categoría'
            subtotal = float(detalle.subtotal)
            
            if categoria in categorias_ventas:
                categorias_ventas[categoria] += subtotal
            else:
                categorias_ventas[categoria] = subtotal
    
    return {
        'labels': list(categorias_ventas.keys()),
        'data': list(categorias_ventas.values())
    }

def calcular_top_productos(ventas):
    productos_cantidad = {}
    productos_valor = {}
    
    for venta in ventas:
        for detalle in venta.detalles:
            producto_id = detalle.producto_id
            producto_nombre = detalle.producto.nombre_comercial
            cantidad = detalle.cantidad
            subtotal = float(detalle.subtotal)
            
            # Por cantidad
            if producto_id in productos_cantidad:
                productos_cantidad[producto_id]['cantidad'] += cantidad
            else:
                productos_cantidad[producto_id] = {
                    'nombre': producto_nombre,
                    'cantidad': cantidad
                }
            
            # Por valor
            if producto_id in productos_valor:
                productos_valor[producto_id] += subtotal
            else:
                productos_valor[producto_id] = subtotal
    
    # Ordenar y formatear resultados
    top_cantidad = sorted(
        [{'nombre': p['nombre'], 'cantidad': p['cantidad']} 
         for p in productos_cantidad.values()],
        key=lambda x: x['cantidad'],
        reverse=True
    )
    
    top_valor = sorted(
        [{'nombre': productos_cantidad[id]['nombre'], 'total': total} 
         for id, total in productos_valor.items()],
        key=lambda x: x['total'],
        reverse=True
    )
    
    return top_cantidad, top_valor# controllers/reporte_controller.py
from flask import Blueprint, render_template, request, jsonify
from models.venta_model import Venta
from models.venta_detalle_model import VentaDetalle
from models.producto_model import Producto
from models.categoria_model import Categoria
from models.usuario_model import Usuario
from datetime import datetime, timedelta
import json

reporte_bp = Blueprint('reporte', __name__, url_prefix='/reportes')

@reporte_bp.route('/ventas', methods=['GET', 'POST'])
def reporte_ventas():
    # Obtener parámetros de filtro
    fecha_inicio = request.form.get('fechaInicio', (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
    fecha_fin = request.form.get('fechaFin', datetime.now().strftime('%Y-%m-%d'))
    categoria_id = request.form.get('categoria', '')
    vendedor_id = request.form.get('vendedor', '')

    # Convertir a objetos datetime para consulta
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)  # Incluir todo el día fin

    # Consulta base de ventas
    ventas_query = Venta.query.filter(
        Venta.fecha >= fecha_inicio_dt,
        Venta.fecha <= fecha_fin_dt,
        Venta.deleted_at.is_(None)
    )

    # Aplicar filtros adicionales
    if categoria_id:
        ventas_query = ventas_query.join(Venta.detalles).join(VentaDetalle.producto).filter(
            Producto.categoria_id == categoria_id
        )
    
    if vendedor_id:
        ventas_query = ventas_query.filter(Venta.usuario_id == vendedor_id)

    ventas = ventas_query.all()

    # Calcular métricas
    total_ventas = sum(venta.total_neto for venta in ventas)
    promedio_venta = total_ventas / len(ventas) if ventas else 0
    clientes_atendidos = len(set(venta.cliente_id for venta in ventas))
    productos_vendidos = sum(
        detalle.cantidad 
        for venta in ventas 
        for detalle in venta.detalles
    )

    # Datos para gráficos
    datos_tendencia = calcular_tendencia_ventas(ventas, fecha_inicio_dt, fecha_fin_dt)
    datos_categorias = calcular_ventas_por_categoria(ventas)

    # Top productos
    top_cantidad, top_valor = calcular_top_productos(ventas)

    # Obtener opciones para filtros
    categorias = Categoria.query.all()
    vendedores = Usuario.query.all()

    return render_template('reportes/ventas.html',
                           fecha_inicio=fecha_inicio,
                           fecha_fin=fecha_fin,
                           categoria_seleccionada=int(categoria_id) if categoria_id else '',
                           vendedor_seleccionado=int(vendedor_id) if vendedor_id else '',
                           total_ventas=total_ventas,
                           promedio_venta=promedio_venta,
                           clientes_atendidos=clientes_atendidos,
                           productos_vendidos=productos_vendidos,
                           datos_tendencia=json.dumps(datos_tendencia),
                           datos_categorias=json.dumps(datos_categorias),
                           ventas=ventas,
                           categorias=categorias,
                           vendedores=vendedores,
                           top_cantidad=top_cantidad[:5],
                           top_valor=top_valor[:5],
                           fecha_generacion=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
   
def calcular_tendencia_ventas(ventas, fecha_inicio, fecha_fin):
    # Crear un diccionario con todos los días en el rango
    tendencia = {}
    current_date = fecha_inicio
    while current_date <= fecha_fin:
        tendencia[current_date.strftime('%Y-%m-%d')] = 0
        current_date += timedelta(days=1)
    
    # Agregar ventas a los días correspondientes
    for venta in ventas:
        fecha = venta.fecha.strftime('%Y-%m-%d')
        if fecha in tendencia:
            tendencia[fecha] += float(venta.total_neto)
    
    return {
        'labels': list(tendencia.keys()),
        'data': list(tendencia.values())
    }

def calcular_ventas_por_categoria(ventas):
    categorias_ventas = {}
    for venta in ventas:
        for detalle in venta.detalles:
            categoria = detalle.producto.categoria.categoria if detalle.producto.categoria else 'Sin categoría'
            subtotal = float(detalle.subtotal)
            
            if categoria in categorias_ventas:
                categorias_ventas[categoria] += subtotal
            else:
                categorias_ventas[categoria] = subtotal
    
    return {
        'labels': list(categorias_ventas.keys()),
        'data': list(categorias_ventas.values())
    }

def calcular_top_productos(ventas):
    productos_cantidad = {}
    productos_valor = {}
    
    for venta in ventas:
        for detalle in venta.detalles:
            producto_id = detalle.producto_id
            producto_nombre = detalle.producto.nombre_comercial
            cantidad = detalle.cantidad
            subtotal = float(detalle.subtotal)
            
            # Por cantidad
            if producto_id in productos_cantidad:
                productos_cantidad[producto_id]['cantidad'] += cantidad
            else:
                productos_cantidad[producto_id] = {
                    'nombre': producto_nombre,
                    'cantidad': cantidad
                }
            
            # Por valor
            if producto_id in productos_valor:
                productos_valor[producto_id] += subtotal
            else:
                productos_valor[producto_id] = subtotal
    
    # Ordenar y formatear resultados
    top_cantidad = sorted(
        [{'nombre': p['nombre'], 'cantidad': p['cantidad']} 
         for p in productos_cantidad.values()],
        key=lambda x: x['cantidad'],
        reverse=True
    )
    
    top_valor = sorted(
        [{'nombre': productos_cantidad[id]['nombre'], 'total': total} 
         for id, total in productos_valor.items()],
        key=lambda x: x['total'],
        reverse=True
    )
    
    return top_cantidad, top_valor