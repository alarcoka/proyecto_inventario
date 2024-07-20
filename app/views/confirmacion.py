from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db, socketio
from app.models import Transacciones, Item
from app.decorators import roles_required
from datetime import datetime

confirmacion = Blueprint('confirmacion', __name__)

@confirmacion.route('/confirmacion/<int:tr_id>', methods=['GET', 'POST'])
@roles_required('admin', 'usuario')
@login_required
def confirmacion_view(tr_id):
    transaccion = Transacciones.query.get(tr_id)
    
    if not transaccion:
        return "Transaccion no encontrada", 404
    
    if request.method == 'POST':
        cantidad_entregada = request.form.get('cantidad_entregada')
        if not cantidad_entregada:
            return "Por favor ingrese la cantidad que fue entregada.", 400
        
        transaccion.cantidad_entregada = cantidad_entregada
        transaccion.confirmado = True
        transaccion.fecha_confirmado = datetime.utcnow()
        transaccion.confirmado_por_id = current_user.user_id
 
        item = Item.query.get(transaccion.item_id)
        item.cantidad -= int(cantidad_entregada)
        
        db.session.commit()

        socketio.emit('delivery_confirmed', {'message': 'Delivery confirmed'})


        return redirect(url_for('main.index'))
    
    return render_template('confirmacion.html', transaccion=transaccion)

@confirmacion.route('/confirmaciones')
@roles_required('admin', 'usuario')
@login_required
def confirmaciones_view():
    transacciones_pendientes = Transacciones.query.filter_by(confirmado=False).all()
    return render_template('confirmaciones.html', transacciones=transacciones_pendientes)

