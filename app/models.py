from sqlalchemy import func
from app import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Item(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50))
    cantidad = db.Column(db.Integer)
    
    transacciones = db.relationship('Transacciones', backref='related_item', lazy=True)
    
    def __repr__(self):
        return f'Item(item_id={self.item_id}, nombre=(self.nombre)'
    
class Departamentos(db.Model):
    __tablename__ = "departamentos"
    dept_id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50))
    
    transacciones = db.relationship('Transacciones', backref='departamento_rel', lazy=True)
    
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(60), nullable=False)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('departamentos.dept_id'))
    rol = db.Column(db.Enum('admin', 'principal', 'usuario'))
    
    def __repr__(self):
        return f"User('{self.nombre}', '{self.email}')"

    def get_id(self):
        return str(self.user_id)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            current_app.logger.error(f"Error verifying reset token: {e}")
            return None
        return User.query.get(user_id)



    orden_pedida = db.relationship('Transacciones', foreign_keys='Transacciones.pedido_por_id', back_populates='pedido_por_user', lazy=True)
    orden_confirmada = db.relationship('Transacciones', foreign_keys='Transacciones.confirmado_por_id', back_populates='confirmado_por_user', lazy=True)

class Transacciones(db.Model):
    __tablename__ = 'transacciones'
    tr_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), autoincrement=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('departamentos.dept_id'))
    cantidad_pedida = db.Column(db.Integer)  
    cantidad_entregada = db.Column(db.Integer, default=0)
    cantidad_recibida = db.Column(db.Integer, default=0)
    tr_tipo = db.Column(db.Enum('Pedido', 'Entrega', 'Recibo', 'Confirmacion'))
    confirmado = db.Column(db.Boolean, default=False)
    fecha_pedido = db.Column(db.DateTime, default = db.func.current_timestamp())
    fecha_confirmado = db.Column(db.DateTime)
    pedido_por_id = db.Column(db.Integer, db.ForeignKey('user.user_id')) 
    confirmado_por_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)


    item_rel = db.relationship('Item', backref='tr_item_rel', lazy=True)
    dept_rel = db.relationship('Departamentos', backref='tr_dept_rel', lazy=True)
    
    pedido_por_user = db.relationship('User', foreign_keys=[pedido_por_id], back_populates='orden_pedida')
    confirmado_por_user = db.relationship('User', foreign_keys=[confirmado_por_id], back_populates='orden_confirmada')
