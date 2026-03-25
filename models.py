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
    
class SolicitudProduccion(db.Model):
    __tablename__ = 'solicitud_produccion'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    producto = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    estatus = db.Column(db.String(20), default='Pendiente')

    def __repr__(self):
        return f'<SolicitudProduccion {self.producto} - {self.cantidad}>'

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    unidadBase = db.Column(db.String(20), nullable=False)
    stockActual = db.Column(db.Numeric(10, 2), nullable=False)
    stockMinimo = db.Column(db.Numeric(10, 2), nullable=False)
    idCategoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    