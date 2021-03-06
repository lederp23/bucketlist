import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import datetime
from db_setup import db


class Item(db.Model):
    """Model for bucketlist items"""
    __tablename__ = 'items'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'),
                              nullable=False)

    def __init__(self, name, bucketlist):
        self.name = name
        self.bucketlist_id = bucketlist


class BucketList(db.Model):
    """Model for bucketlists"""
    __tablename__ = 'bucketlists'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_by = db.Column(db.String, nullable=False)
    items = db.relationship(Item, backref='bucketlists',
                            cascade="all,delete", lazy='dynamic')

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by
