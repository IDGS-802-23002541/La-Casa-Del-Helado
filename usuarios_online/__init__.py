from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, ClienteExterno  
from datetime import datetime
import random
# Importamos Message de flask_mail (asegúrate de tenerlo configurado en app.py)
from flask_mail import Message 

clientesOn = Blueprint('clientesOn', __name__, template_folder='templates')

@clientesOn.route('/login_cliente', methods=['GET', 'POST'])
def login_cliente():
    if request.method == 'POST':
        correo = request.form.get('txtCorreo')
        password = request.form.get('txtPassword')

        cliente = ClienteExterno.query.filter_by(correo=correo, estatus=True).first()

        if cliente and check_password_hash(cliente.password, password):
            # 1. Generar código de seguridad
            codigo_2fa = str(random.randint(100000, 999999))
            
            # 2. Guardar datos temporales (ID y Nombre)
            session['temp_cliente_id'] = cliente.id
            session['temp_cliente_nombre'] = cliente.nombre # Guardamos el nombre para el saludo
            session['codigo_2fa'] = codigo_2fa
            
            # 3. ENVIAR CORREO (Usando su nombre)
            try:
                from app import mail 
                msg = Message(
                    subject="Tu código de acceso - La Casa del Helado",
                    sender="tu_correo@gmail.com",
                    recipients=[cliente.correo]
                )
                # Personalizamos el mensaje con su nombre
                msg.body = f"¡Hola {cliente.nombre}!\n\nTu código de verificación para entrar a La Casa del Helado es: {codigo_2fa}\n\nSi no fuiste tú, ignora este mensaje."
                mail.send(msg)
                
                flash(f"¡Hola {cliente.nombre}! Enviamos un código a tu correo.", "info")
                return redirect(url_for('clientesOn.verificar_2fa'))
            
            except Exception as e:
                print(f"Error de envío: {e}")
                # Si falla el correo, lo imprimimos en consola para que no te quedes trabada
                print(f"DEBUG: Código para {cliente.nombre} es {codigo_2fa}")
                flash("Hubo un problema al enviar el correo, revisa la terminal.", "warning")
                return redirect(url_for('clientesOn.verificar_2fa'))
        else:
            flash("Credenciales incorrectas.", "danger")

    return render_template('security/login_cliente.html')

@clientesOn.route('/verificar_2fa', methods=['GET', 'POST'])
def verificar_2fa():
    # Usamos el nombre temporal para el saludo en la pantalla
    nombre_usuario = session.get('temp_cliente_nombre', 'Cliente')

    if 'temp_cliente_id' not in session:
        return redirect(url_for('clientesOn.login_cliente'))

    if request.method == 'POST':
        codigo_user = request.form.get('txtCodigo')
        if codigo_user == session.get('codigo_2fa'):
            # Login definitivo
            session['cliente_id'] = session.pop('temp_cliente_id')
            session['cliente_nombre'] = session.pop('temp_cliente_nombre')
            session.pop('codigo_2fa')
            
            flash(f"¡Bienvenido de nuevo, {session['cliente_nombre']}!", "success")
            return redirect(url_for('venta_cliente.venta'))
        else:
            flash("El código no coincide.", "danger")

    return render_template('security/verificar_2fa.html', nombre=nombre_usuario)

@clientesOn.route('/registro_cliente', methods=['GET', 'POST'])
def registro_cliente():
    if request.method == 'POST':
        nombre = request.form.get('txtNombre')
        apellido = request.form.get('txtApellido')  
        correo = request.form.get('txtCorreo')    
        telefono = request.form.get('txtTelefono')
        password = request.form.get('txtPassword')

        existe = ClienteExterno.query.filter_by(correo=correo).first()
        if existe:
            flash("Este correo ya está registrado.", "warning")
            return redirect(url_for('clientesOn.registro_cliente'))

        try:
            nuevo_cliente = ClienteExterno(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                telefono=telefono,
                password=generate_password_hash(password),
                fechaRegistro=datetime.now(),
                estatus=True
            )

            db.session.add(nuevo_cliente)
            db.session.commit()

            flash("¡Registro exitoso! Ya puedes entrar.", "success")
            return redirect(url_for('clientesOn.login_cliente'))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar: {str(e)}", "danger")

    return render_template('usuarios_online/registroUsuarios.html')


@clientesOn.route('/logout_cliente')
def logout_cliente():
    session.clear() 
    flash("Has cerrado sesión.", "info")
    return redirect(url_for('clientesOn.login_cliente'))
