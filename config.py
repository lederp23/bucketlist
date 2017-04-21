import os


class Config(object):
    DEBUG = True
    TESTING = False
    POSTGRES = {
        'user': 'postgres',
        'pw': '',
        'db': 'bucketlist',
        'host': 'localhost',
        'port': '5432',
    }

    SQLALCHEMY_DATABASE_URI = os.getenv('HEROKU_POSTGRESQL_PUCE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    TESTING = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = os.getenv('SECRET_KEY')
