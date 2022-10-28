from os import environ
from datetime import timedelta


class Config(object):
    """Base configuration."""

    SECRET_KEY = "98c5125f7de55305fdfc720090eddf11b2e587e83731235604dae5adef1d3a0c2c07b512b313da43d418133947d7f9f3373980c17c0786ce5147bdf2e798da7f"
    DEBUG = False
    TESTING = False
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15) 
    SESSION_TYPE = "filesystem"

class ProductionConfig(Config):
    """Production configuration."""

    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )
    # Sesion valores
    SESSION_TYPE = "filesystem"
    SESSION_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    """Development configuration."""

    # Valores de la DB
    DEBUG = True
    DB_USER = environ.get("DB_USER", "postgres")
    DB_PASS = environ.get("DB_PASS", "postgres")
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_NAME = environ.get("DB_NAME", "club")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )
    # Sesion valores
    SESSION_TYPE = "filesystem"


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True


config = {
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "production": ProductionConfig,
}
