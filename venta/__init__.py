from flask import Blueprint, render_template, request, redirect, url_for

venta_bp = Blueprint(
    'venta',
    __name__,
    template_folder='templates'
)

@venta_bp.route("/venta", methods=["GET", "POST"])
def auth():
    return render_template("punto_venta/venta.html")