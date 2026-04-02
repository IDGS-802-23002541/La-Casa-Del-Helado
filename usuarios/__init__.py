from flask import Blueprint, render_template, request, redirect, url_for, flash 
from werkzeug.security import generate_password_hash
from models import db, Usuario, Rol
import uuid, forms
from datetime import date
from flask_security.decorators import roles_accepted, login_required

usuarios_bp = Blueprint(
    'usuarios',
    __name__,
    template_folder='templates'
)

@usuarios_bp.route("/usuarios", methods=["GET", "POST"])
# @login_required
# @roles_accepted('Administrador')
def index():
    edit_id = request.args.get('edit', type=int)
    busqueda = request.args.get('busqueda','')
    idRol = request.args.get('idRol', '')
    estatus = request.args.get('estatus', '')

    query = Usuario.query
    if busqueda:
        query = query.filter(
            Usuario.nombre.ilike(f'%{busqueda}%') |
            Usuario.apellido.ilike(f'%{busqueda}%') |
            Usuario.nombreUsuario.ilike(f'%{busqueda}%')
        )
    if idRol:
        query = query.filter(Usuario.idRol == idRol)
    if estatus == 'activo':
        query = query.filter(Usuario.estatus == True)
    elif estatus == 'inactivo':
        query = query.filter(Usuario.estatus == False)

    usr_editar = None
    form = forms.UserForm()
    form.idRol.choices = [ (r.id, r.nombre) for r in Rol.query.all()]

    if edit_id:
        usr_editar = db.session.query(Usuario).filter(Usuario.id == edit_id).first()
        form.nombre.data = usr_editar.nombre
        form.apellido.data = usr_editar.apellido
        form.nombreUsuario.data = usr_editar.nombreUsuario
        form.idRol.data = usr_editar.idRol
        form.estatus.data = usr_editar.estatus

    roles = Rol.query.all()
    usuarios = query.all()
    total = Usuario.query.count()
    activos = Usuario.query.filter_by(estatus=True).count()
    inactivos = Usuario.query.filter_by(estatus=False).count()

    return render_template("usuarios/usuarios.html", roles=roles, usuarios=usuarios, total=total, activos=activos, inactivos=inactivos, usr_editar=usr_editar, busqueda=busqueda, idRol = idRol
    )

@usuarios_bp.route("/usuarios/crear", methods=["POST"])
# @login_required
# @roles_accepted('Administrador','Produccion')
def crear():
    create_from = forms.UserForm(request.form)
    create_from.idRol.choices = [
        (r.id, r.nombre) for r in Rol.query.all()
    ]

    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    nombreUsuario = request.form.get('nombreUsuario')
    password = request.form.get('password')
    idRol = request.form.get('idRol')
    estatus = request.form.get('estatus') == 'true'

    usuario = Usuario(
        nombre=nombre, 
        apellido=apellido,
        nombreUsuario=nombreUsuario, 
        password=generate_password_hash(password),
        fechaIngreso = date.today(),
        estatus=estatus, 
        fs_uniquifier=str(uuid.uuid4()),
        idRol=idRol,
    )
    db.session.add(usuario)
    db.session.commit()

    flash('Usuario creado correctamente', 'success')
    return redirect(url_for('usuarios.index'))

@usuarios_bp.route("/usuarios/editar", methods=["POST"])
# @login_required
# @roles_accepted('Administrador')
def editar():
    id = request.args.get('id')
    usr = db.session.query(Usuario).filter(Usuario.id==id).first()

    usr.nombre = request.form.get('nombre')
    usr.apellido = request.form.get('apellido')
    usr.nombreUsuario = request.form.get('nombreUsuario')
    usr.idRol = request.form.get('idRol')
    usr.estatus = request.form.get('estatus') == 'true'

    password = request.form.get('password')
    if password:
        usr.password = generate_password_hash(password)

    db.session.commit()
    flash('Usuario actualizado correctamente', 'success')
    return redirect(url_for('usuarios.index'))

@usuarios_bp.route("/usuarios/eliminar", methods=["POST"])
# @login_required
# @roles_accepted('Administrador')
def eliminar():
    id = request.args.get('id')
    usr = Usuario.query.get_or_404(id)
    usr.estatus = False
    db.session.commit()
    flash('Usuario desactivado', 'warning')
    return redirect(url_for('usuarios.index'))

