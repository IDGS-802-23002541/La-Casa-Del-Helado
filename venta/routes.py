from flask import render_template, request, redirect, url_for, session, flash
from models import db, Producto, Venta, DetalleVenta, Categoria, presentacionVenta
from . import venta_bp 
from datetime import datetime
from flask_security import login_required, roles_accepted, current_user

@venta_bp.route("/venta", methods=["GET"])
@login_required
@roles_accepted('Mostrador')
def punto_venta():
    vista = 'vd'
    categorias = Categoria.query.all()
    presentaciones = presentacionVenta.query.filter_by(estatus=True).all()
    carrito = session.get('carrito_pos', [])
    total_v = sum(float(item['subtotal']) for item in carrito)
    return render_template("punto_venta/venta.html", 
                           presentaciones=presentaciones, 
                           categorias=categorias, 
                           total=total_v, 
                           carrito=carrito,
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
    total_v = sum(float(item['subtotal']) for item in carrito)
    
    return render_template("punto_venta/venta.html", 
                           presentaciones=presentaciones, 
                           categorias=categorias, 
                           total=total_v, 
                           carrito=carrito,
                           cat_actual=categoria_id,
                           query_actual=busqueda,
                           vista='vd')

@venta_bp.route("/vender_agregar", methods=["POST"])
@login_required
@roles_accepted('Mostrador')
def vender_agregar():
    id_pres = request.form.get('id')

    if not id_pres:
        return redirect(url_for('venta.punto_venta'))
    
    pres = presentacionVenta.query.get_or_404(id_pres)
    # se usa el precio que se registro al momento de crear una presentacion
    precio_unitario = float(pres.precio)
    
    carrito = session.get('carrito_pos', [])
    encontrado = False
    for item in carrito:
        if item['id'] == int(id_pres):
            item['cantidad'] += 1
            item['subtotal'] = float(item['cantidad']) * precio_unitario
            encontrado = True
            break
    
    if not encontrado:
        carrito.append({
            'id': pres.id,
            'nombre':pres.nombre,
            'cantidad': 1,
            'precio': precio_unitario,
            'subtotal': precio_unitario,
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
        total_v = sum(float(item['subtotal']) for item in carrito)
        
        # Registramos la venta vinculada al usuario logueado
        # agregando el uso de procedures
        result = db.session.execute(
            db.text("CALL finalizar_VEnta(:idUsuario, :total, @idVenta)") , {'idUsuario':current_user.id, 'total': total_v}           
        )
        id_venta = db.session.execute(db.text("select @idVenta")).scalar()

        for item in carrito:
            db.session.execute(
                db.text("call agregar_detalle_Venta(:idVenta, :idProductoBase, :idPresentacion, :cantidad, :precio, :equivalencia)"),
                {
                    "idVenta":id_venta,
                    "idProductoBase":item['idProductoBase'],
                    "idPresentacion":item['id'],
                    "cantidad":item['cantidad'],
                    "precio":item['precio'],
                    "equivalencia":item['equivalencia'],
                }
            )
          

        db.session.commit()
        session.pop('carrito_pos', None)
        flash("Venta realizada con éxito", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al procesar la venta: {e}", "error")
        
    return redirect(url_for('venta.punto_venta'))

@venta_bp.route("/limpiar_ticket")
@login_required
@roles_accepted('Mostrador')
def limpiar_ticket(): 
    session.pop('carrito_pos', None)
    return redirect(url_for('venta.punto_venta'))

@venta_bp.route("/pedidos_online", methods=["GET"])
@login_required
@roles_accepted('Mostrador')
def pedidos_online():
    pedidos_ol = [
        {
            'id_formateado': '#PED-0041',
            'cliente': 'Mariana García',
            'telefono': '477 123 4567',
            'lista_productos': ['Cono Doble', 'Paleta de Agua'],
            'estado_texto': 'En preparación',
            'estado_color': '#FB923C'
        },
        {
            'id_formateado': '#PED-0040',
            'cliente': 'Juan P.',
            'telefono': '477 555 0000',
            'lista_productos': ['1 Cono de Nuez'],
            'estado_texto': 'Marcar listo',
            'estado_color': '#10B981'
        }
    ]
    carrito = session.get('carrito_pos', [])
    total_v = sum(float(item.get('subtotal', 0)) for item in carrito)
    return render_template("punto_venta/venta.html", 
                           pedidos_ol=pedidos_ol, 
                           total=total_v, 
                           carrito=carrito, 
                           vista='ol')