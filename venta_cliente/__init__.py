from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from datetime import date

clientes = Blueprint(
    'venta_cliente',
    __name__,
    template_folder='templates'
)

@clientes.route('/venta_cliente', methods=['POST', 'GET'])
def venta_cliente():
    return render_template('punto_venta/venta_cliente.html')