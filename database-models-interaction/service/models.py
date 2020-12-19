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

class NotificationCategory(db.Model, ResourceAddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<NotificationCategory %r>' % self.name

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
