from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = False


class DevelopmentConfig(Config):
    DEBUG = True

    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    WTF_CSRF_ENABLED = False  # True en producción
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_LOGIN_URL = '/fs-login'
    SECURITY_LOGOUT_URL = '/fs-logout'
    SECURITY_REGISTERABLE = False