from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Proveedor, Compra, Usuario, MateriaPrima, DetalleCompra
from flask_security import current_user
from flask import session
from datetime import datetime

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

    proveedores = Proveedor.query.distinct().all()
    compra_form.idProveedor.choices = [(p.id, p.razonSocial) for p in proveedores]

    materias = MateriaPrima.query.all()
    detalle_form.idMateriaPrima.choices = [(m.id, m.nombre) for m in materias]

    # Utilizamos sessions para las materias primas
    if "detalles" not in session:
        session["detalles"] = []
    
    compra_data = session.get("compra_data", {})

    compra_form.factura.data = compra_data.get("factura")
    compra_form.idProveedor.data = int(compra_data.get("idProveedor")) if compra_data.get("idProveedor") else None

    if request.method == "POST":

        accion = request.form.get("accion")

        if accion == "agregar_detalle":

            errores = []

            if not detalle_form.idMateriaPrima.data:
                errores.append("Selecciona una materia prima")

            if not request.form.get("contenidoNeto"):
                errores.append("Selecciona una presentación")

            if not detalle_form.cantidad.data:
                errores.append("Ingresa la cantidad")

            if not detalle_form.precio.data:
                errores.append("Ingresa el precio")

            if errores:
                return render_template(
                    "compras/compraPV.html",
                    compra_form=compra_form,
                    detalle_form=detalle_form,
                    detalles=session.get("detalles"),
                    errores_detalle=errores,
                    compras=compras
            )

            session["compra_data"] = {
                "factura": request.form.get("factura"),
                "idProveedor": request.form.get("idProveedor")
            }

            session.modified = True

            detalle_temp = {
                "idMateriaPrima": detalle_form.idMateriaPrima.data,
                "nombre": dict(detalle_form.idMateriaPrima.choices).get(detalle_form.idMateriaPrima.data),
                "cantidad": detalle_form.cantidad.data,
                "contenidoNeto": request.form.get("contenidoNeto"),
                "precio": detalle_form.precio.data
            }

            detalles = session["detalles"]
            detalles.append(detalle_temp)
            session["detalles"] = detalles
            session.modified = True

            return redirect(url_for("compra.compra"))

        if accion == "guardar_compra":

            if not session["detalles"]:
                return "Agrega al menos un producto", 400
            
            detalles_json = json.dumps(session["detalles"])

            compra = Compra(
                factura=compra_form.factura.data,
                idProveedor=compra_form.idProveedor.data,
                idUsuario=1, #current_user.id,
                estatus=True
            )

            db.session.add(compra)
            db.session.flush()

            for d in session["detalles"]:
                detalle = DetalleCompra(
                    idCompra=compra.id,
                    idMateriaPrima=d["idMateriaPrima"],
                    cantidad=d["cantidad"],
                    contenidoNeto=d["contenidoNeto"],
                    precio=d["precio"]
                )

                db.session.add(detalle)

                # Actualizar stock
                materia = MateriaPrima.query.get(d["idMateriaPrima"])
                
                cantidad_convertida = convertir_a_base(
                    d["cantidad"],
                    d["contenidoNeto"],
                    materia.unidadBase
                )

                materia.stockActual += cantidad_convertida

            db.session.commit()

            session.pop("detalles", None)
            session.pop("compra_data", None)
            session.pop("detalles", None)

            return redirect(url_for("compra.compra"))
    return render_template(
        "compras/compraPV.html",
        compra_form=compra_form,
        detalle_form=detalle_form,
        detalles=session["detalles"],
        compras=compras
    )

def convertir_a_base(cantidad, presentacion, unidad_base):
    factor = CONVERSIONES[unidad_base].get(presentacion)

    if not factor:
        raise Exception("Conversión no definida")

    return cantidad * factor

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

    return redirect(url_for("compra.compra"))

CONVERSIONES = {
    "ml": {
        "ml": 1,
        "L": 1000,
        "galon": 3785,
        "medio_galon": 1892,
        "cuarto_galon": 946
    },
    "g": {
        "g": 1,
        "kg": 1000,
        "500g": 500,
        "250g": 250
    },
    "unidad": {
        "unidad": 1,
        "docena": 12,
        "media_docena": 6,
        "caja_12": 12,
        "caja_24": 24
    }
}

PRESENTACIONES_UI = {
    "ml": [
        ("ml", "Mililitros"),
        ("L", "Litro (1L)"),
        ("galon", "Galón (3.785L)"),
        ("medio_galon", "Medio galón (1892L)"),
    ],
    "g": [
        ("g", "Gramos"),
        ("kg", "Kilogramo (1kg)"),
        ("500g", "Bolsa 500g"),
        ("250g", "Bolsa 250g"),
    ],
    "unidad": [
        ("unidad", "Unidad"),
        ("docena", "Docena (12)"),
        ("caja_12", "Caja 12 piezas"),
    ]
}