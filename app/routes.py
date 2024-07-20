'''

import os
from tkinter import CURRENT
from flask import render_template, request, redirect, url_for, flash
from app import app, db, bcrypt, mail, socketio
from app.decorators import roles_required
from app.models import Item, Departamentos, Transacciones, User
from app.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_mail import Message
from sqlalchemy import func


'''













