from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, SolicitudProduccion, Producto, Receta, MateriaPrima
from flask_security.decorators import roles_accepted, login_required
import datetime
import decimal

produccion_bp = Blueprint(
    'produccion',
    __name__,
    template_folder='templates'
)

@produccion_bp.route("/produccion")
@login_required
@roles_accepted('Produccion')
def tablero():
    pendientes = SolicitudProduccion.query.filter_by(estatus='Pendiente').all()
    en_proceso = SolicitudProduccion.query.filter_by(estatus='En Proceso').all()
    terminadas = SolicitudProduccion.query.filter_by(estatus='Terminado').all()

    return render_template(
        "produccion/prod.html",
        pendientes=pendientes,
        en_proceso=en_proceso,
        terminadas=terminadas
    )

@produccion_bp.route("/produccion/iniciar/<int:sol_id>", methods=["POST"])
@login_required
@roles_accepted('Produccion')
def iniciar_produccion(sol_id):
    solicitud = SolicitudProduccion.query.get_or_404(sol_id)

    if solicitud.estatus != 'Pendiente':
        flash("La solicitud no se puede iniciar", "warning")
        return redirect(url_for('produccion.tablero'))

    solicitud.estatus = 'En Proceso'
    db.session.commit()

    flash(f"Producción de {solicitud.producto.nombre} iniciada", "success")
    return redirect(url_for('produccion.tablero'))

@produccion_bp.route("/produccion/terminar/<int:sol_id>", methods=["POST"])
@login_required
@roles_accepted('Produccion')
def terminar_produccion(sol_id):
    solicitud = SolicitudProduccion.query.get_or_404(sol_id)

    if solicitud.estatus != 'En Proceso':
        flash("La solicitud no se puede terminar", "warning")
        return redirect(url_for('produccion.tablero'))

    receta = Receta.query.get(solicitud.idReceta)

    if receta:
        for detalle in receta.detalles:
            materia = MateriaPrima.query.get(detalle.idMateriaPrima)

            if materia:
                cantidad_requerida = decimal.Decimal(str(detalle.cantidad)) * decimal.Decimal(str(solicitud.lotes))

                if materia.stockActual < cantidad_requerida:
                    flash(f"No hay suficiente {materia.nombre}", "danger")
                    return redirect(url_for('produccion.tablero'))

                materia.stockActual -= cantidad_requerida

    producto = Producto.query.get(solicitud.idProducto)
    producto.stockActual += decimal.Decimal(str(solicitud.lotes)) * decimal.Decimal(str(receta.cantidadProducida))

    solicitud.estatus = 'Terminado'
    db.session.commit()

    flash(f"Producción de {producto.nombre} terminada y stock actualizado", "success")
    return redirect(url_for('produccion.tablero'))


# @produccion_bp.route("/produccion/materiales")
# def materiales():
#     materias_db = MateriaPrima.query.all()

#     materias_primas = []
#     for mp in materias_db:
#         materias_primas.append({
#             "id": mp.id,
#             "nombre": mp.nombre,
#             "unidadBase": mp.unidadBase,
#             "stockActual": float(mp.stockActual or 0),
#             "stockMinimo": float(mp.stockMinimo or 0),
#             "estatus": mp.estatus,
#             "categoria": {
#                 "id": mp.categoria.id if mp.categoria else None,
#                 "nombre": mp.categoria.nombre if mp.categoria else "Sin categoría"
#             }
#         })

#     return render_template(
#         "produccion/materia_prima.html",
#         materias_primas=materias_primas
#     )
    
