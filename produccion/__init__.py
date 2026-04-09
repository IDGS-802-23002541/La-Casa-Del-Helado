from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, SolicitudProduccion, Producto, Receta, DetalleReceta, MateriaPrima, Usuario
import datetime
import decimal

produccion_bp = Blueprint(
    'produccion',
    __name__,
    template_folder='templates'
)

@produccion_bp.route("/produccion")
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
def iniciar_produccion(sol_id):
    solicitud = SolicitudProduccion.query.get_or_404(sol_id)

    if solicitud.estatus != 'Pendiente':
        flash("La solicitud no se puede iniciar", "warning")
        return redirect(url_for('produccion.tablero'))

    solicitud.estatus = 'En Proceso'
    db.session.commit()

    flash(f"Producción de {solicitud.producto.nombre} iniciada", "success")
    return redirect(url_for('produccion.tablero'))


@produccion_bp.route("/produccion/materiales")
def materiales():
    materias_db = MateriaPrima.query.all()

    materias_primas = []
    for mp in materias_db:
        materias_primas.append({
            "id": mp.id,
            "nombre": mp.nombre,
            "unidadBase": mp.unidadBase,
            "stockActual": float(mp.stockActual or 0),
            "stockMinimo": float(mp.stockMinimo or 0),
            "estatus": mp.estatus,
            "categoria": {
                "id": mp.categoria.id if mp.categoria else None,
                "nombre": mp.categoria.nombre if mp.categoria else "Sin categoría"
            },
            "proveedor": {
                "id": mp.proveedor.id if mp.proveedor else None,
                "razonSocial": mp.proveedor.razonSocial if mp.proveedor else "Sin proveedor"
            }
        })

    return render_template(
        "produccion/materia_prima.html",
        materias_primas=materias_primas
    )

@produccion_bp.route("/produccion/terminar/<int:sol_id>", methods=["POST"])
def terminar_produccion(sol_id):
    solicitud = SolicitudProduccion.query.get_or_404(sol_id)
    print(f"\n>>> INICIANDO TERMINACIÓN: Solicitud ID {sol_id} para Producto ID {solicitud.idProducto}")

    if solicitud.estatus != 'En Proceso':
        flash("La solicitud no está en proceso", "warning")
        return redirect(url_for('produccion.tablero'))

    # Buscamos la receta
    receta = Receta.query.filter_by(idProducto=solicitud.idProducto).first()

    if not receta:
        print(f">>> ERROR: No se encontró receta para el producto {solicitud.idProducto}")
        flash(f"No hay receta para {solicitud.producto.nombre}", "danger")
        return redirect(url_for('produccion.tablero'))

    print(f">>> RECETA ENCONTRADA: {receta.nombre}. Cantidad de ingredientes: {len(receta.detalles)}")

    try:
        # Iniciamos el ciclo de descuento
        for detalle in receta.detalles:
            materia = MateriaPrima.query.get(detalle.idMateriaPrima)
            
            if materia:
                # CÁLCULO DE PROPORCIÓN (Importante: usamos cantidadProducida de la receta)
                # Si tu receta rinde 10 litros y usas 5kg, por cada 1 litro usas 0.5kg
                proporcion = decimal.Decimal(str(detalle.cantidad)) / decimal.Decimal(str(receta.cantidadProducida))
                cantidad_a_descontar = proporcion * decimal.Decimal(str(solicitud.cantidad_solicitada))

                print(f">>> DESCONTANDO: {materia.nombre} | Actual: {materia.stockActual} | Restando: {cantidad_a_descontar}")
                
                # RESTA FÍSICA EN EL OBJETO
                materia.stockActual = decimal.Decimal(str(materia.stockActual)) - cantidad_a_descontar
            else:
                print(f">>> ERROR: No se encontró la materia prima con ID {detalle.idMateriaPrima}")

        # SUMAR AL STOCK DEL PRODUCTO TERMINADO
        producto = Producto.query.get(solicitud.idProducto)
        if producto:
            producto.stockActual = decimal.Decimal(str(producto.stockActual or 0)) + decimal.Decimal(str(solicitud.cantidad_solicitada))
            print(f">>> PRODUCTO ACTUALIZADO: {producto.nombre} nuevo stock: {producto.stockActual}")

        # CAMBIAR ESTATUS
        solicitud.estatus = 'Terminado'
        
        # EL PASO FINAL: GUARDAR TODO
        print(">>> INTENTANDO HACER COMMIT A LA BASE DE DATOS...")
        db.session.commit()
        print(">>> COMMIT EXITOSO.")
        
        flash(f"Producción terminada e inventarios actualizados", "success")

    except Exception as e:
        db.session.rollback()
        print(f">>> ¡ERROR CRÍTICO!: {str(e)}")
        flash(f"Error en el proceso: {str(e)}", "danger")

    return redirect(url_for('produccion.tablero'))