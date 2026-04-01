from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore
from config import DevelopmentConfig
from models import db, Usuario, Rol 

# Rutas en Blueprint
from proveedores.routes import proveedores
from autenticacion import autenticacion_bp
from dashboard import dash_bp
from finanzas import finanzas_bp
from inv_producto import prod_bp
from materia_prima import materia_bp
from produccion import produccion_bp
from venta import venta_bp
from recetas import receta_bp
from usuarios import usuarios_bp
from compras import compra_bp
from soli_produccion import Soli_Produccion

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db,Usuario,Rol)
security = Security(app, user_datastore)

# Blueprint register
app.register_blueprint(autenticacion_bp)
app.register_blueprint(dash_bp)
app.register_blueprint(finanzas_bp)
app.register_blueprint(prod_bp)
app.register_blueprint(materia_bp)
app.register_blueprint(produccion_bp)
app.register_blueprint(proveedores)
app.register_blueprint(venta_bp)
app.register_blueprint(receta_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(compra_bp)
app.register_blueprint(Soli_Produccion)


db.init_app(app)

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("inicio.html")

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run(debug=True)
