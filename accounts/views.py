import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from flask_login import login_required
from accounts.models import User
from config import ProductionConfig
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask.blueprints import Blueprint
from flask import request, jsonify
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
    return jsonify({'result': authorized})

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

@accounts.route('/auth/token', methods=['GET', 'POST'])
def get_auth_token():
        """Encode a secure token for cookie"""
        username = request.form['username']
        password = request.form['password']
        data = [username, password]
        return login_serializer.dumps(data)

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = db.session.query(User).filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@login_manager.token_loader
def load_token(token):
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
    data = login_serializer.loads(token, max_age=max_age)
    user = User.get(data[0])
    if user and data[1] == user.password:
        return user
    return None
