from wtforms import Form 
from wtforms import StringField, IntegerField, DateField, EmailField, SelectField, BooleanField, FloatField

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
    
class CompraForm(Form):
    factura = StringField("Factura", [
        validators.DataRequired(message="El campo es requerido"), 
    ])
   
    idProveedor = SelectField("Proveedor", coerce=int, validators=[
        validators.DataRequired(message="Selecciona un proveedor")
    ])

class DetalleCompraForm(Form):
    idMateriaPrima = SelectField("Materia Prima", coerce=int, validators=[
        validators.DataRequired(message="Selecciona una materia prima")
    ])

    cantidad = FloatField("Cantidad", [
        validators.DataRequired(message="El campo es requerido")
    ])

    contenidoNeto = StringField("Contenido Neto")

    precio = FloatField("Precio", [
        validators.DataRequired(message="El campo es requerido")
    ])