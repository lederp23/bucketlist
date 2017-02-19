from app import app
from accounts.models import User

@app.route('/auth/login', methods=['POST'])
def login():
    """Logs a user in"""
    authorized = False
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
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
    if User.query.filter_by(username = username).first() is not None:
        abort(400)
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201,
