from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import text
from models import db, Producto, Receta, SolicitudProduccion
from . import Soli_Produccion
from flask_security import login_required, roles_accepted, current_user


#  crear solicitud 
@Soli_Produccion.route('/solicitud_produccion', methods=['GET', 'POST'])
@login_required
@roles_accepted('Mostrador', 'Administrador')
def solicitud_produccion():
    if request.method == 'POST':
        id_receta = request.form.get('idReceta')
        lotes     = request.form.get('lotes', 1)

        if not all([id_receta, lotes]):
            flash("Completa todos los campos", "error")
            return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

        try:
            # El SP toma idProducto de la receta internamente,
            # pero lo necesitamos para pasarlo — lo sacamos de la receta
            receta = Receta.query.get(int(id_receta))
            if not receta:
                flash("Receta no encontrada", "error")
                return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

            db.session.execute(text("""
                CALL crear_solicitud_produccion(
                    :idProducto, :idReceta, :lotes, :idUsuario, @resultado
                )
            """), {
                'idProducto': receta.idProducto,
                'idReceta':   int(id_receta),
                'lotes':      int(lotes),
                'idUsuario':  current_user.id
            })
            db.session.commit()
            flash("Solicitud enviada a producción ✔", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear solicitud: {e}", "error")

        return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

    recetas = Receta.query.filter_by(estatus=True).order_by(Receta.nombre).all()

    historial = (SolicitudProduccion.query
                 .filter_by(idUsuario=current_user.id)
                 .order_by(SolicitudProduccion.id.desc())
                 .limit(20).all())

    return render_template('soli_produccion/solicitudes.html',
                           recetas=recetas,
                           historial=historial)

# recetas por producto 
@Soli_Produccion.route('/recetas/por_producto/<int:id_producto>')
@login_required
def recetas_por_producto(id_producto):
    recetas = (Receta.query
               .filter_by(idProducto=id_producto, estatus=True)
               .all())
    return {
        'recetas': [
            {
                'id':       r.id,
                'nombre':   r.nombre,
                'cantidad': float(r.cantidadProducida)
            }
            for r in recetas
        ]
    }


#  ver tareas pendientes
@Soli_Produccion.route('/panel_produccion')
@login_required
@roles_accepted('Produccion', 'Administrador')
def panel_produccion():
    tareas = (SolicitudProduccion.query
              .filter(SolicitudProduccion.estatus != 'Completada')
              .order_by(SolicitudProduccion.fecha_solicitud.asc())
              .all())
    return render_template('soli_produccion/panel_operario.html', tareas=tareas)


# iniciar (Pendiente → En Proceso)
@Soli_Produccion.route('/produccion/iniciar', methods=['POST'])
@login_required
@roles_accepted('Produccion', 'Administrador')
def iniciar_produccion():
    id_solicitud = request.form.get('id_solicitud')

    solicitud = SolicitudProduccion.query.get(id_solicitud)
    if not solicitud:
        flash("Solicitud no encontrada", "error")
        return redirect(url_for('SolicitudProduccion.panel_produccion'))

    try:
        db.session.execute(
            text("CALL iniciar_produccion(:id)"),
            {'id': int(id_solicitud)}
        )
        db.session.commit()
        flash(f"Producción iniciada — materia prima apartada ✔", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"No se pudo iniciar: {e}", "error")

    return redirect(url_for('SolicitudProduccion.panel_produccion'))


# completar (En Proceso → Completada
@Soli_Produccion.route('/produccion/completar', methods=['POST'])
@login_required
@roles_accepted('Produccion', 'Administrador')
def completar_produccion():
    id_solicitud = request.form.get('id_solicitud')

    solicitud = SolicitudProduccion.query.get(id_solicitud)
    if not solicitud:
        flash("Solicitud no encontrada", "error")
        return redirect(url_for('SolicitudProduccion.panel_produccion'))

    try:
        db.session.execute(
            text("CALL completar_produccion(:id)"),
            {'id': int(id_solicitud)}
        )
        db.session.commit()
        flash(f"¡Producción completada! Stock actualizado ✔", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"No se pudo completar: {e}", "error")

    return redirect(url_for('SolicitudProduccion.panel_produccion'))


# eliminar del historial (solo Pendientes)
@Soli_Produccion.route('/eliminar_historial')
@login_required
@roles_accepted('Administrador')
def eliminar_registro():
    id_reg = request.args.get('id')
    if not id_reg:
        return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

    registro = SolicitudProduccion.query.get(id_reg)
    if not registro:
        flash("Registro no encontrado", "error")
        return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

    if registro.estatus != 'Pendiente':
        flash("Solo puedes eliminar solicitudes que aún no han iniciado", "error")
        return redirect(url_for('SolicitudProduccion.solicitud_produccion'))

    try:
        db.session.delete(registro)
        db.session.commit()
        flash("Registro eliminado", "info")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar: {e}", "error")

    return redirect(url_for('SolicitudProduccion.solicitud_produccion'))