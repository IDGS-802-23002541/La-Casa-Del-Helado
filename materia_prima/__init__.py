from flask import Blueprint, render_template, request, redirect, url_for
from models import db, MateriaPrima, Categoria, Proveedor

materia_bp = Blueprint(
    'materia',
    __name__,
    template_folder='templates'
)

@materia_bp.route("/materia", methods=["GET", "POST"])
def materia():
    if request.method == "POST":
        materia_id = request.form.get("id")
        nombre = request.form.get("nombre")
        unidadBase = request.form.get("unidadBase")
        stockActual = request.form.get("stockActual") or 0
        stockMinimo = request.form.get("stockMinimo") or 0
        idCategoria = request.form.get("idCategoria")
        idProveedor = request.form.get("idProveedor")
        estatus = request.form.get("estatus")

        # Conversión de tipos de datos
        idCategoria = int(idCategoria) if idCategoria else None
        idProveedor = int(idProveedor) if idProveedor else None
        stockActual = float(stockActual)
        stockMinimo = float(stockMinimo)

        if materia_id:
            # EDITAR
            materia_existente = MateriaPrima.query.get(materia_id)
            if materia_existente:
                materia_existente.nombre = nombre
                materia_existente.unidadBase = unidadBase
                materia_existente.stockActual = stockActual
                materia_existente.stockMinimo = stockMinimo
                materia_existente.idCategoria = idCategoria
                materia_existente.idProveedor = idProveedor
                materia_existente.estatus = True if estatus == "1" else False
        else:
            # CREAR
            nueva = MateriaPrima(
                nombre=nombre,
                unidadBase=unidadBase,
                stockActual=stockActual,
                stockMinimo=stockMinimo,
                idCategoria=idCategoria,
                idProveedor=idProveedor,
                estatus=True if estatus == "1" else False
            )
            db.session.add(nueva)

        db.session.commit()
        return redirect(url_for("materia.materia"))

    # CONSULTAS
    materias_db = MateriaPrima.query.all()
    categorias = Categoria.query.all()
    proveedores = Proveedor.query.all()

    # Formateo de datos para el template
    materias_primas = []
    for mp in materias_db:
        materias_primas.append({
            "id": mp.id,
            "nombre": mp.nombre,
            "unidadBase": mp.unidadBase,
            "stockActual": float(mp.stockActual or 0),
            "stockMinimo": float(mp.stockMinimo or 0),
            "estatus": mp.estatus,
            "categoria": {
                "id": mp.categoria.id if mp.categoria else None,
                "nombre": mp.categoria.nombre if mp.categoria else "Sin categoría"
            },
            "proveedor": {
                "id": mp.proveedor.id if mp.proveedor else None,
                "razonSocial": mp.proveedor.razonSocial if mp.proveedor else "Sin proveedor"
            }
        })

    return render_template(
        "materia_prima/materia.html",
        materias_primas=materias_primas,
        categorias=categorias,
        proveedores=proveedores
    )