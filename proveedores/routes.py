from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Proveedor

proveedores = Blueprint('proveedores', __name__, template_folder='templates')

# ── GET /proveedores ─────────────────────────────────────────
@proveedores.route('/proveedores')
def index():
    edit_id        = request.args.get('edit', type=int)
    estatus_activo = request.args.get('estatus', '')
    busqueda       = request.args.get('q', '').strip()

    # Query con filtros opcionales
    query = Proveedor.query

    if estatus_activo in ('Activo', 'Inactivo'):
        query = query.filter_by(estatus=estatus_activo)

    if busqueda:
        query = query.filter(
            Proveedor.razonSocial.ilike(f'%{busqueda}%') |
            Proveedor.correo.ilike(f'%{busqueda}%')
        )

    lista = enriquecer(query.order_by(Proveedor.razonSocial).all())

    # Proveedor que va precargado en el panel derecho
    proveedor_editar = Proveedor.query.get(edit_id) if edit_id else None

    # Stats
    total     = Proveedor.query.count()
    activos   = Proveedor.query.filter_by(estatus='Activo').count()
    inactivos = Proveedor.query.filter_by(estatus='Inactivo').count()

    return render_template(
        'proveedores/proveedores.html',
        proveedores      = lista,
        proveedor_editar = proveedor_editar,
        estatus_activo   = estatus_activo,
        busqueda         = busqueda,
        total            = total,
        activos          = activos,
        inactivos        = inactivos,
        errores          = {},
    )


# ── POST /proveedores/guardar ────────────────────────────────
@proveedores.route('/proveedores/guardar', methods=['POST'])
def guardar():
    prov_id   = request.form.get('id', '0')
    razon     = request.form.get('razonSocial', '').strip()
    correo    = request.form.get('correo', '').strip()
    telefono  = request.form.get('telefono', '').strip()
    direccion = request.form.get('direccion', '').strip()
    estatus   = request.form.get('estatus', 'Activo')
    next_url  = request.form.get('next', url_for('proveedores.index'))

    # ── Validación servidor ──────────────────────────────────
    errores = {}
    if not razon:     errores['razonSocial'] = 'Este campo es obligatorio.'
    if not correo:    errores['correo']      = 'El correo es obligatorio.'
    if not telefono:  errores['telefono']    = 'El teléfono es obligatorio.'
    if not direccion: errores['direccion']   = 'La dirección es obligatoria.'

    if errores:
        # Reconstruir vista mostrando errores y datos que ya escribió el usuario
        lista     = enriquecer(Proveedor.query.order_by(Proveedor.razonSocial).all())
        total     = Proveedor.query.count()
        activos   = Proveedor.query.filter_by(estatus='Activo').count()
        inactivos = Proveedor.query.filter_by(estatus='Inactivo').count()

        # Objeto temporal para repoblar el panel con lo que escribió el usuario
        class Temporal:
            pass
        temp             = Temporal()
        temp.id          = int(prov_id)
        temp.razonSocial = razon
        temp.correo      = correo
        temp.telefono    = telefono
        temp.direccion   = direccion
        temp.estatus     = estatus

        return render_template(
            'proveedores/index.html',
            proveedores      = lista,
            proveedor_editar = temp,
            estatus_activo   = '',
            busqueda         = '',
            total            = total,
            activos          = activos,
            inactivos        = inactivos,
            errores          = errores,
        ), 422

    # ── CREATE ───────────────────────────────────────────────
    if prov_id == '0':
        if Proveedor.query.filter_by(correo=correo).first():
            flash('⚠️ Ese correo ya está registrado en otro proveedor.', 'error')
            return redirect(next_url)

        db.session.add(Proveedor(
            razonSocial = razon,
            correo      = correo,
            telefono    = telefono,
            direccion   = direccion,
            estatus     = estatus,
        ))
        db.session.commit()
        flash(f'✅ Proveedor "{razon}" registrado correctamente.', 'success')

    # ── UPDATE ───────────────────────────────────────────────
    else:
        p = Proveedor.query.get_or_404(int(prov_id))

        if Proveedor.query.filter(
            Proveedor.correo == correo,
            Proveedor.id != p.id
        ).first():
            flash('⚠️ Ese correo ya está registrado en otro proveedor.', 'error')
            return redirect(next_url)

        p.razonSocial = razon
        p.correo      = correo
        p.telefono    = telefono
        p.direccion   = direccion
        p.estatus     = estatus
        db.session.commit()
        flash(f'✅ Proveedor "{razon}" actualizado correctamente.', 'success')

    return redirect(next_url)


# ── POST /proveedores/<id>/toggle ────────────────────────────
@proveedores.route('/proveedores/<int:id>/toggle', methods=['POST'])
def toggle_estatus(id):
    p         = Proveedor.query.get_or_404(id)
    p.estatus = 'Inactivo' if p.estatus == 'Activo' else 'Activo'
    db.session.commit()

    icono = '✅' if p.estatus == 'Activo' else '⏸'
    flash(f'{icono} {p.razonSocial} marcado como {p.estatus}.', 'success')

    return redirect(request.form.get('next', url_for('proveedores.index')))

# Colores de avatar — se asignan por posición en la lista
AVATAR_COLORES = [
    'linear-gradient(135deg,#F4A4A4,#E8756A)',
    'linear-gradient(135deg,#B8EDE4,#5CC8BC)',
    'linear-gradient(135deg,#E8D5F5,#9B72CF)',
    'linear-gradient(135deg,#FFF3C4,#D4956A)',
    'linear-gradient(135deg,#C8E8FF,#5BA8D8)',
]

def enriquecer(lista):
    """Agrega avatar_color a cada objeto Proveedor para usarlo en el template."""
    for i, p in enumerate(lista):
        p.avatar_color = AVATAR_COLORES[i % len(AVATAR_COLORES)]
    return lista
