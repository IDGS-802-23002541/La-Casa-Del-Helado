from re import DEBUG

class config(object):
    SECRET_KEY='Clave nueva'
    SESSION_COOKIE_SECURE=False

class DevelopmentConfig(config):   
    DEBUG= True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:0510@localhost:3306/casadelhelado'
    SQLALCHEMY_TRACK_MODIFICATIONS= False
    SECURITY_PASSWORD_SALT = 'super-secret-salt-lcdh'
    WTF_CSRF_ENABLED = False # cambiar a true si esta en produccion
    SECURITY_LOGIN_URL = '/fs-login'
    SECURITY_LOGOUT_URL = '/fs-logout'
    SECURITY_REGISTERABLE = False