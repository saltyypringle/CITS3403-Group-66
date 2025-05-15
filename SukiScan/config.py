import os

basedir = os.path.abspath(os.path.dirname(__file__))
default_database_location = 'sqlite:///' + os.path.join(basedir, 'data', 'sukiscan.db')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or default_database_location
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'SukiScan'

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = default_database_location
    TESTING = True
    WTF_CSRF_ENABLED = False