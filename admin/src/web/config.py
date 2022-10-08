from os import environ


class Config(object):
    """Base configuration."""

    SECRET_KEY = "secret"
    DEBUG = False
    TESTING = False


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
