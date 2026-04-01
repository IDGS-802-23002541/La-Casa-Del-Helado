from flask import Blueprint

Soli_Produccion = Blueprint(
    'SolicitudProduccion', 
    __name__, 
    template_folder='templates')

from . import routes