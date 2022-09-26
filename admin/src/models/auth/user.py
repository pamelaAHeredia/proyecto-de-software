from enum import unique
from src.models.database import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    active = db.Column(db.)