from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

from v1.api.models import BucketList, Item
from v1.accounts.models import User
from config import ProductionConfig
from v1.accounts.views import accounts
from v1.api.views import api

app = Flask(__name__)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
app.config.from_object(ProductionConfig())
app.register_blueprint(api)
app.register_blueprint(accounts)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
	manager.run()
