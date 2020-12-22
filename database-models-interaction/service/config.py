"""
This module declares variables that determine the configuration for Flask and SQLAlchemy.
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True

DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASS = os.environ.get('DATABASE_PASS')
DATABASE_ADDR = os.environ.get('DATABASE_ADDR')
DATABASE_DEV = os.environ.get('DATABASE_DEV')
DATABASE_PROD = os.environ.get('DATABASE_PROD') 

if DATABASE_DEV:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{user}:{pwd}@{addr}/{db_dev}".format(
        user=DATABASE_USER,
        pwd=DATABASE_PASS,
        addr=DATABASE_ADDR,
        db_dev=DATABASE_DEV)
else:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{user}:{pwd}@{addr}/{db_prod}".format(
        user=DATABASE_USER,
        pwd=DATABASE_PASS,
        addr=DATABASE_ADDR,
        db_prod=DATABASE_PROD)

PAGINATION_PAGE_SIZE = 4
PAGINATION_PAGE_ARGUMENT_NAME = 'page'
