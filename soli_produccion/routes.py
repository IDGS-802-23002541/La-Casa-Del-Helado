from flask import render_template, request, redirect, url_for, flash
from models import db, SolicitudProduccion, Producto

from . import Soli_Produccion

@Soli_Produccion.route('/solicitud_produccion')
def solicitud_produccion():
   productos_db = Producto.query.all()
   return render_template('soli_produccion/solicitudes.html', productos=productos_db)
