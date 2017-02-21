from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
from config import *

app = Flask(__name__)
app.config.from_object(ProductionConfig())
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

if __name__ == "__main__":
    app.run()
