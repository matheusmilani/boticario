from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from schema.schema_file import Schema
from dotenv import load_dotenv
from os import environ
from models import initialize_database
from os import environ
from resources import initialize_resources
db = SQLAlchemy()


def create_test_app():
    global db
    global app

    app = Flask(__name__)
    load_dotenv('./environments/local.env')
    for item in environ.items():
        app.config[item[0]] = item[1]
    app.app_context().push()

    db.init_app(app)
    db.reflect()
    db.drop_all()

    initialize_database(app)
    initialize_resources(app)

    Schema.migration()
    Schema.prepare_db()
