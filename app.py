from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import ProductionConfig

app = Flask(__name__)
app.config.from_object(ProductionConfig())
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run()
