from flask import render_template
from datetime import datetime
from . import dash_bp 

from flask_security.decorators import roles_accepted, login_required 

@dash_bp.route("/dash", methods=["GET", "POST"])
@login_required
@roles_accepted('Administrador')
def auth():
    fecha_hoy = datetime.now().strftime('%d de %B %Y')
    return render_template("dashboard/dash.html", fecha_hoy=fecha_hoy)

