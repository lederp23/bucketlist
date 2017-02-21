from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from api.models import BucketList, Item
from accounts.models import User
from config import ProductionConfig
from accounts.views import accounts
from api.views import api

migrate = Migrate(app, db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/bucketlist.db'
app.register_blueprint(api)
app.register_blueprint(accounts)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
