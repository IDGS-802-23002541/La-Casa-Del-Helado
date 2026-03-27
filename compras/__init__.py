from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Proveedor, Compra, Usuario 

compra_bp = Blueprint(
    'compra',
    __name__,
    template_folder='templates'
)

@compra_bp.route("/compra", methods=["GET", "POST"])
def auth():
    
    return render_template("compras/compraPV.html")