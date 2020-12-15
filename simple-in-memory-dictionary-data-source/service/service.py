"""
This module contains the NotificationManager object that is used to persist the
NotificationModel instances in an in-memory dictionary. It also contains the
CRUD (create, read, update, delete) methods that will be used by the application.
"""
from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime
from models import NotificationModel
from http_status import HttpStatus
from pytz import utc

class NotificationManager():
    """This object will be the manager that persist the NotificationInstance
    in an in-memory dictionary"""
    last_id = 0

    def __init__(self):
        self.notifications = {}

    def insert_notification(self, notification):
        """Insert a Nofitication into an in-memory dictionary.

        Receives a recently created NotificationModel instance in the
        notification argument, increase the value for the last_id attribute
        and the assigns the resulting value to the ID for the received
        notification.

        Args:
            notification (NotificationModel): A NotificationModel instance
        """
        self.__class__.last_id += 1
        notification.id = self.__class__.last_id
        self.notifications[self.__class__.last_id] = notification

    def get_notification(self, id):
        """Gets a Notification by its id.

        Receives the id of the notification that has to be retrieved from the
        self.notifications dictionary.

        Args:
            id (int): Notifications dictionary id
        Returns:
            A NofiticationModel instance
        """
        return self.notifications[id]

    def delete_notification(self, id):
        """Deletes a Notification from an in-memory dictionary.

        Receives the id of the notification that has to be removed
        from the self.notifications dictionary.

        Args:
            id (int): Integer key number of the notifications dictionary
        """
        del self.notifications[id]

notification_fields = {
    'id': fields.Integer,
    'uri': fields.Url('notification_endpoint'),
    'message': fields.String,
    'ttl': fields.Integer,
    'creation_date': fields.DateTime,
    'notification_category': fields.String,
    'displayed_times': fields.Integer,
    'displayed_once': fields.Boolean
}

notification_manager = NotificationManager()

class Notification(Resource):
    """Represents the notification resource of the Flask-RESTful API

    Is a subclass of the flask_restful.Resource superclass and declares
    the following three methods that will be called when HTTP method with
    the same name arrives as a request on the represented resource."""
    def abort_if_notification_not_found(self, id):
        """Receives the id for an existing NotificationModel instance in the
        id argument.

        It the received id is not in the keys of the NoticationManager
        dictionary, the method class the flask_restful abort function with
        HTTP not found status code (404) and a message indicating that the
        notification with the specified id doesn't exist.

        Args:
            id (int): NotificationManager.notifications id key
        """
        if id not in notification_manager.notifications:
            abort(
                HttpStatus.not_found_404.value,
                message="Notification {0} not found".format(id))

    @marshal_with(notification_fields)
    def get(self, id):
        """Retreives the resource with a particular id argument.

        The code calls the self.abort_if_notification_not_found method to
        abort in case there is no notification with the requested ID.

        Args:
            id (int): Notification id key
        Returns:
            Notificaion object
        """
        self.abort_if_notification_not_found(id)
        return notification_manager.get_notification(id)

    def delete(self, id):
        """Deletes the resource with a particular id argument.

        The code calls the self.abort_if_notification_not_found method to
        abort in case there is no notification with the requested ID.

        Args:
            id (int): Notification id key
        Returns:
            tuple pair with empty strings and the HTTP no content status code
        """
        self.abort_if_notification_not_found(id)
        notification_manager.delete_notification(id)
        return '', HttpStatus.no_content_204.value

    @marshal_with(notification_fields)
    def patch(self, id):
        """Updates or patches the resource with a particar id argument

        The code calls the self.abort_if_notification_not_found method to
        abort in case there is no notification with the requested ID.

        The RequestParser instance allows to add arguments with their names
        and types and then easily parse the arguments received with the
        request (parser.add_argument). Then the code calls the method
        parser.parse_args to parse all the arguments from the request.

        Args:
            id (int): Notification id key
        Returns:
            Notificaion object
        """
        self.abort_if_notification_not_found(id)
        notification = notification_manager.get_notification(id)
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str)
        parser.add_argument('ttl', type=int)
        parser.add_argument('displayed_times', type=int)
        parser.add_argument('displayed_once', type=bool)
        args = parser.parse_args()
        print(args)
        if 'message' in args and args['message'] is not None:
            notification.message = args['message']
        if 'ttl' in args and args['ttl'] is not None:
            notificatin.ttl = args['ttl']
        if 'displayed_times' in args and args['displayed_times'] is not None:
            notification.displayed_times = args['displayed_times']
        if 'displayed_once' in args and args['displayed_once'] is not None:
            notification.displayed_once = args['displayed_once']
        return notification

class NotificationList(Resource):
    """Represents the collection of notifications (resources)

    This class is a subclass of the flask_restful.Resource superclass and
    declares the following two methods that will be called when the HTTP method
    with the same name arrives as a request on the resource."""
    @marshal_with(notification_fields)
    def get(self):
        """Returns a list with all the NotificationModel instances saved
        in the notification_manager.notifications dictionary.

        The marshal_with decorator will take each NotificationModel instance
        in the returned list and apply the field filtering and output
        formatting specified in notification_fields.

        Returns:
           List of Notifications (resources)
        """
        return [v for v in notification_manager.notifications.values()]

    @marshal_with(notification_fields)
    def post(self):
        """Creates a flask_restful.reqparse.RequestParser instance named parser.

        This allows to add arguments with their names and types and then easily
        parse the arguments with the POST request to create new NotificaionModel
        instance.

        Returns:
           A tuple composed of the inserted NotificaionModel instance and a 201
           created HTTP status code.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('message', type=str, required=True,
                            help='Message cannot be blank!')
        parser.add_argument('ttl', type=int, required=True,
                            help='Time to live cannot be blank!')
        parser.add_argument('notification_category', type=str, required=True,
                            help='Notification category cannot be blank!')
        args = parser.parse_args()
        notification = NotificationModel(
            message=args['message'],
            ttl=args['ttl'],
            creation_date=datetime.now(utc),
            notification_category=args['notification_category']
            )
        notification_manager.insert_notification(notification)
        return notification, HttpStatus.created_201.value

app = Flask(__name__)
service = Api(app)
service.add_resource(NotificationList, '/service/notifications/')
service.add_resource(Notification, '/service/notifications/<int:id>',
                     endpoint='notification_endpoint')

if __name__ == '__main__':
    app.run(debug=True)
