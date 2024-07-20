from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_socketio import SocketIO

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
migrate = Migrate()
socketio = SocketIO()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'Por favor, inicia sesión para continuar.'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    login_manager.init_app(app)

    from app.views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.views.users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/users')

    from app.views.pedidos import pedidos as pedidos_blueprint
    app.register_blueprint(pedidos_blueprint, url_prefix='/pedidos')

    from app.views.confirmacion import confirmacion as confirmacion_blueprint
    app.register_blueprint(confirmacion_blueprint, url_prefix='/confirmacion')

    from app.views.envios import envios as envios_blueprint
    app.register_blueprint(envios_blueprint, url_prefix='/envios')

    from app.views.historial import historial as historial_blueprint
    app.register_blueprint(historial_blueprint, url_prefix='/historial')

    from app.views.inventario import inventario as inventario_blueprint
    app.register_blueprint(inventario_blueprint, url_prefix='/inventario')

    return app
