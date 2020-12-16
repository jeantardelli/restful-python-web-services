"""
This module declares variables that determine the configuration for Flask and SQLAlchemy.
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
DATABASE_USER = os.environ.get('DB_USER')
DATABASE_PASS = os.environ.get('DB_PASS')
DATABASE_ADDR = os.environ.get('DB_ADDR')
DATABASE_DEV = os.environ.get('DB_DEV')
DATABASE_PROD = os.environ.get('DB_PROD') 

if not DATABASE_DEV:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{user}:{pwd}@{addr}/{db_dev}".format(
        user=Config.DATABASE_USER,
        pwd=Config.DATABASE_PASS,
        addr=Config.DATABASE_ADDR,
        db_dev=Config.DATABASE_DEV)
else:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{user}:{pwd}@{addr}/{db_prod}".format(
        user=Config.DATABASE_USER,
        pwd=Config.DATABASE_PASS,
        addr=Config.DATABASE_ADDR,
        db_prod=Config.DATABASE_PROD)
