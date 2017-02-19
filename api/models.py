from app import db
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class BucketList(db.Model):
    """Model for bucketlists"""
    __tablename__ = 'bucketlists'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, nullable=True)
    items = db.relationship('Item', backref='bucketlists', lazy='dynamic')

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def __repr__(self):
        return '<BucketList %r>' % self.name

class Item(db.Model):
    """Model for bucketlist items"""
    __tablename__ = 'items'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    done = Column(db.Boolean, default=False)
    bucketlist = db.Column(db.Integer, db.ForeignKey('bucketlists.id'), nullable=True)

    def __init__(self, name, bucketlist):
        self.name = name
        self.bucketlist = bucketlist

    def __repr__(self):
        return '<Item %r>' % self.name
