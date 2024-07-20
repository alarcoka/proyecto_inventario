from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Transacciones
from app.decorators import roles_required
from datetime import datetime, timedelta

envios = Blueprint('envios', __name__)

@envios.route('/envios')
@login_required
@roles_required('principal', 'admin')
def envios_view():
    if current_user.rol not in ['admin', 'principal']:
        flash('No tienes acceso a esta página.', 'danger')
        return redirect(url_for('main.index'))

    today = datetime.today().date()
    transacciones = Transacciones.query.filter(
        Transacciones.tr_tipo == 'Pedido',
         Transacciones.confirmado == False,
        db.cast(Transacciones.fecha_pedido, db.Date) == today
    ).order_by(Transacciones.dept_id).all()
    
    return render_template('envios.html', transacciones=transacciones)

