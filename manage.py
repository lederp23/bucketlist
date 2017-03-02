from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from v1.api.models import BucketList, Item
from v1.accounts.models import User
from config import ProductionConfig
from urls import urls

app = Flask(__name__)
db = SQLAlchemy(app)

migrate = Migrate(app, db)
app.config.from_object(ProductionConfig())
app.register_blueprint(urls)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
	manager.run()
