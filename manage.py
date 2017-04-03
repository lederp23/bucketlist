import os
import sys
import inspect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import Flask
from flask_cors import CORS, cross_origin

from config import ProductionConfig
from urls import urls
from v1.api.models import BucketList, Item
from v1.accounts.models import User
import app

cors = CORS(app.app, resources={r"/api/*": {"origins": "*"}})

migrate = Migrate(app.app, app.db)
app.app.config.from_object(ProductionConfig())
app.app.register_blueprint(urls)
app.app.url_map.strict_slashes = False
manager = Manager(app.app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates database with tables"""
    app.db.create_all()
    app.db.session.commit()


@manager.command
def drop_db():
    """Creates database with tables"""
    app.db.drop_all()

if __name__ == "__app__":
    manager.run()
