from app import db
from sqlalchemy import Column, Integer, String

class User(db.Model):
    """Model for users"""
    __tablename__ = 'users'
    id = db.Column(Integer, autoincrement=True)
    username = db.Column(String, unique=True, primary_key=True)
    email = db.Column(String, unique=True)
    password = db.Column(String)
    api_key = db.Column(String, unique=True)
    bucketlists = db.relationship('BucketList', backref='users', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def hash_password(self, new_password):
        self.password = pwd_context.encrypt(new_password)

    def verify_password(self, current_password):
        return pwd_context.verify(current_password, self.password)
