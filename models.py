from flask_sqlalchemy import SQLAlchemy
import datetime 
db = SQLAlchemy()

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    razonSocial = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    estatus = db.Column(db.String(20), default='Activo')

    # compras = db.relationship('Compra', backref='proveedor', lazy=True)

    def __repr__(self):
        return f'<Proveedor {self.razonSocial}>'