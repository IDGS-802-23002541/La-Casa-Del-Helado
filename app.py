from flask import Flask, render_template
from flask import flash
from autenticacion import autenticacion_bp
from dashboard import dash_bp
from finanzas import finanzas_bp
from inv_producto import prod_bp
from materia_prima import materia_bp
from produccion import produccion_bp
from proveedores import proveedores_bp
from venta import venta_bp
from recetas import receta_bp
from usuarios import usuarios_bp

app = Flask(__name__)
app.register_blueprint(autenticacion_bp)
app.register_blueprint(dash_bp)
app.register_blueprint(finanzas_bp)
app.register_blueprint(prod_bp)
app.register_blueprint(materia_bp)
app.register_blueprint(produccion_bp)
app.register_blueprint(proveedores_bp)
app.register_blueprint(venta_bp)
app.register_blueprint(receta_bp)
app.register_blueprint(usuarios_bp)



@app.route("/", methods=['POST', 'GET'])
def index():
	return render_template("inicio.html")

if __name__ == '__main__':
	app.run(debug=True)