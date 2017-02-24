import os
class Config(object):
	DEBUG = True
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'sqlite://'
	SECRET_KEY = "6E3[\x1c\x0f\x8a\xc0\xad\x93==\xe9\xa2\xed\xf1*\xde\xab\xae\x99\x8d\xb3="

class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///database/bucketlist.db'

class DevelopmentConfig(Config):
	TESTING = True

class TestingConfig(Config):
	TESTING = True
	SECRET_KEY = os.getenv('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = 'sqlite://'
