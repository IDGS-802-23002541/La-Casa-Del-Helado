from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from functools import wraps
from models import db, Pedido, DetallePedido, presentacionVenta
from datetime import datetime, timedelta
import uuid
from decimal import Decimal
from sqlalchemy import text

clientes = Blueprint(
    'venta_cliente',
    __name__,
    template_folder='templates'
)

def cliente_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'cliente_id' not in session:
            flash("Debes iniciar sesión.", "warning")
            return redirect(url_for('clientesOn.login_cliente'))
        return f(*args, **kwargs)
    return decorated_function


HORA_APERTURA = 13   # 1:00 PM
HORA_CIERRE = 19   # 7:00 PM
HORA_CORTE = 18   # 6:00 PM  (último pedido del día — recogida mín. 1h después)

def calcular_fecha_recogida():
    """
    Devuelve el datetime mínimo de recogida válido.
    - Si ahora < 6:00 PM  → hoy, a la hora actual + 1h (mínimo 1:00 PM)
    - Si ahora >= 6:00 PM → mañana a la 1:00 PM
    """
    ahora = datetime.now()
    if ahora.hour < HORA_CORTE:
        propuesta = ahora + timedelta(hours=1)
        apertura_hoy = ahora.replace(hour=HORA_APERTURA, minute=0, second=0, microsecond=0)
        return max(propuesta, apertura_hoy)
    else:
        manana = ahora.date() + timedelta(days=1)
        return datetime(manana.year, manana.month, manana.day, HORA_APERTURA, 0, 0)


def validar_horario_recogida(fecha_recogida_dt):
    """
    Valida que la fecha/hora de recogida elegida por el cliente sea válida:
    - Dentro del horario (1 PM – 7 PM)
    - Con al menos 1h de anticipación desde ahora
    - Máximo 2 días en el futuro
    """
    ahora = datetime.now()
    hora  = fecha_recogida_dt.hour

    if hora < HORA_APERTURA or hora >= HORA_CIERRE:
        return False, "El horario de recogida es de 1:00 PM a 7:00 PM."
    if fecha_recogida_dt < ahora + timedelta(hours=1):
        return False, "El pedido requiere al menos 1 hora de anticipación."
    if fecha_recogida_dt > ahora + timedelta(days=2):
        return False, "Solo puedes programar tu pedido hasta 2 días adelante."
    return True, ""

@clientes.route('/venta_cliente', methods=['GET'])
@cliente_login_required
def venta():
    presentaciones = (
        presentacionVenta.query
        .filter_by(estatus=True)
        .join(presentacionVenta.productoBase)
        .all()
    )
    return render_template(
        'punto_venta/venta_cliente.html',
        presentaciones=presentaciones
    )

@clientes.route('/pedido/crear', methods=['POST'])
@cliente_login_required
def pedido_crear():
    data = request.get_json()
    items    = data.get('items', [])

    if not items:
        return jsonify(ok=False, msg="El carrito está vacío."), 400
    if len(items) > 5:
        return jsonify(ok=False, msg="Máximo 5 productos diferentes por pedido."), 400

    try:
        fecha_recogida_dt = datetime.fromisoformat(data.get('fechaRecogida', ''))
    except (ValueError, TypeError):
        return jsonify(ok=False, msg="Fecha de recogida inválida."), 400

    valido, msg_horario = validar_horario_recogida(fecha_recogida_dt)
    if not valido:
        return jsonify(ok=False, msg=msg_horario), 400

    try:
        folio = f"PED-{uuid.uuid4().hex[:8].upper()}"

        # Crear pedido
        db.session.execute(
            text("CALL crear_pedido(:folio, :idCliente, :fecha, :total)"),
            {
                "folio": folio,
                "idCliente": session.get('cliente_id'),
                "fecha": fecha_recogida_dt,
                "total": 0  # provisional
            }
        )

        # Obtener ID del pedido
        pedido = db.session.execute(
            text("SELECT id FROM pedido WHERE folio = :folio"),
            {"folio": folio}
        ).fetchone()

        id_pedido = pedido[0]
        total = Decimal('0')

        for item in items:
            id_pres  = item.get('idPresentacion')
            cantidad = int(item.get('cantidad', 0))

            if cantidad < 1 or cantidad > 20:
                raise Exception(f"Cantidad inválida para el producto {id_pres}")

            db.session.execute(
                text("CALL agregar_detalle_pedido(:idPedido, :idPres, :cantidad)"),
                {
                    "idPedido": id_pedido,
                    "idPres": id_pres,
                    "cantidad": cantidad
                }
            )

            # Obtener precio para total
            precio = db.session.execute(
                text("SELECT precio FROM presentacion_venta WHERE id = :id"),
                {"id": id_pres}
            ).fetchone()[0]

            total += Decimal(precio) * cantidad

        # Actualizar total
        db.session.execute(
            text("UPDATE pedido SET total = :total WHERE id = :id"),
            {"total": total, "id": id_pedido}
        )

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify(ok=False, msg=str(e)), 500

    return jsonify(ok=True, folio=folio, total=float(total)), 201

@clientes.route('/pedido/pagar', methods=['POST'])
@cliente_login_required
def pedido_pagar():
    data  = request.get_json()
    folio = (data.get('folio') or '').strip()

    try:
        db.session.execute(
            text("CALL pagar_pedido(:folio)"),
            {"folio": folio}
        )
        db.session.commit()

        pedido = db.session.execute(
            text("SELECT ce.nombre, p.fechaRecogida, p.total FROM pedido p join cliente_externo ce on p.idCliente = ce.id WHERE p.folio = :folio"),
            {"folio": folio}
        ).fetchone()

    except Exception as e:
        db.session.rollback()
        return jsonify(ok=False, msg=str(e)), 400

    return jsonify(
        ok=True,
        folio=folio,
        nombreCliente=pedido[0],
        fechaRecogida=pedido[1].strftime('%d/%m/%Y %I:%M %p'),
        total=float(pedido[2])
    ), 200


@clientes.route('/pedido/cancelar', methods=['POST'])
@cliente_login_required
def pedido_cancelar():
    data  = request.get_json()
    folio = (data.get('folio') or '').strip()

    try:
        db.session.execute(
            text("CALL cancelar_pedido(:folio)"),
            {"folio": folio}
        )
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return jsonify(ok=False, msg=str(e)), 400

    return jsonify(ok=True, msg="Pedido cancelado y stock restituido."), 200

@clientes.route('/pedido/pago/<folio>', methods=['GET'])
@cliente_login_required
def pedido_pago(folio):
    pedido = Pedido.query.filter_by(folio=folio).first_or_404()

    # Si ya está pagado o cancelado, no mostrar pantalla de pago
    if pedido.estatus != 'Pago en proceso':
        return redirect(url_for('venta_cliente.venta'))

    return render_template(
        'punto_venta/pago.html',
        pedido=pedido
    )


@clientes.route('/mis_pedidos', methods=['GET'])
@cliente_login_required
def mis_pedidos():
    return render_template('punto_venta/mispedidos.html')