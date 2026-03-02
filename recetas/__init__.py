from flask import Blueprint, render_template, request, redirect, url_for

receta_bp = Blueprint(
    'recetas',
    __name__,
    template_folder='templates'
)

@receta_bp.route("/recetas", methods=["GET", "POST"])
def auth():
    return render_template("recetas/recetas.html")