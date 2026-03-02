from flask import Blueprint, render_template, request, redirect, url_for

materia_bp = Blueprint(
    'materia',
    __name__,
    template_folder='templates'
)

@materia_bp.route("/materia", methods=["GET", "POST"])
def auth():
    return render_template("materia_prima/materia.html")