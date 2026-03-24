from flask import Blueprint, render_template, request, redirect, url_for, flash 
from werkzeug.security import generate_password_hash
from models import db, Usuario, Persona, Rol
import uuid, forms
from datetime import date

usuarios_bp = Blueprint(
    'usuarios',
    __name__,
    template_folder='templates'
)

@usuarios_bp.route("/usuarios", methods=["GET", "POST"])
def index():
    busqueda = request.args.get('busqueda','')
    idRol = request.args.get('idRol', '')

    query = Usuario.query.filter(Usuario.estatus == True)
    if busqueda:
        query = query.join(Persona).filter(
            Persona.nombre.ilike(f'%{busqueda}%') |
            Persona.apellido.ilike(f'%{busqueda}%') |
            Usuario.nombreUsuario.ilike(f'%{busqueda}%')
        )
    if idRol: 
        query = query.filter(Usuario.idRol==idRol)

    roles = Rol.query.all()
    usuario = query.all()
    todos = Usuario.query.all()
    
    return render_template("usuarios/usuarios.html", roles=roles, usuario=usuario, todos=todos)

@usuarios_bp.route("/usuarios/crear", methods=["GET", "POST"])
def crear():
    roles = Rol.query.all()
    create_from = forms.UserForm(request.form)
    create_from.idRol.choices = [
        (r.id, r.nombre) for r in Rol.query.all()
    ]
    if request.method == "POST":
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        nombreUsuario = request.form.get('nombreUsuario')
        password = request.form.get('password')
        idRol = request.form.get('idRol')
        estatus = request.form.get('estatus') == 'true'

        persona = Persona(nombre=nombre, apellido=apellido)
        db.session.add(persona)
        db.session.flush()

        usuario = Usuario(
            nombreUsuario=nombreUsuario, password=generate_password_hash(password),
            fechaIngreso = date.today(),
            estatus=True, 
            fs_uniquifier=str(uuid.uuid4()),
            idRol=idRol,
            idPersona=persona.id
            )
        db.session.add(usuario)
        db.session.commit()

        flash('Usuario creado correctamente')
        return redirect(url_for('usuarios.index'))
    return render_template("usuarios/crear.html", roles=roles, form = create_from)

@usuarios_bp.route("/usuarios/editar", methods=["GET", "POST"])
def editar():
    roles = Rol.query.all()
    usuario = Usuario.query.all()
    create_from = forms.UserForm(request.form)
    create_from.idRol.choices = [
        (r.id, r.nombre) for r in Rol.query.all()
    ]
    if request.method == "GET":
        id = request.args.get('id')
        usr = db.session.query(Usuario).filter(Usuario.id==id).first()
        create_from.nombre.data = usr.persona.nombre
        create_from.apellido.data = usr.persona.apellido
        create_from.nombreUsuario.data = usr.nombreUsuario
        create_from.password.data = usr.password
        create_from.idRol.data = usr.idRol
        create_from.estatus.data = usr.estatus

    if request.method == "POST":

        id = request.args.get('id')
        usr = db.session.query(Usuario).filter(Usuario.id==id).first()

        usr.persona.nombre = create_from.nombre.data
        usr.persona.apellido = create_from.apellido.data
        usr.nombreUsuario = create_from.nombreUsuario.data
        usr.password = create_from.password.data
        usr.idRol = create_from.idRol.data
        usr.estatus = create_from.estatus.data
        db.session.add(usr)
        db.session.commit()
        return redirect(url_for('usuarios.index'))

    return render_template("usuarios/editar.html", roles=roles, form = create_from, usuario=usuario)

@usuarios_bp.route("/usuarios/eliminar", methods=["POST", "GET"])
def eliminar():
    id = request.args.get('id')
    usr = db.session.query(Usuario).filter(Usuario.id==id).first()

    if request.method == "POST":
        usr.estatus = False
        db.session.commit()
        flash('Usuario desactivado')
        return redirect(url_for('usuarios.index'))

    return render_template("usuarios/eliminar.html", usr=usr)
