"""
This module contains the NotifcationModel class that will be used to represent
notifications. This model won't be persisting data in any database or file. It
just provides the required attributes and no mapping information.
"""
class NotificationModel:
    """Represents all the necessary attributes to an RESTful in-memory API"""
    def __init__(self, message, ttl, creation_date, notification_category):
        # Id will be automatically generated
        self.id = 0
        self.message = message
        self.ttl = ttl
        self.creation_date = creation_date
        self.notification_category = notification_category
        self.displayed_times = 0
        self.displayed_once = False
