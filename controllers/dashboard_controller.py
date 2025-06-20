from flask import Blueprint, render_template
from datetime import datetime, timedelta
from models.venta_model import Venta
from models.venta_detalle_model import VentaDetalle
from models.producto_model import Producto
from models.categoria_model import Categoria
from models.cliente_model import Cliente
from sqlalchemy import func, extract
from utils.decorators import login_required
import calendar
from database import db

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/', endpoint='index')
@login_required 
def dashboard():
    hoy = datetime.now()
    primer_dia_mes = datetime(hoy.year, hoy.month, 1)
    
    # 1. Resumen de tarjetas
    resumen = calcular_resumen(hoy, primer_dia_mes)
    
    # 2. Productos más vendidos
    productos_mas_vendidos, max_ventas = obtener_productos_mas_vendidos(primer_dia_mes, hoy)
    
    # 3. Últimas ventas
    ultimas_ventas = obtener_ultimas_ventas(5)
    
    # 4. Datos para gráficos
    datos_ventas_mensuales = obtener_ventas_mensuales(hoy.year)
    datos_ventas_categoria = obtener_ventas_por_categoria(primer_dia_mes, hoy)
    
    # 5. Ventas de hoy para reemplazar "Ventas por Asumat"
    ventas_hoy = calcular_ventas_hoy(hoy)
    
    return render_template('dashboard/index.html',
                          resumen=resumen,
                          productos_mas_vendidos=productos_mas_vendidos,
                          max_ventas=max_ventas,
                          ultimas_ventas=ultimas_ventas,
                          datos_ventas_mensuales=datos_ventas_mensuales,
                          datos_ventas_categoria=datos_ventas_categoria,
                          ventas_hoy=ventas_hoy,
                          hoy=hoy)

def calcular_resumen(hoy, primer_dia_mes):
    # Ventas totales (históricas)
    total_ventas = db.session.query(func.sum(Venta.total_neto)).scalar() or 0
    
    # Ventas del mes actual
    ventas_mes = db.session.query(func.sum(Venta.total_neto)).filter(
        Venta.fecha >= primer_dia_mes,
        Venta.fecha <= hoy
    ).scalar() or 0
    
    # Clientes nuevos este mes
    clientes_nuevos = db.session.query(Cliente).filter(
        Cliente.created_at >= primer_dia_mes,
        Cliente.created_at <= hoy
    ).count()
    
    # Productos vendidos este mes (cantidad total)
    productos_vendidos = db.session.query(func.sum(VentaDetalle.cantidad)).join(Venta).filter(
        Venta.fecha >= primer_dia_mes,
        Venta.fecha <= hoy
    ).scalar() or 0
    
    return [
        {'nombre': 'Ventas Totales', 'monto': total_ventas, 'color': '#4e73df', 'es_dinero': True},
        {'nombre': 'Ventas del Mes', 'monto': ventas_mes, 'color': '#1cc88a', 'es_dinero': True},
        {'nombre': 'Clientes Nuevos', 'monto': clientes_nuevos, 'color': '#36b9cc', 'es_dinero': False},
        {'nombre': 'Productos Vendidos', 'monto': productos_vendidos, 'color': '#f6c23e', 'es_dinero': False}
    ]

def obtener_productos_mas_vendidos(fecha_inicio, fecha_fin, limit=5):
    productos = db.session.query(
        Producto.nombre_comercial,
        Producto.categoria_id,
        func.sum(VentaDetalle.cantidad).label('cantidad_vendida')
    ).join(VentaDetalle.producto
    ).join(Venta, VentaDetalle.venta_id == Venta.id
    ).filter(
        Venta.fecha >= fecha_inicio,
        Venta.fecha <= fecha_fin
    ).group_by(Producto.id
    ).order_by(func.sum(VentaDetalle.cantidad).desc()
    ).limit(limit).all()
    
    if not productos:
        return [], 1
    
    max_cantidad = max(p.cantidad_vendida for p in productos) if productos else 0
    
    resultados = []
    for p in productos:
        categoria = db.session.query(Categoria).get(p.categoria_id) if p.categoria_id else None
        resultados.append({
            'nombre_comercial': p.nombre_comercial,
            'cantidad_vendida': p.cantidad_vendida,
            'categoria': categoria
        })
    
    return resultados, max_cantidad

def obtener_ultimas_ventas(limit=5):
    return db.session.query(Venta).order_by(Venta.fecha.desc()).limit(limit).all()

def obtener_ventas_mensuales(ano):
    ventas_por_mes = [0] * 12
    
    resultados = db.session.query(
        extract('month', Venta.fecha).label('mes'),
        func.sum(Venta.total_neto).label('total')
    ).filter(extract('year', Venta.fecha) == ano).group_by('mes').all()
    
    for r in resultados:
        if r.mes and r.total:
            ventas_por_mes[int(r.mes) - 1] = float(r.total)
    
    return {
        'labels': [calendar.month_abbr[i] for i in range(1, 13)],
        'data': ventas_por_mes
    }

def obtener_ventas_por_categoria(fecha_inicio, fecha_fin):
    categorias_ventas = db.session.query(
        Categoria.categoria,
        func.sum(VentaDetalle.cantidad * VentaDetalle.precio).label('total')
    ).join(VentaDetalle.producto).join(Producto.categoria).join(VentaDetalle.venta).filter(
        Venta.fecha >= fecha_inicio,
        Venta.fecha <= fecha_fin
    ).group_by(Categoria.id).all()
    
    if not categorias_ventas:
        return {'labels': [], 'data': []}
    
    labels = [cat.categoria for cat in categorias_ventas]
    data = [float(cat.total) for cat in categorias_ventas]
    
    return {'labels': labels, 'data': data}

def calcular_ventas_hoy(hoy):
    inicio_dia = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = hoy.replace(hour=23, minute=59, second=59, microsecond=999999)
    
    return db.session.query(func.sum(Venta.total_neto)).filter(
        Venta.fecha >= inicio_dia,
        Venta.fecha <= fin_dia
    ).scalar() or 0