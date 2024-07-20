import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    #SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://aalarcon:Qtgc.2024@QTGCInventarioDSN/inventario'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER = 'EST-70-05\\SQLEXPRESS'
    DATABASE = 'inventario'
    USERNAME = 'aalarcon'
    PASSWORD = 'Qtgc.2024'
    DRIVER = 'ODBC Driver 17 for SQL Server'
    dsn = 'QTGCInventarioDSN'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_DEFAULT_SENDER = os.environ.get('EMAIL_USER')

