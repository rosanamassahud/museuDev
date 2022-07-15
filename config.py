import os

SECRET_KEY = 'museu'

MYSQL_HOST = "localhost"
MYSQL_USER = "manager"
MYSQL_PASSWORD = "manager"
MYSQL_DB = "museu"
MYSQL_PORT = 3306
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
