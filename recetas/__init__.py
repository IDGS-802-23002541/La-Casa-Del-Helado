from flask import Blueprint, render_template, request, redirect,url_for, flash
from models import db, Receta, Producto, DetalleReceta, MateriaPrima
from flask_security.decorators import roles_accepted, login_required

import forms

receta_bp = Blueprint(
    'recetas',
    __name__,
    template_folder='templates'
)

@receta_bp.route("/recetas", methods=["GET", "POST"])
@login_required
@roles_accepted('Produccion','Administrador')
def index():
    busqueda = request.args.get('busqueda', '')
    estatus = request.args.get('estatus', '')
    id_sel = request.args.get('id', type=int)

    query = Receta.query

    if estatus == 'inactivo':
        query = query.filter(Receta.estatus == False)
    elif estatus == 'activo':
        query = query.filter(Receta.estatus == True)
    # o todas

    # por nombre
    if busqueda:
        query = query.filter(Receta.nombre.ilike(f'%{busqueda}'))
    
    recetas = query.order_by(Receta.id).all()
    total = query.count()

    receta_sel = None
    if id_sel:
        receta_sel = Receta.query.get(id_sel)

    return render_template("recetas/recetas.html", recetas=recetas, total=total, busqueda=busqueda, estatus=estatus, receta_sel=receta_sel,)

@receta_bp.route("/recetas/crear", methods=["GET", "POST"])
@login_required
@roles_accepted('Administrador')
def crear():
    form = forms.RecetaForm(request.form)
    form.idProducto.choices = [ (p.id, p.nombre) for p in Producto.query.order_by(Producto.nombre).all()]

    materias = MateriaPrima.query.order_by(MateriaPrima.nombre).all()

    if request.method == 'POST':
        
        db.session.execute(
            db.text("CALL crear_receta(:nombre, :idProducto, :cantidad, @id_receta)"),
            {
                'nombre': form.nombre.data,
                'idProducto': form.idProducto.data,
                'cantidad': form.cantidadProducida.data
            }
        )
        id_receta = db.session.execute(db.text("Select @id_receta")).scalar()
        # inserta detalles
        cantidades = request.form.getlist('mp_cantidad')
        ids_mp = request.form.getlist('mp_id')
        unidades = request.form.getlist('mp_unidad')

        for i in range(len(cantidades)):
            if cantidades[i] and ids_mp[i]:
                db.session.execute(
                    db.text("call agregar_detalle_receta(:idReceta,:idMp, :cantidad, :unidad)"),
                    {
                        'idReceta':id_receta,
                        'idMp':ids_mp[i],
                        'cantidad':cantidades[i],
                        'unidad':unidades[i],
                    }
                )

        db.session.execute(
            db.text("call calcular_costo_receta(:idReceta)"),
            {"idReceta":id_receta}
        )

        db.session.commit()
        flash('Receta creada correctamente', 'success')
        return redirect(url_for('recetas.index'))

    return render_template("recetas/crear.html", form=form, materias=materias)

@receta_bp.route("/recetas/editar", methods=["GET", "POST"])
# @login_required
# @roles_accepted('Administrador')
def editar():
    id_rec = request.args.get('id', type=int)
    receta = Receta.query.get_or_404(id_rec)

    create_from = forms.RecetaForm(request.form)
    create_from.idProducto.choices = [(p.id, p.nombre) for p in Producto.query.order_by(Producto.nombre).all()]

    materias = MateriaPrima.query.order_by(MateriaPrima.nombre).all()

    if request.method == "GET":
        create_from.nombre.data = receta.nombre
        create_from.idProducto.data = receta.idProducto
        create_from.cantidadProducida.data = receta.cantidadProducida
        create_from.estatus.data = receta.estatus

    if request.method == "POST":
        receta.nombre = create_from.nombre.data
        receta.idProducto = create_from.idProducto.data
        receta.cantidadProducida = create_from.cantidadProducida.data
        receta.estatus = create_from.estatus.data

        DetalleReceta.query.filter_by(idReceta=receta.id).delete()

        cantidades = request.form.getlist('mp_cantidad')
        unidades = request.form.getlist('mp_unidad')
        ids_mp = request.form.getlist('mp_id')

        for i in range(len(cantidades)):
            if cantidades[i] and ids_mp[i]:
                detalle = DetalleReceta(
                    idReceta = receta.id,
                    idMateriaPrima = int(ids_mp[i]),
                    cantidad = cantidades[i],
                    unidad = unidades[i],
                )
                db.session.add(detalle)

        db.session.commit()
        flash('Receta actualizada correctamente', 'success')
        return redirect(url_for('recetas.index'))
    
    return render_template("recetas/editar.html", form=create_from, receta=receta, materias=materias)

@receta_bp.route("/recetas/eliminar", methods=["POST"])
@login_required
@roles_accepted('Administrador')
def eliminar():
    id_rec = request.args.get('id', type=int)
    receta = Receta.query.get_or_404(id_rec)

    receta.estatus = False
    db.session.commit()
    flash("Receta desactivada correctamente", 'warning')
    return redirect(url_for('recetas.index'))

