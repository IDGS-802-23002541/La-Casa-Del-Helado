from flask import Flask, render_template
from flask_security import Security, SQLAlchemyUserDatastore
from config import DevelopmentConfig
from models import db, Usuario, Rol 

from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig 
from models import db

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

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


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


db.init_app(app)

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("inicio.html")

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run(debug=True)
