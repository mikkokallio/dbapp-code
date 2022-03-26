from os import getenv
from flask_sqlalchemy import SQLAlchemy
from .app import app


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQL_URI")
db = SQLAlchemy(app)
