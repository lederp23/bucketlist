from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import ProductionConfig

main = Flask(__name__)
main.config.from_object(ProductionConfig())
db = SQLAlchemy(main)

if __name__ == "__main__":
    app.run()
