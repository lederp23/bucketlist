from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db
from api.models import BucketList, Item
from accounts.models import User

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def init_db():
    db.create_all()

@manager.command
def drop_db():
    db.drop_all()

if __name__ == "__main__":
    manager.run()
