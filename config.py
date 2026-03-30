from re import DEBUG

class config(object):
    SECRET_KEY='Clave nueva'
    SESSION_COOKIE_SECURE=False

class DevelopmentConfig(config):   
    DEBUG= True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123456789@localhost:3306/lacasadelhelado'
    SQLALCHEMY_TRACK_MODIFICATIONS= False
