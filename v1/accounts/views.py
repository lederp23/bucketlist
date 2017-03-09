import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import re
from flask import g
from v1.accounts.models import User, verify_auth_token
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort
from validate_email import validate_email
from app import app, db


def login(request):
    """Logs a user in"""
    authorized = False
    username = request.form['username']
    password = request.form['password']
    if username is '' or password is '':
        abort(400)
    if not re.match('^[a-zA-Z0-9-_]*$', username):
        return jsonify({'error': 'username cannot have special characters'})
    user = db.session.query(User).filter_by(username=username).first()
    if not user:
        abort(404)
    if user and user.verify_password(password):
        authorized = True
    else:
        abort(401)
    access_token = user.generate_token()
    return jsonify({'result': authorized,
                    'access_token': access_token.decode('UTF-8')})


def register(request):
    """Registers a user"""
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    is_valid = validate_email(email)
    if username is '' or password is '':
        abort(400)
    if not is_valid:
        return jsonify({'error': 'invalid email'})
    if not re.match('^[a-zA-Z0-9-_]*$', username):
        return jsonify({'error': 'username cannot have special characters'})
    if db.session.query(User).filter_by(username=username).first() is not None:
        return jsonify({'error': 'user already exists'})
    user = User(username=username, email=email, password=password)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username})


def requires_auth(request):
    """Ensures a user is authenticated before accessing data"""
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
    return True
