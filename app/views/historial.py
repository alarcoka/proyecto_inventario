from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Transacciones

historial = Blueprint('historial', __name__)


@historial.route('/historial')
@login_required
def historial_view():
    transacciones = Transacciones.query.all()
    return render_template('historial.html', transacciones=transacciones)
