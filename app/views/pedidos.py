from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db, socketio
from app.models import Transacciones, Item, Departamentos, User
from app.tasks import send_notification_email

pedidos = Blueprint('pedidos', __name__)


@pedidos.route('/pedidos', methods = ['GET', 'POST'])
@login_required
def pedidos_view():
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        dept_id = request.form.get('dept_id')
        cantidad_pedida = request.form.get('cantidad_pedida')

        print(f"item_id: {item_id}, dept_id: {dept_id}, cantidad_pedida: {cantidad_pedida}")

        
        if not item_id or not dept_id or not cantidad_pedida:
            return "Missing form data", 400
        
        transaccion = Transacciones(
            item_id=item_id, 
            dept_id=dept_id, 
            cantidad_pedida=cantidad_pedida, 
            tr_tipo='Pedido', 
            pedido_por_id=current_user.user_id
            )
        db.session.add(transaccion)
        db.session.commit()

        
        item = transaccion.related_item
        requester = transaccion.pedido_por_user

        recipients = [user.email for user in User.query.filter(
            User.rol.in_(['admin', 'principal'])
        ).all()]

        # Prepare the email template
        email_template = render_template(
            'email/item_request.html',
            item_name=item.nombre,
            requester_name=requester.nombre
        )

       
        for recipient in recipients:
            send_notification_email(
                to=recipient,
                subject='Nuevo Pedido',
                template=email_template,
                item_name=item.nombre,
                requester_name=requester.nombre
        )
        
        socketio.emit('nuevo_pedido', {'message': 'Se ha hecho un nuevo pedido!'})
        
        return redirect(url_for('inventario.inventario_view'))


    items = Item.query.all()
    departamentos = Departamentos.query.all()
    selected_item_id = request.args.get('item_id')
    selected_dept_id = request.args.get('dept_id')
    return render_template('pedidos.html', items=items, departamentos=departamentos, selected_item_id=selected_item_id, selected_dept_id=selected_dept_id)


