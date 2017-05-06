import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import datetime
import json
from flask import g
from flask import jsonify, abort, request, make_response
from v1.accounts.views import requires_auth
from v1.api.models import Item, BucketList
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort
from db_setup import db


PER_PAGE = 20


def get_bucketlists(request, version):
    """Returns all bucketlists"""
    if requires_auth(request):
        limit = int(request.args.get('limit') if request.args.get('limit')
                    else PER_PAGE)
        offset = int(request.args.get('offset')
                     if request.args.get('offset') else 0)
        start = (request.args.get('q') if request.args.get('q') else '')
        count = db.session.query(BucketList).filter(
            BucketList.created_by == g.user.username).count()
        if start:
            bucket = db.session.query(BucketList).filter(
                BucketList.name.contains(start)).filter(
                BucketList.created_by == g.user.username).order_by(BucketList.id.desc())[:(offset + limit)]
        else:
            bucket = db.session.query(BucketList).filter(
                BucketList.created_by == g.user.username).order_by(BucketList.id.desc())[:(offset + limit)]
        bucketlists = []
        for bucketlist in bucket:
            items = []
            for item in bucketlist.items:
                items.append({"id": item.id,
                              "name": item.name,
                              "date_created": item.date_created,
                              "date_modified": item.date_modified,
                              "done": item.done})
            items = sorted(items, key=lambda k: k['date_created'], reverse=True)
            bucketlists.append({"id": bucketlist.id,
                                "name": bucketlist.name,
                                "items": items,
                                "date_created": bucketlist.date_created,
                                "date_modified": bucketlist.date_modified,
                                "created_by": bucketlist.created_by,
                                "url": "/api/" + version + "/bucketlists/" +
                                str(bucketlist.id)})
        print(len(bucketlists), count, (len(bucketlists) % limit))
        if len(bucketlists) < count - limit:
            next_url = '/api/' + version + '/bucketlists/?q=' + start + \
                '&limit=' + str(limit) + '&offset=' + str(offset + limit)
        else:
            next_url = None
        if offset >= limit:
            previous_url = '/api/' + version + '/bucketlists/?q=' + start + \
                '&limit=' + str(limit) + '&offset=' + str(offset - limit)
        else:
            previous_url = ''
        number = (limit if (len(bucketlists) % limit)
                  == 0 else (len(bucketlists) % limit))
        bucketlists = bucketlists[-number:]
        return jsonify({"next_url": next_url, "previous_url": previous_url,
                        "bucketlists": bucketlists})


def get_bucketlist(request, id):
    """Returns a bucketlist using ID"""
    if requires_auth(request):
        bucket = db.session.query(BucketList).filter(
            BucketList.id == id).filter(BucketList.created_by ==
                                        g.user.username).first()
        bucketlist = []
        items = []
        if bucket:
            for item in bucket.items:
                items.append({"id": item.id,
                              "name": item.name,
                              "date_created": item.date_created,
                              "date_modified": item.date_modified,
                              "done": item.done})
            bucketlist.append({"id": bucket.id,
                               "name": bucket.name,
                               "items": items,
                               "date_created": bucket.date_created,
                               "date_modified": bucket.date_modified,
                               "created_by": bucket.created_by})
        else:
            abort(make_response(json.dumps(
                {"message": "Bucketlist not found"}), 404))
        return jsonify({"bucketlist": bucketlist[0]})


def add_bucketlist(request):
    """Creates new bucketlist"""
    if requires_auth(request):
        bucketlist = []
        items = []
        data = json.loads(request.get_data(as_text=True))
        if not data['name']:
            abort(make_response(json.dumps(
                {"message": "Bucketlist name missing"}), 400))
        name = data['name']
        count = db.session.query(BucketList).filter(BucketList.name ==
                                                    name).filter(BucketList.created_by ==
                                                                 g.user.username).count()
        if count > 0:
            return jsonify({'message': (name + " already exists"),
                            "bucketlist": []})
        bucket = BucketList(name=name, created_by=g.user.username)
        db.session.add(bucket)
        db.session.commit()
        bucketlist.append({"id": bucket.id,
                           "name": bucket.name,
                           "items": items,
                           "date_created": bucket.date_created,
                           "date_modified": bucket.date_modified,
                           "created_by": bucket.created_by})
        return jsonify({'bucketlist': bucketlist[0],
                        'message': ("successfully added " + name)})


def update_bucketlist(request, id):
    """Updates a bucketlist"""
    if requires_auth(request):
        data = json.loads(request.get_data(as_text=True))
        name = data['name']
        bucket = db.session.query(BucketList).filter(
            BucketList.id == id).filter(BucketList.created_by ==
                                        g.user.username).first()
        bucketlist = []
        items = []
        if bucket:
            bucket.name = name
            bucket.date_modified = datetime.datetime.now()
            db.session.commit()
            for item in bucket.items:
                items.append({"id": item.id,
                              "name": item.name,
                              "date_created": item.date_created,
                              "date_modified": item.date_modified,
                              "done": item.done})
            bucketlist.append({"id": bucket.id,
                               "name": bucket.name,
                               "items": items,
                               "date_created": bucket.date_created,
                               "date_modified": bucket.date_modified,
                               "created_by": bucket.created_by})
            return jsonify({'result': True, 'bucketlist': bucketlist[0],
                            'message': ("successfully updated " + name)})
        abort(make_response(json.dumps(
            {"message": "Bucketlist not found"}), 404))


def delete_bucketlist(request, id):
    """Deletes a bucketlist"""
    if requires_auth(request):
        bucketlist = db.session.query(BucketList).filter(
            BucketList.id == id).filter(BucketList.created_by ==
                                        g.user.username).first()
        if bucketlist:
            db.session.delete(bucketlist)
            db.session.commit()
            return jsonify({'result': True,
                            'message': ('Successfully deleted ' +
                                        bucketlist.name)})
        abort(make_response(json.dumps(
            {"message": "Bucketlist not found"}), 404))


def add_item(request, id):
    """Creates new bucketlist item"""
    if requires_auth(request):
        data = json.loads(request.get_data(as_text=True))
        if not data['name']:
            abort(make_response(json.dumps(
                {"message": "Item name missing"}), 400))
        name = data['name']
        items = []
        item = Item(name=name, bucketlist=id)
        bucketlist = db.session.query(BucketList).filter(
            BucketList.id == id).filter(BucketList.created_by ==
                                        g.user.username).first()
        if not bucketlist:
            abort(make_response(json.dumps(
                {"message": "Bucketlist not found"}), 404))
        db.session.add(item)
        db.session.commit()
        items.append({"id": item.id,
                      "name": item.name,
                      "date_created": item.date_created,
                      "date_modified": item.date_modified,
                      "done": item.done,
                      "bucketlist_id": item.bucketlist_id})
        return jsonify({'item': items[0],
                        'message': ("successfully added " +
                                    name + " to " + bucketlist.name)})


def update_item(request, id, item_id):
    """Updates a bucketlist item"""
    if requires_auth(request):
        data = json.loads(request.get_data(as_text=True))
        name = data['name']
        done = data['done']
        items = []
        bucketlist = db.session.query(BucketList).filter(
            BucketList.id == id).filter(BucketList.created_by ==
                                        g.user.username).first()
        if not bucketlist:
            abort(make_response(json.dumps(
                {"message": "Bucketlist not found"}), 404))
        item = db.session.query(Item).filter(Item.id == item_id).first()
        if item:
            item.name = name
            if done:
                item.done = done
            item.date_modified = datetime.datetime.now()
            db.session.commit()
            items.append({"id": item.id,
                          "name": item.name,
                          "date_created": item.date_created,
                          "date_modified": item.date_modified,
                          "done": item.done})
            return jsonify({'result': True, 'item': items[0],
                            'message': ("successfully updated " + name)})
        abort(make_response(json.dumps({"message": "Item not found"}), 404))


def delete_item(request, id, item_id):
    """Deletes a bucketlist item"""
    if requires_auth(request):
        bucketlist = db.session.query(BucketList).filter(
            BucketList.id == id).filter(BucketList.created_by ==
                                        g.user.username).first()
        if not bucketlist:
            abort(make_response(json.dumps(
                {"message": "Bucketlist not found"}), 404))
        item = db.session.query(Item).filter(Item.id == item_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({'result': True,
                            'message': ('Successfully deleted ' + item.name)})
        abort(make_response(json.dumps({"message": "Item not found"}), 404))
