from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig 
from proveedores.routes import proveedores
from models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
app.register_blueprint(proveedores)

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template("inicio.html")

if __name__ == '__main__':
    app.run(debug=True)