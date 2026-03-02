from flask import Blueprint, render_template, request, redirect, url_for

autenticacion_bp = Blueprint(
    'auth',
    __name__,
    template_folder='templates'
)

@autenticacion_bp.route("/auth", methods=["GET", "POST"])
def auth():
    return render_template("autenticacion/auth.html")