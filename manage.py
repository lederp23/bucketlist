import os
import sys
import inspect
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import Flask
from flask_cors import CORS, cross_origin

from config import ProductionConfig
from urls import urls
from app import app, db
from v1.api.models import BucketList, Item
from v1.accounts.models import User

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

migrate = Migrate(app, db)
app.config.from_object(ProductionConfig())
app.register_blueprint(urls)
app.url_map.strict_slashes = False
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates database with tables"""
    db.create_all()
    db.session.commit()


@manager.command
def drop_db():
    """Creates database with tables"""
    db.drop_all()

if __name__ == "__app__":
    manager.run()
