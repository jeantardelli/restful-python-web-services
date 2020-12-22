"""
This module contains the instances that will be used to represent and persist
the users, the notification categories, the notifications and their relationship 
in the MySQL database.
"""
import re

from marshmallow import Schema, fields, pre_load
from marshmallow import validate

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from passlib.apps import custom_app_context as password_context

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

class User(db.Model, ResourceAddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique= True, nullable=False)
    password_hash = db.Column(db.String(20), nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        nullable=False)

    def verify_password(self, password):
        return password_context.verify(password, self.password_hash)

    def check_password_strength_and_hash_if_ok(self, password):
        if len(password) < 8:
            return 'The password is too short. Please, specify a password with'\
                    ' at least 8 characters.', False
        if len(password) > 32:
            return 'The password is too long. Please, specify a password with '\
                    'no more than 32 characters.', False
        if re.search(r'[A-Z]', password) is None:
            return 'The password must include at least one lowercase letter.',\
                    False
        if re.search(r'[a-z]', password) is None:
            return 'The password must include at least one lowercase letter.',\
                    False
        if re.search(r'\d', password) is None:
            return 'The password must include at least one Number.', False
        if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None:
            return 'The password must include at least one symbol.', False

        # Save the hash for the password and not the actual one
        self.password_hash = password_context.hash(password)

        return '', True

    def __init__(self, name):
        self.name = name

class Notification(db.Model, ResourceAddUpdateDelete):
    id = db.Column(db.Integer,primary_key=True)
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
        order_by='Notification.message'))
    displayed_times = db.Column(db.Integer, nullable=False,
        server_default='0')
    displayed_once = db.Column(db.Boolean, nullable=False,
        server_default='0')

    def __init__(self, message, ttl, notification_category):
        self.message = message
        self.ttl = ttl
        self.notification_category = notification_category

    def __repr__(self):
        return '<Notification %r>' % self.message

    @classmethod
    def is_message_unique(cls, id, message):
        existing_notification = cls.query.filter_by(message=message).first()
        if existing_notification is None:
            return True
        else:
            if existing_notification.id == id:
                return True
            else:
                return False

class NotificationCategory(db.Model, ResourceAddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<NotificationCategory %r>' % self.name

    @classmethod
    def is_name_unique(cls, id, name):
        existing_notification_category = cls.query.filter_by(name=name).first()
        if existing_notification_category is None:
            return True
        else:
            if existing_notification_category.id == id:
                return True
            else:
                return False

class NotificationCategorySchema(ma.Schema):
    id = fields.Integer(dump_only=3)
    name = fields.String(required=True, validate=validate.Length(3))
    url = ma.URLFor(
        'service.notificationcategoryresource',
        id='<id>',
        _external=True)
    notifications = fields.Nested(
        'NotificationSchema',
        many=True,
        exclude=('notification_category',))

class NotificationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    message = fields.String(required=True, validate=validate.Length(5))
    ttl = fields.Integer()
    creation_date = fields.DateTime()
    notification_category = fields.Nested(
        NotificationCategorySchema,
        only=['id', 'url', 'name'],
        required=True)
    displayed_times = fields.Integer()
    displayed_once = fields.Boolean()
    url = ma.URLFor(
        'service.notificationresource',
        id='<id>',
        _external=True)

    @pre_load
    def process_notification_category(self, data):
        notification_category = data.get('notification_category')
        if notification_category:
            if isinstance(notification_category, dict):
                notification_category_name = notification_category.get('name')
            else:
                notification_category_name = notification_category
            notification_category_dict = dict(name=notification_category_name)
        else:
            notification_category_dict = {}
        data['notification_category'] = notification_category_dict
        return data
