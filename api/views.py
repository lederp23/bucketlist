import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from flask import jsonify, abort, request
from flask_login import login_required
from api.models import BucketList, Item
from config import ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask.blueprints import Blueprint
from flask import request, jsonify, abort
from flask_security import auth_token_required
from flask_paginate import Pagination
from app import login_manager

api = Blueprint('api', __name__, template_folder='templates')
db = SQLAlchemy()
auth = HTTPBasicAuth()

PER_PAGE = 20

@api.route('/bucketlist/api/v1.0/bucketlists/', methods=['GET'])
@login_manager.token_loader
def get_bucketlists():
    """Returns all bucketlists"""
    limit = (request.args.get('limit') if request.args.get('limit') else PER_PAGE)
    start = request.args.get('q')
    if start:
        bucket = db.session.query(BucketList).filter(BucketList.name.contains(start)).all()
    else:
        bucket = db.session.query(BucketList).all()
    bucketlists = []
    for bucketlist in bucket:
        items = []
        for item in bucketlist.items:
            items.append({"id": item.id,\
                          "name": item.name,\
                          "date_created": item.date_created,\
                          "date_modified": item.date_modified,\
                          "done": item.done})
        bucketlists.append({"id": bucketlist.id,\
                           "name": bucketlist.name,\
                           "items": items,\
                           "date_created": bucketlist.date_created,\
                           "date_modified": bucketlist.date_modified,\
                           "created_by": bucketlist.created_by})
    pagination = Pagination(page=1, total=len(bucketlists))
    return jsonify({"bucketlists": bucketlists})

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>', methods=['GET'])
@login_manager.token_loader
def get_bucketlist(id):
    """Returns a bucketlist using ID"""
    bucket = db.session.query(BucketList).filter(BucketList.id==id).first()
    bucketlist = []
    items = []
    for item in bucket.items:
        items.append({"id": item.id,\
                      "name": item.name,\
                      "date_created": item.date_created,\
                      "date_modified": item.date_modified,\
                      "done": item.done})
    bucketlist.append({"id": bucket.id,\
                       "name": bucket.name,\
                       "items": items,\
                       "date_created": bucket.date_created,\
                       "date_modified": bucket.date_modified,\
                       "created_by": bucket.created_by})
    if len(bucketlist) == 0:
        abort(404)
    return jsonify({"bucketlist": bucketlist[0]})

@api.route('/bucketlist/api/v1.0/bucketlists/', methods=['POST'])
@login_manager.token_loader
def add_bucketlist():
    """Creates new bucketlist"""
    bucketlist = []
    items = []
    name = request.form['name']
    bucket = BucketList(name=name, created_by=' ')
    db.session.add(bucket)
    db.session.commit()
    bucketlist.append({"id": bucket.id,\
                       "name": bucket.name,\
                       "items": items,\
                       "date_created": bucket.date_created,\
                       "date_modified": bucket.date_modified,\
                       "created_by": bucket.created_by})
    return jsonify({'bucketlist': bucketlist[0]})

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>', methods=['PUT'])
@login_manager.token_loader
def update_bucketlist(id):
    """Updates a bucketlist"""
    name = request.form['name']
    bucket = db.session.query(BucketList).filter(BucketList.id==id).first()
    bucketlist = []
    items=[]
    if bucket:
        bucket.name = name
        db.session.commit()
        for item in bucket.items:
            items.append({"id": item.id,\
                          "name": item.name,\
                          "date_created": item.date_created,\
                          "date_modified": item.date_modified,\
                          "done": item.done})
        bucketlist.append({"id": bucket.id,\
                           "name": bucket.name,\
                           "items": items,\
                           "date_created": bucket.date_created,\
                           "date_modified": bucket.date_modified,\
                           "created_by": bucket.created_by})
        return jsonify({'bucketlist': bucketlist[0]})
    abort(404)

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>', methods=['DELETE'])
@login_manager.token_loader
def delete_bucketlist(id):
    """Deletes a bucketlist"""
    bucketlist = db.session.query(BucketList).filter(BucketList.id==id).first()
    if bucketlist:
        db.session.delete(bucketlist)
        db.session.commit()
        return jsonify({'result': True})
    abort(404)

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>/items/', methods=['GET', 'POST'])
@login_manager.token_loader
def add_item(id):
    """Creates new bucketlist item"""
    name = request.form['name']
    items=[]
    item = Item(name=name, bucketlist=id)
    db.session.add(item)
    db.session.commit()
    items.append({"id": item.id,\
                  "name": item.name,\
                  "date_created": item.date_created,\
                  "date_modified": item.date_modified,\
                  "done": item.done})
    return jsonify({'item': items[0]})

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
@login_manager.token_loader
def update_item(id, item_id):
    """Updates a bucketlist item"""
    name = request.form['name']
    items=[]
    item = db.session.query(Item).filter(Item.id==item_id).first()
    if item:
        item.name = name
        db.session.commit()
        items.append({"id": item.id,\
                      "name": item.name,\
                      "date_created": item.date_created,\
                      "date_modified": item.date_modified,\
                      "done": item.done})
        return jsonify({'item': items[0]})
    abort(404)

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
@login_manager.token_loader
def delete_item(id,item_id):
    """Deletes a bucketlist item"""
    item = db.session.query(Item).filter(Item.id==item_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'result': True})
    abort(404)
