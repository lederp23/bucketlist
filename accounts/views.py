import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from flask import g
from flask_login import login_required
from functools import wraps
from accounts.models import User, verify_auth_token
from config import ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask.blueprints import Blueprint
from flask import request, jsonify, abort
from app import login_manager, app
from itsdangerous import URLSafeTimedSerializer

accounts = Blueprint('accounts', __name__, template_folder='templates')
login_serializer = URLSafeTimedSerializer(app.secret_key)

db = SQLAlchemy()
auth = HTTPBasicAuth()


@accounts.route('/auth/login', methods=['GET', 'POST'])
def login():
	"""Logs a user in"""
	authorized = False
	username = request.form['username']
	password = request.form['password']
	user = db.session.query(User).filter_by(username=username).first()
	if user and user.verify_password(password):
		authorized = True
	access_token = user.generate_token()
	return jsonify({'result': authorized, 'access_token': access_token.decode('UTF-8')})

@accounts.route('/auth/register', methods=['GET', 'POST'])
def register():
	"""Registers a user"""
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']

	if username is None or password is None:
		return jsonify(400)
	if db.session.query(User).filter_by(username=username).first() is not None:
		return jsonify(400)
	user = User(username=username, email=email, password=password)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()
	return jsonify({ 'username': user.username })

@auth.verify_password
def verify_password(username_or_token, password):
	user = User.verify_auth_token(username_or_token)
	if not user:
		user = db.session.query(User).filter_by(username = username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.headers['Token']
		if not auth:
			abort(401)
		user = verify_auth_token(auth)
		if user is None:
			abort(401)
		return f(*args, **kwargs)
	return decorated
