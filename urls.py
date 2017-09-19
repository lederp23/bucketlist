import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import importlib
from flask import request, abort, make_response
from flask.blueprints import Blueprint

urls = Blueprint('urls', __name__, template_folder='templates')


@urls.route('/api/<version>/auth/login', methods=['POST'])
def login_api(version):
    account_views = import_account_views(version)
    return account_views.login(request)


@urls.route('/api/<version>/auth/register', methods=['POST'])
def register_user(version):
    account_views = import_account_views(version)
    return account_views.register(request)


@urls.route('/api/<version>/bucketlists/', methods=['GET'])
def get_bucket_lists(version):
    api_views = import_api_views(version)
    return api_views.get_bucketlists(request, version)


@urls.route('/api/<version>/bucketlists/<int:bucketlist_id>', methods=['GET'])
def get_bucket_list(version, bucketlist_id):
    api_views = import_api_views(version)
    return api_views.get_bucketlist(request, bucketlist_id)


@urls.route('/api/<version>/bucketlists/', methods=['POST'])
def add_bucket_list(version):
    api_views = import_api_views(version)
    return api_views.add_bucketlist(request)


@urls.route('/api/<version>/bucketlists/<int:bucketlist_id>', methods=['PUT'])
def update_bucket_list(version, bucketlist_id):
    api_views = import_api_views(version)
    return api_views.update_bucketlist(request, bucketlist_id)


@urls.route('/api/<version>/bucketlists/<int:bucketlist_id>',
            methods=['DELETE'])
def delete_bucket_list(version, bucketlist_id):
    api_views = import_api_views(version)
    return api_views.delete_bucketlist(request, bucketlist_id)


@urls.route('/api/<version>/bucketlists/<int:bucketlist_id>/items/',
            methods=['POST'])
def add_bucketlist_item(version, bucketlist_id):
    api_views = import_api_views(version)
    return api_views.add_item(request, bucketlist_id)


@urls.route(
    '/api/<version>/bucketlists/<int:bucketlist_id>/items/<int:item_id>',
    methods=['PUT']
)
def update_bucketlist_item(version, bucketlist_id, item_id):
    api_views = import_api_views(version)
    return api_views.update_item(request, bucketlist_id, item_id)


@urls.route(
    '/api/<version>/bucketlists/<int:bucketlist_id>/items/<int:item_id>',
    methods=['DELETE']
)
def delete_bucketlist_item(version, bucketlist_id, item_id):
    api_views = import_api_views(version)
    return api_views.delete_item(request, bucketlist_id, item_id)


def import_account_views(version):
    """Imports version of api"""
    try:
        mod = importlib.import_module(version + ".accounts.views")
        return mod
    except ImportError:
        abort(make_response("Version does not exist", 404))


def import_api_views(version):
    """Imports version of api"""
    try:
        mod = importlib.import_module(version + ".api.views")
        return mod
    except ImportError:
        abort(make_response("Version does not exist", 404))
