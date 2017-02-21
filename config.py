import os
class Config(object):
    DEBUG = True
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
    SECRET_KEY = "6E3[\x1c\x0f\x8a\xc0\xad\x93==\xe9\xa2\xed\xf1*\xde\xab\xae\x99\x8d\xb3="

class ProductionConfig(Config):
    DATABASE_URI = 'sqlite:///database/bucketlist.db'
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_SALT = 'something_super_secret_change_in_production'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = os.getenv('SECRET_KEY')
