import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

#Silent the TRACK_MODIFICATIONS warning
SQLALCHEMY_TRACK_MODIFICATIONS = False 

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://ali:123@localhost:5432/fyyur'
