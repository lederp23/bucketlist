from flask_sqlalchemy import SQLAlchemy
from app import app
from config import ProductionConfig

app.config.from_object(ProductionConfig())
db = SQLAlchemy(app)
