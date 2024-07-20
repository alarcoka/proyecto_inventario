from flask_mail import Message
from flask import current_app
from app import mail

def send_notification_email(to, subject, template, item_name, requester_name):
    app = current_app._get_current_object()
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
