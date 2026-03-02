from flask import Blueprint, render_template, request, redirect, url_for

dash_bp = Blueprint(
    'dash',
    __name__,
    template_folder='templates'
)

@dash_bp.route("/dash", methods=["GET", "POST"])
def auth():
    return render_template("dashboard/dash.html")