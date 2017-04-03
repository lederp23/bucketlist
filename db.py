from flask_sqlalchemy import SQLAlchemy
import app
from config import ProductionConfig

db = SQLAlchemy(app.app)
