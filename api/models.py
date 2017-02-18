from app import db
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class BucketList(db.Model):
    __tablename__ = 'bucketlists'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.username'), nullable=False)
    items = db.relationship('Item', backref='bucketlists', lazy='dynamic')

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def __repr__(self):
        return '<BucketList %r>' % self.name

class Item(db.Model):
    __tablename__ = 'items'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    done = Column(db.Boolean, default=False)
    bucketlist = db.Column(db.Integer, db.ForeignKey('bucketlists.name'), nullable=False)

    def __init__(self, name, bucketlist):
        self.name = name
        self.bucketlist = bucketlist

    def __repr__(self):
        return '<Item %r>' % self.name
