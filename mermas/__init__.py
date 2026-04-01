from flask import Blueprint, render_template, request, redirect, url_for
from models import db, MateriaPrima, Usuario, Producto, Merma
from flask_security import current_user
from flask import session
from datetime import datetime

import forms

merma_bp = Blueprint(
    'merma',
    __name__,
    template_folder='templates'
)

@merma_bp.route('/merma', methods=["GET", "POST"])
def merma():
    mermas = Merma.query.all()
    merma_form = forms.MermaForm(request.form)

    materias = MateriaPrima.query.all()
    merma_form.idMateriaPrima.choices = [(m.id, m.nombre) for m in materias]

    productos = Producto.query.all()
    merma_form.idProducto.choices = [(p.id, p.nombre) for p in productos]

    return render_template('mermas/merma.html', mermas=mermas)
