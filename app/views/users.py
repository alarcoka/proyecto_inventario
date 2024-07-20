from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from app import db, mail, bcrypt, current_app
from app.models import User
from app.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from werkzeug.security import generate_password_hash, check_password_hash

users = Blueprint('users', __name__)


@users.route("/registrar", methods=['GET', 'POST'])
def registrar():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(nombre = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'\u00a1Tu cuenta ha sido creada, {form.username.data}!', 'success')
        return redirect(url_for('users.login'))
    return render_template('registrar.html', title='Registrar', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('No se pudo iniciar la sesión. Por favor revise su email y contraseña.', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))



def send_reset_email(user):
    try:
        token = user.get_reset_token()
        msg = Message('Pedir Cambio de Contraseña',
                      sender='noreply@demo.com',
                      recipients=[user.email])
        msg.body = f'''Para cambiar su contraseña, por favor ingrese al siguiente link:
    {url_for('users.reset_token', token=token, _external=True)}

    Si usted no pidió este cambio, ignore este mensaje y no habrá ninguna alteración.
    '''
        mail.send(msg)
    except Exception as e:
        current_app.logger.error(f"Error sending reset email: {e}")
    raise


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('Se ha enviado un email con instrucciones para cambiar su contraseña.', 'info')
        else:
            flash('No se encontró una cuenta con ese correo electrónico.', 'warning')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Este token es inválido o ha expirado.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Su contraseña se ha actualizado! Ahora puede iniciar sesión.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

