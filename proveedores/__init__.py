from flask import Blueprint, render_template, request, redirect, url_for

proveedores_bp = Blueprint(
    'proveedores',
    __name__,
    template_folder='templates'
)

@proveedores_bp.route("/proveedores", methods=["GET", "POST"])
def auth():
    return render_template("proveedores/proveedores.html")