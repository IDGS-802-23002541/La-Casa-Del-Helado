from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Producto, Categoria, presentacionVenta
import forms
from flask_security.decorators import roles_accepted, login_required

prod_bp = Blueprint(
    'producto',
    __name__,
    template_folder='templates'
)

@prod_bp.route("/invproducto", methods=["GET"])
@login_required
@roles_accepted('Administrador')
def index():
    
    edit_id = request.args.get('edit', type=int)
    busqueda = request.args.get('busqueda', '')
    idCategoria = request.args.get('idCategoria', '')

    query = Producto.query

    if busqueda:
        query = query.filter(Producto.nombre.ilike(f'%{busqueda}%'))
    if idCategoria:
        query = query.filter(Producto.idCategoria == idCategoria)

    prod_editar = None
    presentaciones = []
    create_from = forms.ProductoForm()
    create_from.idCategoria.choices= [(c.id,c.nombre) for c in Categoria.query.all()]

    if edit_id:
        prod_editar = Producto.query.filter_by(id=edit_id).first()
        create_from.nombre.data = prod_editar.nombre
        create_from.unidadBase.data = prod_editar.unidadBase
        create_from.stockActual.data = prod_editar.stockActual
        create_from.stockMinimo.data = prod_editar.stockMinimo
        create_from.idCategoria.data = prod_editar.idCategoria
        presentaciones = presentacionVenta.query.filter_by(idProductoBase=prod_editar.id).all()
    
    productos = query.all()
    categorias = Categoria.query.all()
    total = Producto.query.count()

    return render_template("inv_productos/productos.html", productos=productos, categorias=categorias, total=total,prod_editar=prod_editar,form=create_from,busqueda=busqueda,idCategoria=idCategoria,presentaciones=presentaciones)

@prod_bp.route("/invproducto/crear", methods=["POST"])
@login_required
@roles_accepted('Administrador')
def crear():
    create_from = forms.ProductoForm(request.form)
    create_from.idCategoria.choices = [ (c.id, c.nombre) for c in Categoria.query.all()]

    producto = Producto(
        nombre= request.form.get('nombre'),
        unidadBase= request.form.get('unidadBase'),
        stockActual=request.form.get('stockActual'),
        stockMinimo=request.form.get('stockMinimo'),
        idCategoria=request.form.get('idCategoria'),
    )
    db.session.add(producto)
    db.session.commit()
    flash('Producto creado correctamente', 'success')
    return redirect(url_for('producto.index'))

@prod_bp.route("/invproducto/editar", methods=["GET", "POST"])
@login_required
@roles_accepted('Administrador')
def editar():
    id = request.args.get('id')
    producto = Producto.query.filter_by(id=id).first()
    categorias = Categoria.query.all()
    create_from = forms.ProductoForm(request.form)
    create_from.idCategoria.choices = [ (c.id, c.nombre) for c in categorias]

    producto.nombre = request.form.get('nombre')
    producto.unidadBase= request.form.get('unidadBase')
    producto.stockActual= request.form.get('stockActual')
    producto.stockMinimo= request.form.get('stockMinimo')
    producto.idCategoria= request.form.get('idCategoria')

    db.session.commit()
    flash('Producto actualizado correctamente', 'success')
    return redirect(url_for('producto.index'))
    
@prod_bp.route("/invproducto/eliminar", methods=["GET", "POST"])
@login_required
@roles_accepted('Administrador')
def eliminar():
    id = request.args.get('id')
    producto = Producto.query.filter_by(id=id).first()

    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('producto.index'))
    
@prod_bp.route("/invproducto/<int:id>/presentaciones/crear", methods=["POST"])
@login_required
@roles_accepted('Administrador')
def crear_presentacion(id):
    form = forms.PresentacionVentaForm(request.form)
    
    nueva = presentacionVenta(
        nombre=form.nombre.data,
        precio=form.precio.data,
        equivalencia=form.equivalencia.data,
        idProductoBase=id,
        estatus=True
    )
    db.session.add(nueva)
    db.session.commit()
    flash('Presentacion agregada correctamente', 'success')
    return redirect(url_for('producto.index', edit=id))

@prod_bp.route("/invproducto/presentaciones/eliminar", methods=["POST"])
@login_required
@roles_accepted('Administrador')
def eliminar_presentacion():
    id = request.args.get('id')
    p = presentacionVenta.query.filter_by(id=id).first()
    id_producto = p.idProductoBase
    db.session.delete(p)
    db.session.commit()
    flash('Presentacion eliminada correctamente','success')
    return redirect(url_for('producto.index', edit=id_producto))

@prod_bp.route("/invproducto/presentaciones/editar", methods=["POST"])
@login_required
@roles_accepted('Administrador')
def editar_presentacion():
    id = request.args.get('id')
    p = presentacionVenta.query.filter_by(id=id).first()
    form = forms.PresentacionVentaForm(request.form)

    p.nombre = form.nombre.data
    p.precio = form.precio.data
    p.equivalencia = form.equivalencia.data

    db.session.commit()
    flash('Presentacion actualizada correctamente', 'success')
    return redirect(url_for('producto.index', edit=p.idProductoBase))





