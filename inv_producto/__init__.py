from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Producto, Categoria
import forms

prod_bp = Blueprint(
    'producto',
    __name__,
    template_folder='templates'
)

@prod_bp.route("/invproducto", methods=["GET"])
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
    create_from = forms.ProductoForm()
    create_from.idCategoria.choices= [(c.id,c.nombre) for c in Categoria.query.all()]

    if edit_id:
        prod_editar = Producto.query.filter_by(id=edit_id).first()
        create_from.nombre.data = prod_editar.nombre
        create_from.unidadBase.data = prod_editar.unidadBase
        create_from.stockActual.data = prod_editar.stockActual
        create_from.stockMinimo.data = prod_editar.stockMinimo
        create_from.costoUnitario.data = prod_editar.costoUnitario
        create_from.idCategoria.data = prod_editar.idCategoria
    
    productos = query.all()
    categorias = Categoria.query.all()
    total = Producto.query.count()

    return render_template("inv_productos/productos.html", productos=productos, categorias=categorias, total=total,prod_editar=prod_editar,form=create_from,busqueda=busqueda,idCategoria=idCategoria)

@prod_bp.route("/invproducto/crear", methods=["POST"])
def crear():
    create_from = forms.ProductoForm(request.form)
    create_from.idCategoria.choices = [ (c.id, c.nombre) for c in Categoria.query.all()]

    producto = Producto(
        nombre= request.form.get('nombre'),
        unidadBase= request.form.get('unidadBase'),
        stockActual=request.form.get('stockActual'),
        stockMinimo=request.form.get('stockMinimo'),
        costoUnitario=request.form.get('costoUnitario'),
        idCategoria=request.form.get('idCategoria'),
    )
    db.session.add(producto)
    db.session.commit()
    flash('Producto creado correctamente', 'success')
    return redirect(url_for('producto.index'))

@prod_bp.route("/invproducto/editar", methods=["GET", "POST"])
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
    producto.costoUnitario= request.form.get('costoUnitario')
    producto.idCategoria= request.form.get('idCategoria')

    db.session.commit()
    flash('Producto actualizado correctamente', 'success')
    return redirect(url_for('producto.index'))
    
@prod_bp.route("/invproducto/eliminar", methods=["GET", "POST"])
def eliminar():
    id = request.args.get('id')
    producto = Producto.query.filter_by(id=id).first()

    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente')
    return redirect(url_for('producto.index'))
    
