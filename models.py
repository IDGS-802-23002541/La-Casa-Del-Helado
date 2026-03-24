from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy

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

    roles = db.relationship('Rol', foreign_keys=[idRol], viewonly=True)

    @property
    def roles(self):
        return [self.rol] if self.rol else []
    
    @property
    def active(self):
        return self.estatus
    
