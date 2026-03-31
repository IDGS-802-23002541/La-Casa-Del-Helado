from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    
class SolicitudProduccion(db.Model):
    __tablename__ = 'solicitudproduccion'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    estatus = db.Column(db.String(20), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    producto = db.relationship('Producto', backref='solicitudes_produccion')

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    unidadBase = db.Column(db.String(20), nullable=False)
    stockActual = db.Column(db.Numeric(10, 2), nullable=False)
    stockMinimo = db.Column(db.Numeric(10, 2), nullable=False)
    idCategoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

class Turno(db.Model):
    __tablename__ = 'turno'
    id = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    apertura = db.Column(db.DateTime, nullable=False, default=datetime.now)
    cierre = db.Column(db.DateTime, nullable=True) 
    ventas = db.relationship('Venta', backref='turno_rel')

class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    idTurno = db.Column(db.Integer, db.ForeignKey('turno.id'), nullable=False)
    detalles = db.relationship('DetalleVenta', backref='venta_rel', cascade="all, delete-orphan")

class DetalleVenta(db.Model):
    __tablename__ = 'detalleventa'
    id = db.Column(db.Integer, primary_key=True)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    idVenta = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    precioUnitario = db.Column(db.Numeric(10, 2), nullable=False)

    producto = db.relationship('Producto')

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    productos = db.relationship('Producto', backref='categoria_rel')
    