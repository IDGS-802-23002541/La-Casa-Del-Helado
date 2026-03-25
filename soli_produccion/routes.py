from flask import session, request, redirect, url_for, render_template, flash
from models import Producto, db, SolicitudProduccion
from datetime import datetime
from . import Soli_Produccion

@Soli_Produccion.route('/solicitud_produccion')
def solicitud_produccion():
    productos = Producto.query.all()
    if 'carrito_produccion' not in session:
        session['carrito_produccion'] = []
        
    return render_template('soli_produccion/solicitudes.html', 
                           productos=productos, 
                           carrito_produccion=session['carrito_produccion'],
                           current_user=current_user) 

@Soli_Produccion.route('/agregar_item', methods=['POST'])
def agregar_item():
    id_prod = request.form.get('idProducto')
    sabor = request.form.get('sabor')
    cantidad = request.form.get('cantidad')
    
    producto_db = Producto.query.get(id_prod)
    
    if producto_db:
        nuevo_item = {
            'id_prod': id_prod,
            'nombre_prod': producto_db.nombre,
            'sabor': sabor,
            'cantidad': cantidad
        }
        
        carrito = session.get('carrito_produccion', [])
        carrito.append(nuevo_item)
        session['carrito_produccion'] = carrito
        session.modified = True 
        
    return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

@Soli_Produccion.route('/quitar_item/<int:index>')
def quitar_item(index):
    carrito = session.get('carrito_produccion', [])
    if 0 <= index < len(carrito):
        carrito.pop(index)
        session['carrito_produccion'] = carrito
        session.modified = True
    return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

@Soli_Produccion.route('/limpiar_carrito')
def limpiar_carrito():
    session.pop('carrito_produccion', None)
    return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

@Soli_Produccion.route('/finalizar_solicitud', methods=['POST'])
def finalizar_solicitud():
    carrito = session.get('carrito_produccion', [])
    
    if not carrito:
        flash("No hay productos para enviar", "error")
        return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

    try:
        for item in carrito:
            nueva_soli = SolicitudProduccion(
                fecha=datetime.now(),
                estatus='Pendiente',
                idProducto=item['id_prod'],
                cantidad=item['cantidad']
            )
            db.session.add(nueva_soli)
        
        db.session.commit()
        session.pop('carrito_produccion', None) 
        flash("¡Solicitud enviada a producción con éxito!", "success")
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error al guardar: {str(e)}", "error")
        
    return redirect(url_for('SolicitudProduccion.solicitud_produccion'))