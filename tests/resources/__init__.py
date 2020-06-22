from dotenv import load_dotenv
from os import environ
from urllib.request import urlopen
from flask import Flask, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from schema.schema_file import Schema
from resources import initialize_resources
import pytest
db = SQLAlchemy()


def create_test_app():
    app = Flask(__name__)
    load_dotenv('./environments/test.env')
    for item in environ.items():
        app.config[item[0]] = item[1]
    db.init_app(app)
    db.drop_all()
    Schema.migration()
    Schema.prepare_db()
    initialize_resources(app)
    return app


@pytest.fixture
def app():
    app = create_test_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()
