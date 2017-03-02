import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import datetime
from flask import g
from flask import jsonify, abort, request
from v1.api.models import BucketList, Item
from v1.accounts.views import requires_auth
from config import ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask.blueprints import Blueprint
from flask import request, jsonify, abort
from flask_paginate import Pagination
from app import db

api = Blueprint('api', __name__, template_folder='templates')

PER_PAGE = 20

@api.route('/bucketlist/api/v1.0/bucketlists/', methods=['GET'])
@requires_auth
def get_bucketlists():
	"""Returns all bucketlists"""
	limit = int(request.args.get('limit') if request.args.get('limit') else PER_PAGE)
	offset = int(request.args.get('offset') if request.args.get('offset') else 0)
	start = (request.args.get('q') if request.args.get('q') else '')
	if start:
		bucket = db.session.query(BucketList).filter(BucketList.name.\
				 contains(start)).filter(BucketList.id>offset).limit(limit)
	else:
		bucket = db.session.query(BucketList).filter(BucketList.id>offset).\
				 limit(limit)
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
	if len(bucketlists) == limit:
		next_url = '/bucketlist/api/v1.0/bucketlists/?q=' + start + '&limit=' +\
				   str(limit) + '&offset=' + str(offset + limit)
	else:
		next_url = ''
	if offset >= limit:
		previous_url = '/bucketlist/api/v1.0/bucketlists/?q=' + start +\
					   '&limit=' + str(limit) + '&offset=' + str(offset - limit)
	else:
		previous_url = ''
	return jsonify({"bucketlists": bucketlists, "next_url": next_url,\
					"previous_url": previous_url})

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>', methods=['GET'])
@requires_auth
def get_bucketlist(id):
	"""Returns a bucketlist using ID"""
	bucket = db.session.query(BucketList).filter(BucketList.id==id).first()
	bucketlist = []
	items = []
	if bucket:
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
	else:
		abort(404)
	return jsonify({"bucketlist": bucketlist[0]})

@api.route('/bucketlist/api/v1.0/bucketlists/', methods=['POST'])
@requires_auth
def add_bucketlist():
	"""Creates new bucketlist"""
	bucketlist = []
	items = []
	name = request.form['name']
	bucket = BucketList(name=name, created_by=g.user.username)
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
@requires_auth
def update_bucketlist(id):
	"""Updates a bucketlist"""
	name = request.form['name']
	bucket = db.session.query(BucketList).filter(BucketList.id==id).first()
	bucketlist = []
	items=[]
	if bucket:
		bucket.name = name
		bucket.date_modified = datetime.datetime.now()
		db.session.commit()
		return jsonify({'result': True})
	abort(404)

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>', methods=['DELETE'])
@requires_auth
def delete_bucketlist(id):
	"""Deletes a bucketlist"""
	bucketlist = db.session.query(BucketList).filter(BucketList.id==id).first()
	if bucketlist:
		db.session.delete(bucketlist)
		db.session.commit()
		return jsonify({'result': True})
	abort(404)

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>/items/', methods=['POST'])
@requires_auth
def add_item(id):
	"""Creates new bucketlist item"""
	name = request.form['name']
	items=[]
	item = Item(name=name, bucketlist=id)
	bucketlist = db.session.query(BucketList).filter(BucketList.id==id).first()
	if not bucketlist:
		abort(404)
	db.session.add(item)
	db.session.commit()
	items.append({"id": item.id,\
				  "name": item.name,\
				  "date_created": item.date_created,\
				  "date_modified": item.date_modified,\
				  "done": item.done,
				  "bucketlist_id": item.bucketlist_id})
	return jsonify({'item': items[0]})

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>/items/<int:item_id>',\
		   methods=['PUT'])
@requires_auth
def update_item(id, item_id):
	"""Updates a bucketlist item"""
	name = request.form['name']
	items=[]
	bucketlist = db.session.query(BucketList).filter(BucketList.id==id).first()
	if not bucketlist:
		abort(404)
	item = db.session.query(Item).filter(Item.id==item_id).first()
	if item:
		item.name = name
		item.date_modified = datetime.datetime.now()
		db.session.commit()
		items.append({"id": item.id,\
					  "name": item.name,\
					  "date_created": item.date_created,\
					  "date_modified": item.date_modified,\
					  "done": item.done})
		return jsonify({'item': items[0]})
	abort(404)

@api.route('/bucketlist/api/v1.0/bucketlists/<int:id>/items/<int:item_id>',\
		   methods=['DELETE'])
@requires_auth
def delete_item(id,item_id):
	"""Deletes a bucketlist item"""
	item = db.session.query(Item).filter(Item.id==item_id).first()
	if item:
		db.session.delete(item)
		db.session.commit()
		return jsonify({'result': True})
	abort(404)
