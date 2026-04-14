from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore
from config import DevelopmentConfig
from models import db, Usuario, Rol 
from flask_migrate import Migrate

# Rutas en Blueprint
from proveedores.routes import proveedores
from autenticacion import autenticacion_bp
from dashboard import dash_bp
from inv_producto import prod_bp
from materia_prima import materia_bp
from produccion import produccion_bp
from venta import venta_bp
from recetas import receta_bp
from usuarios import usuarios_bp
from compras import compra_bp
from mermas import merma_bp
from soli_produccion import Soli_Produccion
from venta_cliente import clientes

import logging

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
migrate = Migrate(app, db)

user_datastore = SQLAlchemyUserDatastore(db,Usuario,Rol)
security = Security(app, user_datastore)

# Blueprint register
app.register_blueprint(autenticacion_bp)
app.register_blueprint(dash_bp)
app.register_blueprint(prod_bp)
app.register_blueprint(materia_bp)
app.register_blueprint(produccion_bp)
app.register_blueprint(proveedores)
app.register_blueprint(venta_bp)
app.register_blueprint(receta_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(compra_bp)
app.register_blueprint(merma_bp)
app.register_blueprint(Soli_Produccion)
app.register_blueprint(clientes)


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("inicio.html")

@app.errorhandler(500)
def servidor_error(e):
    return render_template("500.html"), 500

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

@app.errorhandler(403)
def access_denied(e):
	return render_template("403.html"), 403

#Logs
LOG_FILENAME = 'errores.log'

logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run(debug=True)
	LOG_FILENAME = 'errores.log' 

