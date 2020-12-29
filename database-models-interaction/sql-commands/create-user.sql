CREATE USER IF NOT EXISTS 'pyuser'@'localhost' IDENTIFIED BY 'Py@pp4Demo';

GRANT ALL PRIVILEGES ON flask_notifications.* TO 'pyuser'@'localhost';
GRANT ALL PRIVILEGES ON test_flask_notifications.* TO 'pyuser'@'localhost';
