from flask import Blueprint, render_template, request, redirect, url_for

produccion_bp = Blueprint(
    'produccion',
    __name__,
    template_folder='templates'
)

@produccion_bp.route("/produccion", methods=["GET", "POST"])
def auth():
    return render_template("produccion/prod.html")