from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.models import Item, Transacciones

inventario = Blueprint('inventario', __name__)


@inventario.route('/inventario')
def inventario_view():
    items = Item.query.all()
    return render_template('inventario.html', items=items)



@inventario.route('/agregar_item', methods=['GET', 'POST'])
@login_required
def agregar_item():
    if request.method == 'POST':
        item_nombre = request.form['nombre']
        dept_id = request.form.get('dept_id')
        cantidad = request.form['cantidad']

        if not item_nombre or not cantidad:
            return "Missing form data", 400

        item = Item.query.filter_by(nombre=item_nombre).first()
        if item:
            item.cantidad += int(cantidad)
            transaccion = Transacciones(item_id=item.item_id, dept_id=1, cantidad_pedida=0, cantidad_entregada=0, cantidad_recibida=int(cantidad), tr_tipo='Recibo', confirmado=True)
        else:
            nuevo_item = Item(nombre=item_nombre, cantidad=int(cantidad))
            db.session.add(nuevo_item)
            db.session.flush()
            transaccion = Transacciones(
                item_id=nuevo_item.item_id,
                dept_id=1,  
                cantidad_pedida=0,
                cantidad_entregada=0,
                cantidad_recibida=cantidad,
                tr_tipo='Recibo',
                confirmado=True
            )
        
        db.session.add(transaccion)
        db.session.commit()
        return redirect(url_for('inventario.inventario_view'))

    return render_template('agregar_item.html')

