from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Proveedor

proveedores = Blueprint('proveedores', __name__)

@proveedores.route('/proveedores')
def proveedoresTabla():
    busqueda = request.args.get('q', '')
    estatus_filtro = request.args.get('estatus', '')
    query = Proveedor.query
    if busqueda:
        query = query.filter(Proveedor.razonSocial.contains(busqueda))
    if estatus_filtro:
        query = query.filter(Proveedor.estatus == estatus_filtro)   
    lista = enriquecer(query.order_by(Proveedor.razonSocial).all())
    total = len(lista)
    return render_template("proveedores/proveedores.html",proveedores=lista, total=total,busqueda=busqueda, 
                           estatus_activo=estatus_filtro)

@proveedores.route("/proveedorDetalles")
def proveedorDetalles():
    id_proveedor = request.args.get('id', type=int)
    proveedor = Proveedor.query.get_or_404(id_proveedor)
    return render_template("proveedores/proveedores.html", proveedor=proveedor, modo="detalles")

@proveedores.route("/proveedorNuevo", methods=["GET", "POST"])
def proveedorNuevo():
    if request.method == "POST":
        razon     = request.form.get('razonSocial')
        correo    = request.form.get('correo')
        telefono  = request.form.get('telefono')
        direccion = request.form.get('direccion')
        estatus   = request.form.get('estatus', 'Activo')
        if not razon or not correo or not telefono or not direccion:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for('proveedores.proveedoresTabla'))
        if Proveedor.query.filter_by(correo=correo).first():
            flash("El correo ya existe", "error")
            return redirect(url_for('proveedores.proveedoresTabla'))
        try:
            nuevo = Proveedor( razonSocial=razon,correo=correo,telefono=telefono,direccion=direccion,estatus=estatus)
            db.session.add(nuevo)
            db.session.commit()
            flash("Proveedor registrado correctamente", "success")
            return redirect(url_for('proveedores.proveedoresTabla'))
        except:
            db.session.rollback()
            flash("Error al guardar proveedor", "error")
            return redirect(url_for('proveedores.proveedoresTabla'))
            
    return redirect(url_for('proveedores.proveedoresTabla'))

@proveedores.route("/proveedorModificar", methods=["GET", "POST"])
def proveedorModificar():
    id_proveedor = request.args.get('id', type=int)
    proveedor = Proveedor.query.get_or_404(id_proveedor)
    if request.method == "POST":
        correo = request.form.get('correo')
        if Proveedor.query.filter(Proveedor.correo == correo, Proveedor.id != proveedor.id).first():
            flash("El correo ya existe", "error")
            return redirect(url_for('proveedores.proveedoresTabla'))
        proveedor.razonSocial = request.form.get('razonSocial')
        proveedor.correo      = correo
        proveedor.telefono    = request.form.get('telefono')
        proveedor.direccion   = request.form.get('direccion')
        proveedor.estatus     = request.form.get('estatus')
        db.session.commit()
        flash("Proveedor actualizado", "success")
        return redirect(url_for('proveedores.proveedoresTabla'))
    
    # Para editar, volvemos a cargar la tabla pero pasando el objeto 'proveedor' para el panel
    lista = enriquecer(Proveedor.query.order_by(Proveedor.razonSocial).all())
    return render_template("proveedores/proveedores.html", proveedores=lista, proveedor=proveedor, modo="editar")

@proveedores.route("/proveedorEliminar", methods=["GET", "POST"])
def proveedorEliminar():
    id_proveedor = request.args.get('id', type=int)
    proveedor = Proveedor.query.get_or_404(id_proveedor)

    if request.method == "POST":
        db.session.delete(proveedor)
        db.session.commit()
        flash("Proveedor eliminado", "success")
        return redirect(url_for('proveedores.proveedoresTabla'))
        
    return render_template("proveedores/proveedores.html", proveedor=proveedor, modo="eliminar")

@proveedores.route("/proveedorToggle", methods=["POST"])
def proveedorToggle():
    id_proveedor = request.form.get('id', type=int)
    proveedor = Proveedor.query.get_or_404(id_proveedor)
    proveedor.estatus = 'Inactivo' if proveedor.estatus == 'Activo' else 'Activo'
    db.session.commit()
    flash(f"Estado cambiado a {proveedor.estatus}", "success")
    return redirect(url_for('proveedores.proveedoresTabla'))

# ── COLORES AVATAR ────────
AVATAR_COLORES = [
    'linear-gradient(135deg,#F4A4A4,#E8756A)',
    'linear-gradient(135deg,#B8EDE4,#5CC8BC)',
    'linear-gradient(135deg,#E8D5F5,#9B72CF)',
    'linear-gradient(135deg,#FFF3C4,#D4956A)',
    'linear-gradient(135deg,#C8E8FF,#5BA8D8)',]
def enriquecer(lista):
    for i, p in enumerate(lista):
        p.avatar_color = AVATAR_COLORES[i % len(AVATAR_COLORES)]
    return lista