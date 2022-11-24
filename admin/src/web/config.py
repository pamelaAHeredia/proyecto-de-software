from os import environ
import secrets
from datetime import timedelta


class Config(object):
    """Base configuration."""
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.jpeg']
    SECRET_KEY = secrets.token_urlsafe(32)
    DEBUG = False
    TESTING = False
    SESSION_PERMANENT = True
    SESSION_TYPE = "filesystem"
    WTF_CSRF_TIME_LIMIT = 120

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
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
    PORTAL_URL = "https://grupo06.proyecto2022.linti.unlp.edu.ar"
    ADMIN_URL = "https://admin-grupo06.proyecto2022.linti.unlp.edu.ar"
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
    PORTAL_URL = ["http://127.0.0.1:5173", "http://localhost:5173"]
    ADMIN_URL = ["http://127.0.0.1:5000", "http://localhost:5000"]

class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True


config = {
    "development": DevelopmentConfig,
    "test": TestingConfig,
    "production": ProductionConfig,
}
