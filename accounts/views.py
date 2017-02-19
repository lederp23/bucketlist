from app import app
from accounts.models import User

@app.route('/auth/login', methods=['POST'])
def login(name):
    """Logs a user in"""
    pass

@app.route('/auth/register', methods=['POST'])
def register(name):
    """Registers a user"""
    pass
