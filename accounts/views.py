from app import app, auth, db
from flask_login import login_required
from accounts.models import User

@app.route('/auth/login', methods=['POST'])
def login():
    """Logs a user in"""
    authorized = False
    username = request.json.get('username')
    password = request.json.get('password')
    user = db.session.query(User).filter(User.username=username).first()
    if user and user.verify_password(password):
        authorized = True
    return jsonify({'result': authorized})

@app.route('/auth/register', methods=['POST'])
def register():
    """Registers a user"""
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if db.session.query(User).filter(User.username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201,

@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_token()
    return jsonify({ 'token': token.decode('ascii') })

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        user = db.session.query(User).filter(User.username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
