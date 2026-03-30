from flask import Blueprint, render_template, request, redirect,url_for, flash

from models import db, Receta, Producto, DetalleReceta

import forms

receta_bp = Blueprint(
    'recetas',
    __name__,
    template_folder='templates'
)

@receta_bp.route("/recetas", methods=["GET", "POST"])
def index():
    busqueda = request.args.get('busqueda', '')
    query = Receta.query.filter(Receta.estatus == True)

    if busqueda:
        query = query.filter(Receta.nombre.ilike(f'%{busqueda}'))
    
    recetas = query.all()
    return render_template("recetas/recetas.html", recetas=recetas)

@receta_bp.route("/recetas/crear", methods=["GET", "POST"])
def crear():
    form = forms.RecetaForm(request.form)
    form.idProducto.choices = [ (p.id, p.nombre) for p in Producto.query.all()]

    if request.method == 'POST':
        if form.validate():
            receta = Receta (
                nombre = form.nombre.data,
                idProducto = form.idProducto.data,
                cantidadProducida = form.cantidadProducida.data,
                estatus = True
            )
            db.session.add(receta)
            db.session.flush()

            nombres = request.form.getlist('mp_nombre')
            cantidades = request.form.getlist('mp_cantidad')
            unidades = request.form.getlist('mp_unidad')
            ids_mp = request.form.getlist('mp_id')

            for i in range(len(cantidades)):
                if cantidades[i]:
                    detalle = DetalleReceta(
                        idReceta=receta.id,
                        idMateriaPrima=int(ids_mp[i]) if ids_mp[i] else 0,
                        cantidad=cantidades[i],
                        unidad=unidades[i]
                    )
                    db.session.add(detalle)
            db.session.commit()

            flash("Receta creada correctamente")
            return redirect(url_for('recetas.index'))
    return render_template("recetas/crear.html", form=form)






@receta_bp.route("/recetas/detalles", methods=["GET", "POST"])
def detalles():
    id = request.args.get('id')
    receta = Receta.query.filter_by(id=id).first()
    return render_template('recetas/detalles.html', receta=receta)

@receta_bp.route("/recetas/editar", methods=["GET","POST"])
def editar():
    id = request.args.get('id')
    receta = Receta.query.filter_by(id=id).first()
    form = forms.RecetaForm(request.form)
    form.idProducto.choices = [(p.id, p.nombre) for p in Producto.query.all()]

    if request.method == "GET":
        form.nombre.data = receta.nombre
        form.idProducto.data = receta.idProducto
        form.cantidadProducida.data = receta.cantidadProducida
        form.estatus.data = receta.estatus

    if request.method == "POST":
        receta.nombre = form.nombre.data
        receta.idProducto = form.idProducto.data
        receta.cantidadProducida = form.cantidadProducida.data
        receta.estatus = form.estatus.data

        DetalleReceta.query.filter_by(idReceta=receta.id).delete()

        cantidades = request.form.getlist('mp_cantidad')
        unidades = request.form.getlist('mp_unidad')
        ids_mp = request.form.getlist('mp_id')

        for i in range(len(cantidades)):
            if cantidades[i]:
                detalle = DetalleReceta(
                    idReceta=receta.id,
                    idMateriaPrima=int(ids_mp[i]) if ids_mp[i] else 0,
                    cantidad=cantidades[i],
                    unidad=unidades[i]
                )
                db.session.add(detalle)
        db.session.commit()
        flash('Receta actualizada correctamente')
        return redirect(url_for('recetas.index'))

    return render_template("recetas/editar.html", form=form, receta=receta)

@receta_bp.route("/recetas/eliminar", methods=["GET","POST"])
def eliminar():
    id = request.args.get('id')
    receta = Receta.query.filter_by(id=id).first()

    if request.method == "POST":
        receta.estatus = False
        db.session.commit()
        flash("Receta desactivada")
        return redirect(url_for('recetas.index'))

    return render_template("recetas/eliminar.html", receta=receta)