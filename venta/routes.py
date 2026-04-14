from flask import render_template, request, redirect, url_for, session, flash
from models import db, Producto, Categoria, presentacionVenta, Receta, DetalleReceta, MateriaPrima
from . import venta_bp
from flask_security import current_user
from datetime import datetime
import uuid

# --- MANEJO DE ERRORES ---
@venta_bp.app_errorhandler(403)
def error_403(e):
    return render_template("errors/403.html"), 403

@venta_bp.app_errorhandler(404)
def error_404(e):
    return render_template("errors/404.html"), 404

@venta_bp.route("/venta", methods=["GET"])
@login_required
@roles_accepted('Mostrador')
def punto_venta():
    vista = 'vd'
    categorias = Categoria.query.all()
    
    presentaciones = presentacionVenta.query.filter_by(estatus=True).all()
    carrito = session.get('carrito_pos', [])
    total_v = sum(float(item['subtotal']) for item in carrito)

    return render_template(
        "punto_venta/venta.html",
        presentaciones=presentaciones,
        categorias=categorias,
        carrito=carrito,
        total=total_v,
        vista=vista
    )


@venta_bp.route("/venta/filtrar", methods=["GET"])
@login_required
@roles_accepted('Mostrador')
def filtrar_productos():
    categoria_id = request.args.get('cat_id', type=int)
    busqueda = request.args.get('q', '').strip()

    query = presentacionVenta.query.filter_by(estatus=True)
    if busqueda:
        query = query.filter(presentacionVenta.nombre.ilike(f"%{busqueda}%"))
    if categoria_id:
        query = query.join(Producto).filter(Producto.idCategoria == categoria_id)
    presentaciones = query.all()
    categorias = Categoria.query.all()

    carrito = session.get('carrito_pos', [])
    total_v = sum(float(item.get('subtotal', 0)) for item in carrito)

    return render_template(
        "punto_venta/venta.html",
        presentaciones=presentaciones,
        categorias=categorias,
        carrito=carrito,
        total=total_v,
        vista='vd',
        cat_actual=categoria_id,
        query_actual=busqueda
    )


@venta_bp.route("/vender_agregar", methods=["POST"])
@login_required
@roles_accepted('Mostrador')
def vender_agregar():
    id_pres = request.form.get('id')
    if not id_pres:
        return redirect(url_for('venta.punto_venta'))
    pres = presentacionVenta.query.get_or_404(id_pres)
    precio = float(pres.precio)

    carrito = session.get('carrito_pos', [])
    for item in carrito:
        if item['id'] == int(id_pres):
            item['cantidad'] += 1
            item['subtotal'] = item['cantidad'] * precio
            break
    else:
        carrito.append({
            'id': pres.id,
            'nombre': pres.nombre,
            'cantidad': 1,
            'precio': precio,
            'subtotal': precio,
            'idProductoBase': pres.idProductoBase,
            'equivalencia': float(pres.equivalencia)
        })

    session['carrito_pos'] = carrito
    session.modified = True
    return redirect(url_for('venta.punto_venta'))

@venta_bp.route("/finalizar_venta", methods=["POST"])
@login_required
@roles_accepted('Mostrador')
def finalizar_venta():
    carrito = session.get('carrito_pos', [])

    if not carrito:
        flash("El carrito está vacío", "warning")
        return redirect(url_for('venta.punto_venta'))
    try:
        total = sum(float(i['subtotal']) for i in carrito)
        db.session.execute(
            db.text("CALL finalizar_venta(:idUsuario, :total, @idVenta)"),
            {"idUsuario": current_user.id, "total": total}
        )
        id_venta = db.session.execute(db.text("SELECT @idVenta")).scalar()
        for i in carrito:
            db.session.execute(
                db.text("CALL agregar_detalle_venta(:idVenta, :idProductoBase, :idPresentacion, :cantidad, :precio, :equivalencia)"),
                {
                    "idVenta": id_venta,
                    "idProductoBase": i['idProductoBase'],
                    "idPresentacion": i['id'],
                    "cantidad": i['cantidad'],
                    "precio": i['precio'],
                    "equivalencia": i['equivalencia']
                }
            )

        db.session.commit()
        session['ultimo_ticket'] = {
            "folio": f"TK-{id_venta}",
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "productos": carrito,
            "total": total,
            "cajero": current_user.id
        }
        session.pop('carrito_pos', None)
        flash("Venta realizada con éxito", "success")
        return redirect(url_for('venta.ticket_venta'))

    except Exception as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('venta.punto_venta'))

@venta_bp.route("/ticket")
def ticket_venta():
    ticket = session.get("ultimo_ticket")
    if not ticket:
        return redirect(url_for("venta.punto_venta"))
    return render_template("punto_venta/ticket.html", ticket=ticket)

@venta_bp.route("/limpiar_ticket")
@login_required
@roles_accepted('Mostrador')
def limpiar_ticket(): 
    session.pop('carrito_pos', None)
    return redirect(url_for('venta.punto_venta'))



# --- PEDIDOS EN LÍNEA ---

@venta_bp.route("/pedidos_online", methods=["GET"])
@login_required
@roles_accepted('Mostrador')
def pedidos_online():
    # 1. Traemos los datos (Asegúrate de traer el ID)
    resultados = db.session.execute(db.text("""
        SELECT id, folio, nombreCliente, telefono, fechaRecogida, total, estatus
        FROM pedido
        ORDER BY id DESC
    """)).fetchall()

    pedidos_ol = []
    
    # IMPORTANTE: Estos nombres deben ser iguales a los que mandas en los botones
    estados_config = {
        "Pendiente": ("#F59E0B", "Pendiente"),
        "En preparación": ("#3B82F6", "En preparación"),
        "Listo para recoger": ("#22C55E", "Listo para recoger"),
        "Pagado": ("#10B981", "Pagado")
    }

    for p in resultados:
        productos_db = db.session.execute(db.text("""
            SELECT pr.nombre, dp.cantidad
            FROM detalle_pedido dp
            JOIN presentacion_venta pr ON pr.id = dp.idPresentacion
            WHERE dp.idPedido = :id
        """), {"id": p.id}).fetchall()

        lista_items = [f"{n} x{c}" for n, c in productos_db]
        color, texto = estados_config.get(p.estatus, ("#6B7280", p.estatus))

        pedidos_ol.append({
            "id": p.id,
            "id_formateado": p.folio,
            "cliente": p.nombreCliente,
            "telefono": p.telefono,
            "total": float(p.total) if p.total else 0.0,
            "lista_productos": lista_items,
            "estado_texto": texto,
            "estado_color": color
        })

    return render_template(
        "punto_venta/pedidos_online.html",
        pedidos_ol=pedidos_ol,
        vista='ol'
    )

@venta_bp.route("/cambiar_estado_pedido/<int:pedido_id>/<string:nuevo_estado>", methods=["POST"])
def cambiar_estado_pedido(pedido_id, nuevo_estado):
    try:
        from models import Pedido, DetallePedido, Receta, DetalleReceta, MateriaPrima, presentacionVenta
        import decimal

        pedido = Pedido.query.get_or_404(pedido_id)
        estado_normalizado = nuevo_estado.strip()

        # 1. Lógica de Inventario (Solo al iniciar preparación)
        if estado_normalizado == "En preparación":
            # Recorremos lo que el cliente compró (DetallePedido)
            detalles = DetallePedido.query.filter_by(idPedido=pedido_id).all()
            
            for d in detalles:
                # Accedemos al ID del producto base a través de la presentación
                # En tu modelo es: d.presentacion.idProductoBase
                prod_id = d.presentacion.idProductoBase
                
                # Buscamos la receta asociada a ese producto
                receta = Receta.query.filter_by(idProducto=prod_id).first()
                
                if receta:
                    # Buscamos los insumos de la receta (DetalleReceta)
                    for ing in receta.detalles:
                        # Buscamos la MateriaPrima para restar el stock
                        # En tu modelo DetalleReceta tiene idMateriaPrima
                        mp = MateriaPrima.query.get(ing.idMateriaPrima)
                        if mp:
                            # Calculamos: (cantidad necesaria por receta) * (cuántos compró el cliente)
                            cantidad_a_descontar = decimal.Decimal(ing.cantidad) * decimal.Decimal(d.cantidad)
                            mp.stockActual -= cantidad_a_descontar
                            print(f"DEBUG: Descontando {cantidad_a_descontar} de {mp.nombre}")

        # 2. Actualizamos el estatus del pedido
        pedido.estatus = estado_normalizado
        db.session.commit()
        
        print(f"DEBUG: Pedido {pedido_id} actualizado a {estado_normalizado} con éxito.")

    except Exception as e:
        db.session.rollback()
        print(f"ERROR CRÍTICO EN VENTAS: {e}")
    
    return redirect(url_for('venta.pedidos_online'))