from flask import Blueprint, render_template, request, redirect, url_for

prod_bp = Blueprint(
    'producto',
    __name__,
    template_folder='templates'
)

@prod_bp.route("/invproducto", methods=["GET", "POST"])
def auth():
    return render_template("inv_productos/productos.html")