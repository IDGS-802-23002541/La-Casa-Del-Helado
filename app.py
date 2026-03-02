from flask import Flask, render_template
from flask import flash
from autenticacion import autenticacion_bp
from dashboard import dash_bp
from finanzas import finanzas_bp

app = Flask(__name__)
app.register_blueprint(autenticacion_bp)
app.register_blueprint(dash_bp)
app.register_blueprint(finanzas_bp)

@app.route("/", methods=['POST', 'GET'])
def index():
	return render_template("inicio.html")

if __name__ == '__main__':
	app.run(debug=True)