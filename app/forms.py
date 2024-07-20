# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, nombre):
        user = User.query.filter_by(nombre=nombre.data).first()
        if user:
            raise ValidationError('Ya existe este nombre. Por favor, utilice otro.')
        
        def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Este email ya está en uso. Por favor, utilice otro.')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuérdame')
    submit = SubmitField('Login')



class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Cambiar contraseña')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Si hay un email asociado con esta cuenta, se enviará un mensaje para cambiar su contraseña pronto.')



class ResetPasswordForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cambiar Contraseña')