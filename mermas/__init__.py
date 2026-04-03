from flask import Blueprint, render_template, request, redirect, url_for
from models import db, MateriaPrima, Usuario, Producto, Merma
from flask_security import current_user
from flask import flash
from sqlalchemy import text
from datetime import datetime

import forms

merma_bp = Blueprint(
    'merma',
    __name__,
    template_folder='templates'
)

@merma_bp.route('/merma', methods=["GET", "POST"])
def merma():
    mermas = Merma.query.filter_by(estatus=True).all()
    merma_form = forms.MermaForm(request.form)

    materias = MateriaPrima.query.all()
    merma_form.idMateriaPrima.choices = [(0, "Selecciona materia prima")] + [(m.id, m.nombre) for m in materias]


    productos = Producto.query.all()
    merma_form.idProducto.choicess = [(0, "Selecciona producto")] + [(p.id, p.nombre) for p in productos]

    if request.method == "POST" and request.form.get("accion") == "guardar_merma":
        try:
            idMateriaPrima = request.form.get("idMateriaPrima") or None
            idProducto = request.form.get("idProducto") or None
            cantidad = int(request.form.get("cantidad"))
            justificacion = request.form.get("justificacion")

            # convertir a int o None
            idMateriaPrima = int(idMateriaPrima) if idMateriaPrima else None
            idProducto = int(idProducto) if idProducto else None

            db.session.execute(
                text("CALL registrar_merma(:materiaprima, :producto, :cantidad, :justificacion, :user)"),
                {
                    "materiaprima": idMateriaPrima,
                    "producto": idProducto,
                    "cantidad": cantidad,
                    "justificacion": justificacion,
                    "user": 1
                }
            )

            db.session.commit()

            flash("Merma registrada correctamente", "success")

        except Exception as e:
            db.session.rollback()
            # print({str(e)})
            # flash(f"Error: {str(e)}", "error")
            flash(f"Vuelve a intentarlo más tarde", "error")

        return redirect(url_for('merma.merma'))

    return render_template(
        'mermas/merma.html',
        mermas=mermas,
        merma_form=merma_form,
        materias=materias,
        productos=productos
    )

@merma_bp.route("/merma/eliminar/<int:id>", methods=["POST"])
def eliminar_merma(id):
    merma = Merma.query.get_or_404(id)

    merma.estatus = False
    merma.fechaEliminacion = datetime.now()

    db.session.commit()

    flash("Eliminación realizada", "success")

    return redirect(url_for("merma.merma"))
