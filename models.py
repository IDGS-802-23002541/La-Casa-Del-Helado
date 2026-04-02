from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Rol(db.Model, RoleMixin):
    __tablename__ = 'rol'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    @property
    def name(self):
        return self.nombre


class Persona(db.Model):
    __tablename__ = 'persona'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'

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

    compras = db.relationship('Compra', back_populates='usuario')

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

    proveedor = db.relationship('Proveedor', back_populates='compras')
    usuario = db.relationship('Usuario', back_populates='compras')


class Categoria(db.Model):
    __tablename__ = 'categoria'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    materiasPrimas = db.relationship('MateriaPrima', back_populates='categoria')

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

    categoria = db.relationship('Categoria', back_populates='materiasPrimas')
    proveedor = db.relationship('Proveedor', back_populates='materiasPrimas')

    def __repr__(self):
        return f'<MateriaPrima {self.nombre}>'