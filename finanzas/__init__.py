from flask import Blueprint, render_template, request, redirect, url_for

finanzas_bp = Blueprint(
    'finanzas',
    __name__,
    template_folder='templates'
)

@finanzas_bp.route("/finanzas", methods=["GET", "POST"])
def auth():
    return render_template("finanzas/finanzas.html")