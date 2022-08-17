import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# TODO IMPLEMENT DATABASE URL

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT=  os.getenv('DB_PORT',5432)
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '7y8a1h64')
DB_NAME = os.getenv('DB_NAME', 'fyyurdb')

SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_TRACK_MODIFICATIONS  = False;
