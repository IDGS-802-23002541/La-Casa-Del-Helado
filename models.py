from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
import datetime

db= SQLAlchemy()    

class Rol(db.Model, RoleMixin):
    __tablename__='rol'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    @property
    def name(self):
        return self.nombre
    
class Persona(db.Model):
    __tablename__='persona'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
class Usuario(db.Model, UserMixin):
    __tablename__='usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fechaIngreso = db.Column(db.Date, nullable=False)
    estatus = db.Column(db.Boolean, default=True, nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    idRol = db.Column(db.Integer, db.ForeignKey('rol.id'))
    idPersona = db.Column(db.Integer, db.ForeignKey('persona.id'))

    rol = db.relationship('Rol', backref='usuarios')
    persona = db.relationship('Persona', backref='usuario')

    @property
    def roles(self):
        return [self.rol] if self.rol else []
    
    @property
    def active(self):
        return self.estatus

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

class Receta(db.Model):
    __tablename__ = 'receta'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=True)
    cantidadProducida = db.Column(db.Numeric(10,2), nullable=False)
    estatus = db.Column(db.Boolean, default=True, nullable=False)

    producto = db.relationship('Producto', backref='recetas', passive_deletes=True)
    detalles = db.relationship('DetalleReceta', backref='receta', cascade='all, delete-orphan')

class DetalleReceta(db.Model):
    __tablename__ = 'detalle_receta'

    id = db.Column(db.Integer, primary_key=True)
    idReceta = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable=False)
    idMateriaPrima = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Numeric(10,2), nullable=False)
    unidad = db.Column(db.String(20), nullable=False)

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

class Producto(db.Model): 
    __tablename__ = 'producto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    unidadBase = db.Column(db.String(20), nullable=False)
    stockActual = db.Column(db.Numeric(10,2), nullable=False, default = 0)
    stockMinimo = db.Column(db.Numeric(10,2), nullable=False, default = 0)
    costoUnitario = db.Column(db.Numeric(10,2), nullable=False, default = 0)
    idCategoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    categoria = db.relationship('Categoria', foreign_keys=[idCategoria])

class Compra(db.Model):
    __tablename__='compra'

    id=db.Column(db.Integer, primary_key=True)
    factura=db.Column(db.String(50))
    fechaCompra=db.Column(db.Date, default=datetime.datetime.now)
    idProveedor=db.Column(db.Integer)
    idUsuario=db.Column(db.Integer)

    proveedor=db.relationship('Proveedor', back_populates='compra')
    