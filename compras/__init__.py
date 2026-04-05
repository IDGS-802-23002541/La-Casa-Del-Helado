from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, Proveedor, Compra, Usuario, MateriaPrima, DetalleCompra
from flask_security import current_user
from sqlalchemy import text
from datetime import datetime
import json
import forms

compra_bp = Blueprint(
    'compra',
    __name__,
    template_folder='templates'
)

@compra_bp.route("/compra", methods=["GET", "POST"])
def compra():
    compras = Compra.query.filter_by(estatus=True).all()
    compra_form = forms.CompraForm(request.form)
    detalle_form = forms.DetalleCompraForm(request.form)

    # Llenar choices dinámicos
    proveedores = Proveedor.query.distinct().all()
    compra_form.idProveedor.choices = [(p.id, p.razonSocial) for p in proveedores]

    materias = MateriaPrima.query.all()
    detalle_form.idMateriaPrima.choices = [('', '— Seleccionar producto —')] + [(m.id, m.nombre) for m in materias]

    # Inicializar sesión para los detalles (el "carrito")
    if "detalles" not in session:
        session["detalles"] = []
    
    # Recuperar persistencia de Factura y Proveedor
    compra_data = session.get("compra_data", {})
    if request.method == "GET":
        compra_form.factura.data = compra_data.get("factura")
        if compra_data.get("idProveedor"):
            compra_form.idProveedor.data = int(compra_data.get("idProveedor"))

    # Variable para mantener presentaciones si hay un error de validación
    presentaciones_render = []
    id_materia_sel = request.form.get("idMateriaPrima")
    if id_materia_sel:
        m_sel = MateriaPrima.query.get(id_materia_sel)
        if m_sel:
            presentaciones_render = PRESENTACIONES_UI.get(m_sel.unidadBase, [])

    if request.method == "POST":
        accion = request.form.get("accion")

        # --- ACCIÓN: AGREGAR PRODUCTO A LA LISTA TEMPORAL ---
        if accion == "agregar_detalle":
            errores = []
            if not detalle_form.idMateriaPrima.data: errores.append("Selecciona una materia prima")
            if not request.form.get("contenidoNeto"): errores.append("Selecciona una presentación")
            if not detalle_form.cantidad.data: errores.append("Ingresa la cantidad")
            if not detalle_form.precio.data: errores.append("Ingresa el precio")

            if errores:
                return render_template(
                    "compras/compraPV.html",
                    compra_form=compra_form,
                    detalle_form=detalle_form,
                    detalles=session.get("detalles"),
                    presentaciones=presentaciones_render,
                    errores_detalle=errores,
                    compras=compras
                )

            # Guardar datos de cabecera en sesión para no reescribirlos
            session["compra_data"] = {
                "factura": request.form.get("factura"),
                "idProveedor": request.form.get("idProveedor")
            }

            detalle_temp = {
                "idMateriaPrima": int(detalle_form.idMateriaPrima.data),
                "nombre": dict(detalle_form.idMateriaPrima.choices).get(int(detalle_form.idMateriaPrima.data)),
                "cantidad": float(detalle_form.cantidad.data),
                "contenidoNeto": request.form.get("contenidoNeto"),
                "precio": float(detalle_form.precio.data)
            }

            detalles = session["detalles"]
            detalles.append(detalle_temp)
            session["detalles"] = detalles
            session.modified = True
            return redirect(url_for("compra.compra"))

        # --- ACCIÓN: GUARDAR COMPRA DEFINITIVA ---
       # --- ACCIÓN: GUARDAR COMPRA DEFINITIVA ---
        if accion == "guardar_compra":
            # 1. Verificamos que haya productos en la sesión
            lista_detalles = session.get("detalles", [])
            if not lista_detalles:
                flash("Agrega al menos un producto antes de guardar", "danger")
                return redirect(url_for("compra.compra"))
            
            # 2. Convertimos a JSON
            detalles_json = json.dumps(lista_detalles)

            try:
                # 3. LLAMADA AL PROCEDIMIENTO ALMACENADO
                # Usamos request.form.get para asegurar que tomamos lo que el usuario escribió
                db.session.execute(
                    text("CALL registrar_compra(:factura, :proveedor, :usuario, :detalles)"),
                    {
                        "factura": request.form.get("factura"),
                        "proveedor": request.form.get("idProveedor"),
                        "usuario": current_user.id if current_user.is_authenticated else 1,
                        "detalles": detalles_json
                    }
                )
                db.session.commit()
                
                # 4. LIMPIEZA TOTAL
                session.pop("detalles", None)
                session.pop("compra_data", None)
                session.modified = True
                
                flash("¡Compra registrada exitosamente!", "success")

            except Exception as e:
                db.session.rollback()
                # Imprime el error en la consola para que veas qué falló en MySQL
                print(f"Error en MySQL: {str(e)}")
                flash(f"Error al registrar en la base de datos: {str(e)}", "danger")

            return redirect(url_for("compra.compra"))

    return render_template(
        "compras/compraPV.html",
        compra_form=compra_form,
        detalle_form=detalle_form,
        detalles=session.get("detalles", []),
        presentaciones=presentaciones_render,
        compras=compras
    )

@compra_bp.route("/get_presentaciones/<int:idMateria>")
def get_presentaciones(idMateria):
    materia = MateriaPrima.query.get(idMateria)
    if not materia:
        return {"error": "Materia no encontrada"}, 404
    opciones = PRESENTACIONES_UI.get(materia.unidadBase, [])
    return {"presentaciones": opciones}

@compra_bp.route("/compra/cancelar", methods=["POST"])
def cancelar_compra():
    session.pop("detalles", None)
    session.pop("compra_data", None)
    return redirect(url_for("compra.compra"))

@compra_bp.route("/compra/eliminar/<int:id>", methods=["POST"])
def eliminar_compra(id):
    compra = Compra.query.get_or_404(id)
    compra.estatus = False
    compra.fechaEliminacion = datetime.now()
    db.session.commit()
    flash("Eliminación completada", "success")
    return redirect(url_for("compra.compra"))

# --- CONFIGURACIÓN DE CONVERSIONES Y UI ---
CONVERSIONES = {
    "Litros": {"ml": 0.001, "L": 1, 
               "galon": 3.785, 
               "medio_galon": 1.892},
    "Kilos": {"g": 0.001, 
              "kg": 1, 
              "500g": 0.5, 
              "250g": 0.25},
    "Piezas": {"unidad": 1, 
               "docena": 12, 
               "caja_12": 12, 
               "caja_24": 24}
}

PRESENTACIONES_UI = {
    "Litros": [
        ("ml", "Mililitros"), ("L", "Litro (1L)"),
        ("galon", "Galón (3.785L)"), ("medio_galon", "Medio galón (1.892L)"),
    ],
    "Kilos": [
        ("g", "Gramos"), ("kg", "Kilogramo (1kg)"),
        ("500g", "Bolsa 500g"), ("250g", "Bolsa 250g"),
    ],
    "Piezas": [
        ("unidad", "Unidad"), ("docena", "Docena (12)"),
        ("caja_12", "Caja 12 piezas"), ("caja_24", "Caja 24 piezas"),
    ]
}