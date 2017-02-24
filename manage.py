from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from bucketlist_modules.api.models import BucketList, Item
from bucketlist_modules.accounts.models import User
from config import ProductionConfig
from bucketlist_modules.accounts.views import accounts
from bucketlist_modules.api.views import api

migrate = Migrate(app, db)
app.config.from_object(ProductionConfig())
app.register_blueprint(api)
app.register_blueprint(accounts)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
