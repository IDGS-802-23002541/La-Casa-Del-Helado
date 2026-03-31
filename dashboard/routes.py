from flask import render_template
from datetime import datetime
from . import dash_bp 

@dash_bp.route("/dash", methods=["GET", "POST"])
def auth():
    fecha_hoy = datetime.now().strftime('%d de %B %Y')
    return render_template("dashboard/dash.html", fecha_hoy=fecha_hoy)

