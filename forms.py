from wtforms import Form 
from wtforms import StringField, IntegerField, DateField, EmailField, SelectField, BooleanField, DecimalField

from wtforms import validators 

class LoginForm(Form):
    nombreUsuario = StringField("Nombre Usuario", [
        validators.DataRequired(message="El campo es requerido"), 
    ])
   
    password = StringField("Contraseña", [
        validators.DataRequired(message="El campo es requerido"), 
    ])

class UserForm(Form):

    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"), 
    ])
   
    apellido = StringField("Apellido", [
        validators.DataRequired(message="El campo es requerido"), 
    ])
   
    nombreUsuario = StringField("Nombre Usuario", [
        validators.DataRequired(message="El campo es requerido"), 
    ])
   
    password = StringField("Contraseña", [
        validators.DataRequired(message="El campo es requerido"), 
    ])

    idRol = SelectField("Rol", coerce=int, validators=[
        validators.DataRequired(message="El campo es requerido")
    ])
    estatus = BooleanField("Estatus",[
        validators.DataRequired(message="El campo es requerido")
    ])
    
class RecetaForm(Form):
    
    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"), 
    ])
    
    idProducto = SelectField("Producto", coerce=int, validators=[
        validators.DataRequired(message="El campo es requerido"), 
    ])
    
    cantidadProducida = DecimalField("Cantidad producida", [
        validators.DataRequired(message="El campo es requerido"), 
    ])

    estatus = BooleanField("Estatus")

class ProductoForm(Form):
    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido"), 
    ])
    
    unidadBase = StringField("Unidad Base", [
        validators.DataRequired(message="El campo es requerido"), 
    ])

    stockActual = DecimalField("Stock Actual", [
        validators.DataRequired(message="El campo es requerido"), 
    ])

    stockMinimo = DecimalField("Stock Minimo", [
        validators.DataRequired(message="El campo es requerido"), 
    ])

    costoUnitario = DecimalField("Costo Unitario", [
        validators.DataRequired(message="El campo es requerido"), 
    ])

    idCategoria = SelectField("Categoria", coerce=int, validators=[
        validators.DataRequired(message="El campo es requerido"), 
    ])

