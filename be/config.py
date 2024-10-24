import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'aaaaa'
    JWT_SECRET_KEY = 'aaaaa'
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'hpq833595@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'rpce ohsa zmxv dnlb'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'hpq833592@gmail.com'
    
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'atm_banking'
