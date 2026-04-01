from flask import Blueprint, render_template, request, redirect, url_for, flash
import forms

from flask_security import login_user, logout_user, login_required
from flask_security.decorators import roles_accepted
from werkzeug.security import check_password_hash
from models import db, Usuario, roles_usuarios

autenticacion_bp = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)

@autenticacion_bp.route('/login', methods=['GET'])
def login():
    form = forms.LoginForm()
    return render_template('security/login.html', form=form)

@autenticacion_bp.route('/login', methods=['POST'])
def login_post():
    nombreUsuario = request.form.get('nombreUsuario')
    password = request.form.get('password')

    usuario = Usuario.query.filter_by(nombreUsuario=nombreUsuario).first()

    if not usuario or not check_password_hash(usuario.password, password):
        flash('Usuario y/o contraseña incorrectos')
        return redirect(url_for('auth.login'))
    
    login_user(usuario)

    db.session.execute(
    roles_usuarios.delete().where(roles_usuarios.c.usuario_id == usuario.id)
    )
    if usuario.idRol:
        db.session.execute(
            roles_usuarios.insert().values(usuario_id=usuario.id, rol_id=usuario.idRol)
        )
    db.session.commit()

    nombre_rol = usuario.rol.nombre if usuario.rol else None

    if nombre_rol == 'Administrador':
        return redirect(url_for('usuarios.index'))
    elif nombre_rol == 'Produccion': 
        return redirect(url_for('recetas.index'))
    elif nombre_rol == 'Mostrador': 
        return redirect(url_for('venta.punto_venta'))
    else: 
        flash('Tu usuario no tiene un rol asignado', 'error')
        return redirect(url_for('auth.login'))

@autenticacion_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
