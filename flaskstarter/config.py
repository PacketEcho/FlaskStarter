import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://app.sqlite'


class TestConfig(Config):
    TESTING = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    CACHE_TYPE = "simple"
