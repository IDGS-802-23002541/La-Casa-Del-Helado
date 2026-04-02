from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# Tabla intermedia para la relación muchos a muchos entre Usuarios y Roles
roles_usuarios = db.Table('roles_usuarios', 
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('rol_id', db.Integer, db.ForeignKey('rol.id'))
)

class Rol(db.Model, RoleMixin):
    __tablename__ = 'rol'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    @property
    def name(self):
        return self.nombre

    @property
    def description(self):
        return ''


class Persona(db.Model):
    __tablename__ = 'persona'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fechaIngreso = db.Column(db.Date, nullable=False)
    estatus = db.Column(db.Boolean, default=True, nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    idRol = db.Column(db.Integer, db.ForeignKey('rol.id'))
    idPersona = db.Column(db.Integer, db.ForeignKey('persona.id'))

    # Relaciones
    rol = db.relationship('Rol', backref='usuarios')
    persona = db.relationship('Persona', backref='usuario')
    compras = db.relationship('Compra', back_populates='usuario')
    ventas = db.relationship('Venta', backref='vendedor')
    
    # Rol secundario para relación muchos a muchos
    roles = db.relationship('Rol', secondary='roles_usuarios', backref='usuarios_sec')

    @property
    def active(self):
        return self.estatus

    @property
    def roles(self):
        return [self.rol] if self.rol else []


class Proveedor(db.Model):
    __tablename__ = 'proveedor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    razonSocial = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    estatus = db.Column(db.String(20), default='Activo')

    # Relaciones
    compras = db.relationship('Compra', back_populates='proveedor')
    materiasPrimas = db.relationship('MateriaPrima', back_populates='proveedor')

    def __repr__(self):
        return f'<Proveedor {self.razonSocial}>'


class Compra(db.Model):
    __tablename__ = 'compra'

    id = db.Column(db.Integer, primary_key=True)
    factura = db.Column(db.String(50))
    fechaCompra = db.Column(db.Date, default=datetime.datetime.now)

    idProveedor = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    # Relaciones
    proveedor = db.relationship('Proveedor', back_populates='compras')
    usuario = db.relationship('Usuario', back_populates='compras')


class Categoria(db.Model):
    __tablename__ = 'categoria'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    # Relaciones
    materiasPrimas = db.relationship('MateriaPrima', back_populates='categoria')
    productos = db.relationship('Producto', backref='categoria_rel')

    def __repr__(self):
        return f'<Categoria {self.nombre}>'


class MateriaPrima(db.Model):
    __tablename__ = 'materia_prima'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    unidadBase = db.Column(db.String(20), nullable=False)

    stockActual = db.Column(db.Numeric(10, 2), default=0)
    stockMinimo = db.Column(db.Numeric(10, 2), nullable=False)

    estatus = db.Column(db.Boolean, default=True)

    idCategoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    idProveedor = db.Column(db.Integer, db.ForeignKey('proveedor.id'))

    # Relaciones
    categoria = db.relationship('Categoria', back_populates='materiasPrimas')
    proveedor = db.relationship('Proveedor', back_populates='materiasPrimas')

    def __repr__(self):
        return f'<MateriaPrima {self.nombre}>'


class Producto(db.Model):
    __tablename__ = 'producto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    unidadBase = db.Column(db.String(20), nullable=False)
    stockActual = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    stockMinimo = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    costoUnitario = db.Column(db.Numeric(10, 2), nullable=False, default=0)

    idCategoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    # Relaciones
    categoria = db.relationship('Categoria', foreign_keys=[idCategoria])


class Venta(db.Model):
    __tablename__ = 'venta'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
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


class SolicitudProduccion(db.Model):
    __tablename__ = 'solicitud_produccion'
    
    id = db.Column(db.Integer, primary_key=True)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # El empleado de mostrador
    cantidad_solicitada = db.Column(db.Integer, nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.datetime.now)
    estatus = db.Column(db.String(50), default='Pendiente') 

    producto = db.relationship('Producto', backref='solicitudes')
    usuario = db.relationship('Usuario', backref='solicitudes_creadas')


class Receta(db.Model):
    __tablename__ = 'receta'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=True)
    cantidadProducida = db.Column(db.Numeric(10, 2), nullable=False)
    estatus = db.Column(db.Boolean, default=True, nullable=False)

    producto = db.relationship('Producto', backref='recetas', passive_deletes=True)
    detalles = db.relationship('DetalleReceta', backref='receta', cascade='all, delete-orphan')


class DetalleReceta(db.Model):
    __tablename__ = 'detalle_receta'

    id = db.Column(db.Integer, primary_key=True)
    idReceta = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable=False)
    idMateriaPrima = db.Column(db.Integer, db.ForeignKey('materia_prima.id'), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    unidad = db.Column(db.String(20), nullable=False)

    materiaPrima = db.relationship('MateriaPrima', foreign_keys=[idMateriaPrima])


class Turno(db.Model):
    __tablename__ = 'turno'
    
    id = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    apertura = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    cierre = db.Column(db.DateTime, nullable=True)