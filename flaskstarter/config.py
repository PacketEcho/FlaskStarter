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
    TESTING = False
    DEBUG = True


class ProductionConfig(Config):
    CACHE_TYPE = "simple"

    TESTING = False
    DEBUG = False

    DB_USER = os.environ.get('POSTGRES_USER')
    DB_PASS = os.environ.get('POSTGRES_PASSWORD')
    DB_HOST = os.environ.get('POSTGRES_HOST')
    DB_PORT = os.environ.get('POSTGRES_PORT') or 5432
    DB_NAME = os.environ.get('POSTGRES_DB')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'