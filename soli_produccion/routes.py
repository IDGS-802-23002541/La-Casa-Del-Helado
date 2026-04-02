from flask import render_template, request, redirect, url_for, flash
from models import db, Producto, SolicitudProduccion
from . import Soli_Produccion
from datetime import datetime
from flask_security import login_required, roles_accepted, current_user


@Soli_Produccion.route('/solicitud_produccion', methods=['GET', 'POST'])
# @login_required
# @roles_accepted('Mostrador')
def solicitud_produccion():
    if request.method == 'POST':
        id_prod = request.form.get('idProducto')
        cantidad = request.form.get('cantidad')
        
        if id_prod and cantidad:
            try:
                nueva_solicitud = SolicitudProduccion(
                    fecha_solicitud=datetime.now(), 
                    estatus='Pendiente',
                    idProducto=id_prod,
                    cantidad_solicitada=int(cantidad),
                    idUsuario=current_user.id 
                )
                db.session.add(nueva_solicitud)
                db.session.commit()
                flash("Solicitud enviada a producción correctamente", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error al procesar solicitud: {e}", "error")
            
        return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

    productos = Producto.query.all()
    historial = SolicitudProduccion.query.order_by(SolicitudProduccion.id.desc()).limit(15).all()
    
    return render_template('soli_produccion/solicitudes.html', 
                           productos=productos, 
                           historial=historial)


# Esta es la ruta que "le llega" a producciom. Solo ven lo que falta por hacer.
@Soli_Produccion.route('/panel_produccion')
# @login_required
# @roles_accepted('Produccion')
def panel_produccion():
    # Solo traemos lo que NO está completado
    tareas = SolicitudProduccion.query.filter(SolicitudProduccion.estatus != 'Completada').order_by(SolicitudProduccion.fecha.asc()).all()
    return render_template('soli_produccion/panel_operario.html', tareas=tareas)


# Esta ruta hace la actualizar el inventario automáticamente cuando se marca una tarea como "Completada"
@Soli_Produccion.route('/estatus/actualizar', methods=['POST'])
# @login_required
# @roles_accepted('Produccion')
def actualizar_estatus():
    id_solicitud = request.form.get('id_solicitud')
    nuevo_estatus = request.form.get('nuevo_estatus')

    solicitud = SolicitudProduccion.query.get_or_404(id_solicitud)
    producto = Producto.query.get(solicitud.idProducto)

    try:
        if nuevo_estatus == 'Completada' and solicitud.estatus != 'Completada':
            if producto:
                producto.stockActual += int(solicitud.cantidad)
                flash(f"¡Inventario actualizado! +{solicitud.cantidad} {producto.nombre}", "success")
        
        solicitud.estatus = nuevo_estatus
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}", "error")
        
    return redirect(request.referrer or url_for('SolicitudProduccion.solicitud_produccion'))

@Soli_Produccion.route('/eliminar_historial')
# @login_required
# @roles_accepted('Mostrador')
def eliminar_registro():
    id_reg = request.args.get('id')
    if id_reg:
        registro = SolicitudProduccion.query.get(id_reg)
        if registro:
            db.session.delete(registro)
            db.session.commit()
            flash("Registro eliminado del historial", "info")
    return redirect(url_for('SolicitudProduccion.solicitud_produccion'))