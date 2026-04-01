from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db= SQLAlchemy()    

roles_usuarios = db.Table('roles_usuarios', 
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.id'))
)

class Rol(db.Model, RoleMixin):
    __tablename__='rol'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    @property
    def name(self):
        return self.nombre
    @property
    def description(self):
        return ''
    
class Usuario(db.Model, UserMixin):
    __tablename__='usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fechaIngreso = db.Column(db.Date, nullable=False)
    estatus = db.Column(db.Boolean, default=True, nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    ventas = db.relationship('Venta', backref='vendedor')

    idRol = db.Column(db.Integer, db.ForeignKey('rol.id'))

    roles = db.relationship('Rol', secondary='roles_usuarios', backref='usuarios_sec')

    rol = db.relationship('Rol', foreign_keys=[idRol])

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
    
class SolicitudProduccion(db.Model):
    __tablename__ = 'solicitud_produccion'
    id = db.Column(db.Integer, primary_key=True)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False) # El empleado de mostrador
    cantidad_solicitada = db.Column(db.Integer, nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.now)
    estatus = db.Column(db.String(50), default='Pendiente') 

    producto = db.relationship('Producto', backref='solicitudes')
    usuario = db.relationship('Usuario', backref='solicitudes_creadas')

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
    idMateriaPrima = db.Column(db.Integer, db.ForeignKey('materia_prima.id'),nullable=False)
    cantidad = db.Column(db.Numeric(10,2), nullable=False)
    unidad = db.Column(db.String(20), nullable=False)

    materiaPrima = db.relationship('MateriaPrima', foreign_keys=[idMateriaPrima])


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
    fechaCompra=db.Column(db.Date, default=datetime.now)
    idProveedor=db.Column(db.Integer, db.ForeignKey('proveedor.id'))
    idUsuario=db.Column(db.Integer)

    proveedor=db.relationship('Proveedor', foreign_keys=[idProveedor])
    
class MateriaPrima(db.Model): 
    __tablename__ = 'materia_prima'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    unidadBase = db.Column(db.String(20), nullable=False)
    stockActual = db.Column(db.Numeric(10,2), nullable=False, default=0)
    stockMinimo = db.Column(db.Numeric(10,2), nullable=False, default=0)
    idCategoria = db.Column(db.Integer, db.ForeignKey('categoria.id'),nullable=False)

    categoria = db.relationship('Categoria', foreign_keys=[idCategoria])

class Turno(db.Model):
    __tablename__ = 'turno'
    id = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    apertura = db.Column(db.DateTime, nullable=False, default=datetime.now)
    cierre = db.Column(db.DateTime, nullable=True) 

class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
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
    