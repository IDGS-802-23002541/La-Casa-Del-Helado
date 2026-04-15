from flask import render_template, request
from flask_login import current_user
from datetime import datetime, timedelta
from . import dash_bp
from sqlalchemy import func, case, extract
from models import Producto, Categoria, Venta, DetalleVenta, MateriaPrima
from flask_security.decorators import roles_accepted, login_required

@dash_bp.route("/dash", methods=["GET", "POST"])
@login_required
@roles_accepted('Administrador')
def auth():

    filtro = request.args.get('filtro', 'semana')
    mes = request.args.get('mes')

    fecha_hoy = datetime.now().strftime('%d de %B %Y')

    if filtro == "semana":

        fecha_inicio = datetime.now() - timedelta(days=6)

        ventas_semanales_query = (
            Venta.query
            .filter(Venta.fecha >= fecha_inicio)
            .with_entities(
                func.date(Venta.fecha).label("dia"),
                func.sum(Venta.total).label("total")
            )
            .group_by(func.date(Venta.fecha))
            .order_by(func.date(Venta.fecha))
            .all()
        )

        ventas_dict = {v.dia.strftime('%a'): float(v.total) for v in ventas_semanales_query}
        dias_ingles = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        dias_es = ['LUN','MAR','MIE','JUE','VIE','SAB','DOM']
        ventas_ordenadas = [ventas_dict.get(d,0) for d in dias_ingles]

        labels = dias_es
        data = ventas_ordenadas

    elif filtro == "mes":

        mes_actual = int(mes) if mes else datetime.now().month

        ventas_query = (
            Venta.query
            .filter(extract('month', Venta.fecha) == mes_actual)
            .with_entities(
                extract('week', Venta.fecha).label("semana"),
                func.sum(Venta.total).label("total")
            )
            .group_by("semana")
            .order_by("semana")
            .all()
        )

        labels = [f"Sem {int(v.semana)}" for v in ventas_query]
        data = [float(v.total) for v in ventas_query]

    else:

        ventas_query = (
            Venta.query
            .with_entities(
                extract('month', Venta.fecha).label("mes"),
                func.sum(Venta.total).label("total")
            )
            .group_by("mes")
            .order_by("mes")
            .all()
        )

        meses_nombres = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
        labels = [meses_nombres[int(v.mes)-1] for v in ventas_query]
        data = [float(v.total) for v in ventas_query]

    ventas_semanales = {"labels": labels, "data": data}

    distribucion_query = (
        DetalleVenta.query
        .join(Producto)
        .join(Categoria, Producto.idCategoria == Categoria.id)
        .join(Venta)
    )

    if filtro == "semana":
        distribucion_query = distribucion_query.filter(Venta.fecha >= datetime.now()-timedelta(days=7))
    elif filtro == "mes":
        distribucion_query = distribucion_query.filter(
            extract('month', Venta.fecha) == (int(mes) if mes else datetime.now().month)
        )

    distribucion_query = (
        distribucion_query
        .with_entities(
            Categoria.nombre.label("categoria"),
            func.sum(DetalleVenta.cantidad).label("cantidad")
        )
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
            (
                func.sum(DetalleVenta.cantidad * DetalleVenta.precioUnitario)
                -
                func.sum(
                    case(
                        (
                            Producto.unidadBase == 'L',
                            DetalleVenta.cantidad * 0.1 * Producto.costoUnitario
                        ),
                        else_=DetalleVenta.cantidad * Producto.costoUnitario
                    )
                )
            ).label("utilidad")
        )
        .group_by(Producto.id)
        .all()
    )

    utilidad_productos = [
        {
            "producto": u.producto,
            "venta": float(u.venta_total or 0),
            "utilidad": float(u.utilidad or 0)
        }
        for u in utilidad_query
    ]

    fecha_semana = datetime.now() - timedelta(days=7)
    fecha_mes = datetime.now() - timedelta(days=30)

    mas_vendidos_semana = (
        DetalleVenta.query
        .join(Producto)
        .join(Venta)
        .filter(Venta.fecha >= fecha_semana)
        .with_entities(Producto.nombre, func.sum(DetalleVenta.cantidad))
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
        .with_entities(Producto.nombre, func.sum(DetalleVenta.cantidad * DetalleVenta.precioUnitario))
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
        .with_entities(Producto.nombre, func.sum(DetalleVenta.cantidad))
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
        .with_entities(Producto.nombre, func.sum(DetalleVenta.cantidad * DetalleVenta.precioUnitario))
        .group_by(Producto.nombre)
        .order_by(func.sum(DetalleVenta.cantidad * DetalleVenta.precioUnitario).desc())
        .limit(5)
        .all()
    )

    top_semana = {"labels": [p[0] for p in mas_vendidos_semana], "data": [float(p[1]) for p in mas_vendidos_semana]}
    top_semana_monto = {"labels": [p[0] for p in mas_vendidos_semana_monto], "data": [float(p[1]) for p in mas_vendidos_semana_monto]}
    top_mes = {"labels": [p[0] for p in mas_vendidos_mes], "data": [float(p[1]) for p in mas_vendidos_mes]}
    top_mes_monto = {"labels": [p[0] for p in mas_vendidos_mes_monto], "data": [float(p[1]) for p in mas_vendidos_mes_monto]}

    def nivel_stock(actual, minimo):
        actual = float(actual or 0)
        minimo = float(minimo or 0)

        if actual <= minimo:
            return "BAJO"
        elif actual <= minimo * 1.5:
            return "MEDIO"
        else:
            return "ALTO"

    productos = Producto.query.all()
    materias = MateriaPrima.query.filter_by(estatus=True).all()

    alertas_productos = []
    for p in productos:
        alertas_productos.append({
            "nombre": p.nombre,
            "stock": float(p.stockActual),
            "minimo": float(p.stockMinimo),
            "nivel": nivel_stock(p.stockActual, p.stockMinimo)
        })

    alertas_materias = []
    for m in materias:
        alertas_materias.append({
            "nombre": m.nombre,
            "stock": float(m.stockActual),
            "minimo": float(m.stockMinimo),
            "nivel": nivel_stock(m.stockActual, m.stockMinimo)
        })

    alertas_productos = [a for a in alertas_productos if a["nivel"] != "ALTO"]
    alertas_materias = [a for a in alertas_materias if a["nivel"] != "ALTO"]

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
        alertas_productos=alertas_productos,
        alertas_materias=alertas_materias,
        current_date=datetime.now().strftime('%d/%m/%Y'),
        usuario_nombre=current_user.nombre if current_user.is_authenticated else "Usuario"
    )