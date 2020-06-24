import os


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = [
        "access",
        "refresh",
    ]



class DevelopmentConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'riodosul'
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_DEV_URL")


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
