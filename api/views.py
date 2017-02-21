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

api = Blueprint('api', __name__, template_folder='templates')
db = SQLAlchemy()
auth = HTTPBasicAuth()

PER_PAGE = 20

@api.route('/bucketlist/api/v1.0/bucketlists/', methods=['GET'])
@auth.login_required
def get_bucketlists():
    """Returns all bucketlists"""
    args = request.args
    limit = ((int(args['limit']) if int(args['limit'])< 100 else PER_PAGE) if args['limit'] else PER_PAGE)
    start = (args['q'] if args['q'] else "")
    bucket = db.session.query(BucketList).filter(BucketList.name.like(start)).all()
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
    bucketlists=bucketlist.paginate(1, limit, len(bucketlists))
    return jsonify({"bucketlists": bucketlists})

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>', methods=['GET'])
@auth.login_required
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

@api.route('/bucketlist/api/v1.0/bucketlists/', methods=['GET', 'POST'])
@auth.login_required
def add_bucketlist():
    """Creates new bucketlist"""
    bucketlist = []
    items = []
    name = requestform['name']
    bucket = BucketList(name=name)
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
@auth.login_required
def update_bucketlist(id):
    """Updates a bucketlist"""
    name = request.json.get('name')
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
@auth.login_required
def delete_bucketlist(id):
    """Deletes a bucketlist"""
    bucketlist = db.session.query(BucketList).filter(BucketList.id==id).first()
    if bucketlist:
        db.session.delete(bucketlist)
        db.session.commit()
        return jsonify({'result': True})
    abort(404)

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>/items/', methods=['GET', 'POST'])
@auth.login_required
def add_item():
    """Creates new bucketlist item"""
    name = requestform['name']
    items=[]
    item = Item(name=name)
    db.session.add(item)
    db.session.commit()
    items.append({"id": item.id,\
                  "name": item.name,\
                  "date_created": item.date_created,\
                  "date_modified": item.date_modified,\
                  "done": item.done})
    return jsonify({'item': item[0]})

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_item(item_id):
    """Updates a bucketlist item"""
    name = request.json.get('name')
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
        return jsonify({'item': item[0]})
    abort(404)

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>/items/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_item(item_id):
    """Deletes a bucketlist item"""
    item = db.session.query(BucketList).filter(BucketList.id==item_id).first()
    if item:
        db.session.delete(bucketlist)
        db.session.commit()
        return jsonify({'result': True})
    abort(404)
