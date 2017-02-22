import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from flask_sqlalchemy import SQLAlchemy
from app import db

class Item(db.Model):
    """Model for bucketlist items"""
    __tablename__ = 'items'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    done = Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'), nullable=False)

    def __init__(self, name, bucketlist):
        self.name = name
        self.bucketlist_id = bucketlist

    def __repr__(self):
        return '<Item %r>' % self.name

class BucketList(db.Model):
    """Model for bucketlists"""
    __tablename__ = 'bucketlists'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, nullable=True)
    items = db.relationship(Item, backref='bucketlists', lazy='dynamic')

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def __repr__(self):
        return '<BucketList %r>' % self.name
