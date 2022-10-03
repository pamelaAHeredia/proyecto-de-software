from datetime import datetime

from src.models.database import db


# Define la clase Socio
class Member(db.Model):
    __tablename__ = "member"
    membership_number = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    document_type = db.Column(db.String(10), nullable=False)
    document_number = db.Column(db.String(10), nullable=False, unique=True)
    gender = db.Column(db.String(4), nullable=False)
    address = db.Column(db.String(100), nullable=False)  
    is_active = db.Column(db.Boolean, default=True)
    phone_number = db.Column(db.String(100))
    email = db.Column(db.String(50))
    creation_date = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)
   