from flask import render_template
from flask_login import current_user
from datetime import datetime, timedelta
from . import dash_bp
from sqlalchemy import func
from models import Producto, Categoria, Venta, DetalleVenta

@dash_bp.route("/", methods=["GET", "POST"])
def auth():
    fecha_hoy = datetime.now().strftime('%d de %B %Y')
    
    fecha_inicio = datetime.now() - timedelta(days=6)
    ventas_semanales_query = (
        Venta.query
        .filter(Venta.fecha >= fecha_inicio)
        .with_entities(func.date(Venta.fecha).label("dia"), func.sum(Venta.total).label("total"))
        .group_by(func.date(Venta.fecha))
        .order_by(func.date(Venta.fecha))
        .all()
    )

    ventas_dict = {v.dia.strftime('%a'): float(v.total) for v in ventas_semanales_query}
    dias_ingles = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    dias_es = ['LUN','MAR','MIE','JUE','VIE','SAB','DOM']
    ventas_ordenadas = [ventas_dict.get(d,0) for d in dias_ingles]

    ventas_semanales = {
        "labels": dias_es,
        "data": ventas_ordenadas
    }

    distribucion_query = (
        DetalleVenta.query
        .join(Producto)
        .join(Categoria, Producto.idCategoria == Categoria.id)
        .with_entities(Categoria.nombre.label("categoria"), func.sum(DetalleVenta.cantidad).label("cantidad"))
        .group_by(Categoria.nombre)
        .all()
    )

    distribucion = {
        "labels": [d.categoria for d in distribucion_query],
        "data": [float(d.cantidad) for d in distribucion_query]
    }

    utilidad_query = (
        DetalleVenta.query
        .join(Producto)
        .with_entities(
            Producto.nombre.label("producto"),
            func.sum(DetalleVenta.cantidad * DetalleVenta.precioUnitario).label("venta_total"),
            (func.sum(DetalleVenta.cantidad * DetalleVenta.precioUnitario) - func.sum(DetalleVenta.cantidad * Producto.costoUnitario)).label("utilidad")
        )
        .group_by(Producto.id)
        .all()
    )

    utilidad_productos = [
        {
            "producto": u.producto,
            "venta": float(u.venta_total),
            "utilidad": float(u.utilidad)
        } for u in utilidad_query
    ]

    fecha_semana = datetime.now() - timedelta(days=7)
    fecha_mes = datetime.now() - timedelta(days=30)

    mas_vendidos_semana = (
        DetalleVenta.query
        .join(Producto)
        .join(Venta)
        .filter(Venta.fecha >= fecha_semana)
        .with_entities(
            Producto.nombre,
            func.sum(DetalleVenta.cantidad).label("cantidad")
        )
        .group_by(Producto.nombre)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
        .limit(5)
        .all()
    )

    mas_vendidos_semana_monto = (
        DetalleVenta.query
        .join(Producto)
        .join(Venta)
        .filter(Venta.fecha >= fecha_semana)
        .with_entities(
            Producto.nombre,
            func.sum(DetalleVenta.cantidad * DetalleVenta.precioUnitario).label("total")
        )
        .group_by(Producto.nombre)
        .order_by(func.sum(DetalleVenta.cantidad * DetalleVenta.precioUnitario).desc())
        .limit(5)
        .all()
    )

    mas_vendidos_mes = (
        DetalleVenta.query
        .join(Producto)
        .join(Venta)
        .filter(Venta.fecha >= fecha_mes)
        .with_entities(
            Producto.nombre,
            func.sum(DetalleVenta.cantidad).label("cantidad")
        )
        .group_by(Producto.nombre)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
        .limit(5)
        .all()
    )

    mas_vendidos_mes_monto = (
        DetalleVenta.query
        .join(Producto)
        .join(Venta)
        .filter(Venta.fecha >= fecha_mes)
        .with_entities(
            Producto.nombre,
            func.sum(DetalleVenta.cantidad * DetalleVenta.precioUnitario).label("total")
        )
        .group_by(Producto.nombre)
        .order_by(func.sum(DetalleVenta.cantidad * DetalleVenta.precioUnitario).desc())
        .limit(5)
        .all()
    )

    top_semana = {
        "labels": [p.nombre for p in mas_vendidos_semana],
        "data": [float(p.cantidad) for p in mas_vendidos_semana]
    }

    top_semana_monto = {
        "labels": [p.nombre for p in mas_vendidos_semana_monto],
        "data": [float(p.total) for p in mas_vendidos_semana_monto]
    }

    top_mes = {
        "labels": [p.nombre for p in mas_vendidos_mes],
        "data": [float(p.cantidad) for p in mas_vendidos_mes]
    }

    top_mes_monto = {
        "labels": [p.nombre for p in mas_vendidos_mes_monto],
        "data": [float(p.total) for p in mas_vendidos_mes_monto]
    }

    return render_template(
        "dashboard/dash.html",
        fecha_hoy=fecha_hoy,
        ventas_semanales=ventas_semanales,
        distribucion=distribucion,
        utilidad_productos=utilidad_productos,
        top_semana=top_semana,
        top_semana_monto=top_semana_monto,
        top_mes=top_mes,
        top_mes_monto=top_mes_monto,
        current_date=datetime.now().strftime('%d/%m/%Y'),
        usuario_nombre=current_user.nombre if current_user.is_authenticated else "Usuario"
    )