from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS

from config import ProductionConfig
from urls import urls
from db_setup import app, db

app.config.from_object(ProductionConfig())

app.register_blueprint(urls)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

with app.app_context():
    from v1.api.models import BucketList, Item
    from v1.accounts.models import User
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
db.create_all()
db.session.commit()


@manager.command
def create_db():
    """Creates database with tables"""
    db.create_all()
    db.session.commit()


@manager.command
def drop_db():
    """Deletez database"""
    db.drop_all()

if __name__ == "__main__":
    manager.run()
