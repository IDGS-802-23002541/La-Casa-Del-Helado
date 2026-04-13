from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

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

    compras = db.relationship('Compra', back_populates='usuario')

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

    # Relaciones
    producto = db.relationship('Producto', backref='recetas', passive_deletes=True)
    
    # COMBINAMOS LAS DOS LÍNEAS EN UNA SOLA:
    detalles = db.relationship('DetalleReceta', 
                               backref='receta', 
                               lazy='joined', # Cambiamos a 'joined' para que cargue los ingredientes de inmediato
                               cascade='all, delete-orphan')

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
    factura=db.Column(db.String(50), nullable=False)
    fechaCompra=db.Column(db.Date, default=datetime.utcnow)
    idProveedor=db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    idUsuario=db.Column(db.Integer,db.ForeignKey('usuario.id'), nullable=False)
    estatus=db.Column(db.Boolean, default=True)
    fechaEliminacion = db.Column(db.DateTime)

    proveedor = db.relationship('Proveedor', back_populates='compras')
    usuario = db.relationship('Usuario', back_populates='compras')

    detalles_compra = db.relationship('DetalleCompra', back_populates='compra', cascade="all, delete-orphan")
    
class DetalleCompra(db.Model):
    __tablename__='detalle_compra'

    id=db.Column(db.Integer, primary_key=True)
    idCompra=db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    idMateriaPrima=db.Column(db.Integer, db.ForeignKey('materia_prima.id'), nullable=False)
    cantidad=db.Column(db.Numeric(10,2), nullable=False)
    contenidoNeto=db.Column(db.String(20))
    precio=db.Column(db.Numeric(10,2), nullable=False)

    compra = db.relationship('Compra', back_populates='detalles_compra')
    materiaPrima=db.relationship('MateriaPrima', back_populates='detalles_compra')

class MateriaPrima(db.Model):
    __tablename__ = 'materia_prima'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    unidadBase = db.Column(db.String(20), nullable=False)  # kg, litros, piezas
    stockActual = db.Column(db.Numeric(10,2), default=0)
    stockMinimo = db.Column(db.Numeric(10,2), default=0)
    idCategoria=db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    estatus = db.Column(db.Boolean, default=True)

    categoria = db.relationship('Categoria', back_populates='materias_primas')
    detalles_compra = db.relationship('DetalleCompra', back_populates='materiaPrima')
    

    def __repr__(self):
        return f'<MateriaPrima {self.nombre}>'
    
class Categoria(db.Model):
    __tablename__='categoria'

    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100), nullable=False)

    materias_primas=db.relationship('MateriaPrima', back_populates='categoria')

class Merma(db.Model):
    __tablename__ = 'merma'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idMateriaPrima = db.Column(db.Integer, db.ForeignKey('materia_prima.id'), nullable=True)
    idProducto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=True)
    
    cantidad = db.Column(db.Numeric(10,2), nullable=False)
    unidad = db.Column(db.String(20), nullable=False)
    justificacion = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now)

    estatus=db.Column(db.Boolean, default=True)
    fechaEliminacion = db.Column(db.DateTime)

    
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    materia_prima = db.relationship('MateriaPrima', backref='mermas')
    producto = db.relationship('Producto', backref='mermas')
    usuario = db.relationship('Usuario', backref='mermas')

    # Check constraint
    __table_args__ = (
        db.CheckConstraint(
            '(idMateriaPrima IS NOT NULL AND idProducto IS NULL) OR '
            '(idMateriaPrima IS NULL AND idProducto IS NOT NULL)',
            name='check_merma_origen'
        ),
    )


class Turno(db.Model):
    __tablename__ = 'turno'
    id = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    apertura = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cierre = db.Column(db.DateTime, nullable=True) 

class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
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

class presentacionVenta(db.Model):
    __tablename__ = "presentacion_venta"

    id = db.Column(db.Integer, primary_key=True) 
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    idProductoBase = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False) 
    equivalencia = db.Column(db.Numeric(10,4), nullable=False)
    estatus = db.Column(db.Boolean, default=True)

    productoBase = db.relationship('Producto', backref='presentaciones')
    
class Conversion(db.Model):
    __tablename__ = 'conversiones'

    unidadBase = db.Column(db.String(20), primary_key=True)
    presentacion = db.Column(db.String(20), primary_key=True)
    factor = db.Column(db.Numeric(10,2), nullable=False)

    def __repr__(self):
        return f'<Conversion {self.presentacion} -> {self.unidadBase} = {self.factor}>'

class Pedido(db.Model):
    __tablename__ = 'pedido'

    id= db.Column(db.Integer, primary_key=True)
    folio= db.Column(db.String(20), nullable=False, unique=True, default=lambda: f"PED-{uuid.uuid4().hex[:8].upper()}")
    nombreCliente= db.Column(db.String(100), nullable=False)
    telefono= db.Column(db.String(10),  nullable=False)
    fechaPedido= db.Column(db.DateTime, nullable=False, default=datetime.now)
    fechaRecogida= db.Column(db.DateTime, nullable=True)
    estatus= db.Column(db.String(30), nullable=False, default='Pago en proceso')
    total= db.Column(db.Numeric(10, 2), nullable=False)

    detalles = db.relationship('DetallePedido', backref='pedido', cascade='all, delete-orphan')


class DetallePedido(db.Model):
    __tablename__ = 'detalle_pedido'

    id= db.Column(db.Integer, primary_key=True)
    idPedido= db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    idPresentacion= db.Column(db.Integer, db.ForeignKey('presentacion_venta.id'), nullable=False)
    cantidad= db.Column(db.Integer, nullable=False)
    precioUnitario= db.Column(db.Numeric(10, 2), nullable=False)

    presentacion = db.relationship('presentacionVenta')