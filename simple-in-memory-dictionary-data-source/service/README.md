Services
========

*http_status.py:*
Declares the status codes for the responses with an enumerable object.
An enumeration is a set of symbolic names (members) bound to unique, constant values. Within an enumeration, the members can be compared by identity, and the enumeration itself can be iterated over. [Here](https://docs.python.org/3/library/enum.html) you can find more details about the library.

*models.py:*
Contains a simple `NotificationModel` class used to represent notifications by just declaring the contructor. This model does not persist any data either to a database or to a file.

*service.py:*
Declares the `NotificationManager` object that is used to persist the `NotificationModel` instances in an in-memory dictionary. It also contains the CRUD (create, read, update, delete) methods that will be used by the Flask application.



