from flask import Blueprint, render_template, request, redirect, url_for

venta_bp = Blueprint(
    'venta',
    __name__,
    template_folder='templates'
)

from . import routes