import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from flask import g
from functools import wraps
from bucketlist_modules.accounts.models import User, verify_auth_token
from config import ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask.blueprints import Blueprint
from flask import request, jsonify, abort
from app import app, db

accounts = Blueprint('accounts', __name__, template_folder='templates')

@accounts.route('/auth/login', methods=['GET', 'POST'])
def login():
	"""Logs a user in"""
	authorized = False
	username = request.form['username']
	password = request.form['password']
	user = db.session.query(User).filter_by(username=username).first()
	if not user:
		abort(404)
	if user and user.verify_password(password):
		authorized = True
	else:
		abort(401)
	access_token = user.generate_token()
	return jsonify({'result': authorized, 'access_token': access_token.decode('UTF-8')})

@accounts.route('/auth/register', methods=['GET', 'POST'])
def register():
	"""Registers a user"""
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']

	if username is '' or password is '':
		abort(400)
	if db.session.query(User).filter_by(username=username).first() is not None:
		return jsonify({'error': 'user already exists'})
	user = User(username=username, email=email, password=password)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	return jsonify({ 'username': user.username })

def requires_auth(f):
	"""Ensures a user is authenticated before accessing data"""
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = ''
		try:
			auth = request.headers['Token']
		except KeyError:
			pass
		if not auth:
			abort(401)
		user = verify_auth_token(auth)
		if user is None:
			abort(401)
		return f(*args, **kwargs)
	return decorated
