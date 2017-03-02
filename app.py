from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import ProductionConfig

app = Flask(__name__)
app.config.from_object(ProductionConfig())
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run()
