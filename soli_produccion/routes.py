from flask import render_template, request, redirect, url_for
from models import db, Producto, SolicitudProduccion
from . import Soli_Produccion
from datetime import datetime

@Soli_Produccion.route('/solicitud_produccion', methods=['GET', 'POST'])
def solicitud_produccion():
    if request.method == 'POST':
        id_prod = request.form.get('idProducto')
        cantidad = request.form.get('cantidad')
        
        if id_prod and cantidad:
            try:
                nueva_solicitud = SolicitudProduccion(
                    fecha=datetime.now().date(),
                    estatus='Pendiente',
                    idProducto=id_prod,
                    cantidad=cantidad
                )
                db.session.add(nueva_solicitud)
                db.session.commit()
            except:
                db.session.rollback()
            
        return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

    productos = Producto.query.all()
    historial = SolicitudProduccion.query.order_by(SolicitudProduccion.id.desc()).limit(5).all()
    
    return render_template('soli_produccion/solicitudes.html', 
                           productos=productos, 
                           historial=historial)

@Soli_Produccion.route('/eliminar_historial')
def eliminar_registro():
    id_reg = request.args.get('id')
    if id_reg:
        registro = SolicitudProduccion.query.get(id_reg)
        if registro:
            try:
                db.session.delete(registro)
                db.session.commit()
            except:
                db.session.rollback()
    return redirect(url_for('SolicitudProduccion.solicitud_produccion'))