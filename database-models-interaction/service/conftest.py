"""
This module declares the pytest fixture functions. These provide a fixed baseline
to enable us to reliably and repeatedly execute tests.
"""
import pytest

from models import db
from flask import Flask
from app import create_app
from views import service_blueprint
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture
def application():
    # Beggining of Setup code
    app = create_app('config')
    with app.app_context():
        # End of Setup code
        db.create_all()

        # The test will start running here

        yield app

        # The test finish running here

        # Beginning of Teardown code
        db.session.remove()
        db.drop_all()

        # End of Teardown code

@pytest.fixture
def client(application):
    return application.test_client()

