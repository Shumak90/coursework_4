import base64
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = "qwerty_test"
    JSON_AS_ASCII = False

    ITEMS_PER_PAGE = 12

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET = 'test_123'
    JWT_ALGORITHM = 'HS256'
    TOKEN_EXPIRE_MINUTES = 15
    TOKEN_EXPIRE_DAYS = 130

    PWD_HASH_SALT = base64.b64decode("salt")
    PWD_HASH_ITERATIONS = 100_000


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        os.path.dirname(BASEDIR), "project/data/movies.db"
    )
    SQLALCHEMY_BINDS = {
        'users': "sqlite:///" + os.path.join(
        os.path.dirname(BASEDIR), "project/data/users.db")
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_JSON = {'ensure_ascii': False, 'indent': 2}
