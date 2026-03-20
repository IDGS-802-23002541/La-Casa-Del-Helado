from flask import Blueprint, render_template, request, redirect, url_for

usuarios_bp = Blueprint(
    'usuarios',
    __name__,
    template_folder='templates'
)

@usuarios_bp.route("/usuarios", methods=["GET", "POST"])
def auth():
    return render_template("usuarios/usuarios.html")