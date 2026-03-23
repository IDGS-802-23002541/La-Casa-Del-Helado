<<<<<<< HEAD
from flask import Blueprint, render_template, request, redirect, url_for

proveedores_bp = Blueprint(
    'proveedores',
    __name__,
    template_folder='templates'
)

@proveedores_bp.route("/proveedores", methods=["GET", "POST"])
def auth():
    return render_template("proveedores/proveedores.html")
=======
from flask import Blueprint

proveedores = Blueprint(
    'proveedores', 
    __name__, 
    template_folder='templates'
)

from .routes import proveedores
>>>>>>> 1fd909cfe1d16c14c53fdd72a8e14ae08acb739a
