import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import re
import importlib
from flask import g, request
from functools import wraps
from config import ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask.blueprints import Blueprint
from validate_email import validate_email
from app import app, db

urls = Blueprint('urls', __name__, template_folder='templates')

@urls.route('/api/<version>/auth/login', methods=['GET', 'POST'])
def login_api(version):
	account_views = import_account_views(version)
	return account_views.login(request)

@urls.route('/api/<version>/auth/register', methods=['GET', 'POST'])
def register_user(version):
	account_views = import_account_views(version)
	return account_views.register(request)

@urls.route('/api/<version>/bucketlists/', methods=['GET'])
def get_bucket_lists(version):
	api_views = import_api_views(version)
	return api_views.get_bucketlists(request)

@urls.route('/api/<version>/bucketlists/<int:id>', methods=['GET'])
def get_bucket_list(version, id):
	api_views = import_api_views(version)
	return api_views.get_bucketlist(request, id)

@urls.route('/api/<version>/bucketlists/', methods=['POST'])
def add_bucket_list(version):
	api_views = import_api_views(version)
	return api_views.add_bucketlist(request)

@urls.route('/api/<version>/bucketlists/<int:id>', methods=['PUT'])
def update_bucket_list(version, id):
	api_views = import_api_views(version)
	return api_views.update_bucketlist(request, id)

@urls.route('/api/<version>/bucketlists/<int:id>', methods=['DELETE'])
def delete_bucket_list(version, id):
	api_views = import_api_views(version)
	return api_views.delete_bucketlist(request, id)

@urls.route('/api/<version>/bucketlists/<int:id>/items/', methods=['POST'])
def add_bucketlist_item(version, id):
	api_views = import_api_views(version)
	return api_views.add_item(request, id)

@urls.route('/api/<version>/bucketlists/<int:id>/items/<int:item_id>',\
		   methods=['PUT'])
def update_bucketlist_item(version, id, item_id):
	api_views = import_api_views(version)
	return api_views.update_item(request,id, item_id)

@urls.route('/api/<version>/bucketlists/<int:id>/items/<int:item_id>',\
		   methods=['DELETE'])
def delete_bucketlist_item(version, id, item_id):
	api_views = import_api_views(version)
	return api_views.delete_item(request, id, item_id)

def import_account_views(version):
	"""Imports version of api"""
	mod = importlib.import_module(version + ".accounts.views")
	return mod

def import_api_views(version):
	"""Imports version of api"""
	mod = importlib.import_module(version + ".api.views")
	return mod
