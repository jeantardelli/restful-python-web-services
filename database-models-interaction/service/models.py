"""
This module contains the instances that will be used to represent and persist
the notification categories, notifications and their relationship in the MySQL
database.
"""
from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class ResourceAddUpdateDelete:

    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

class Notification(db.Model, ResourceAddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(250), unique=True, nullable=False)
    ttl = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.TIMESTAMP,
                               server_default=db.func.current_timestamp(),
                               nullable=False)
    notification_category_id = db.Column(db.Integer,
            db.ForeignKey('notification_category.id', ondelete='CASCADE'),
            nullable=False)
    notification_category = db.relationship('NotificationCategory',
            backref=db.backref('notifications', lazy='dynamic',
            order_by='Notificatoin.message'))
    displayed_times = db.Column(db.Integer, nullable=False, server_default='0')
    displayed_once = db.Column(db.Boolean, nullable=False, server_default='false')

    def __init__(self, message, ttl, notification_category):
        self.message = message
        self.ttl = ttl
        self.notification_category = notification_category

class NotificationCategory(db.Model, ResourceAddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
