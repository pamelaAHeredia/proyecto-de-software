from datetime import datetime

from src.models.database import db


# Define la clase Socio
class Member(db.Model):
    __tablename__ = "member"
    __table_args__ = (
        db.UniqueConstraint(
            "document_type", "document_number", name="unique_member_document"
        ),
    )
    membership_number = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(75), nullable=False)
    last_name = db.Column(db.String(75), nullable=False)
    document_type = db.Column(db.String(10), nullable=False)
    document_number = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(4), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    phone_number = db.Column(db.String(100))
    email = db.Column(db.String(50))
    creation_date = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User")
    suscriptions = db.relationship(
        "Suscription", back_populates="member", lazy="dynamic"
    )

    def __init__(
        self,
        first_name,
        last_name,
        document_type,
        document_number,
        gender,
        address,
        phone_number,
        email,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.document_type = document_type
        self.document_number = document_number
        self.gender = gender
        self.address = address
        self.phone_number = phone_number
        self.email = email

    @property
    def username(self):
        if self.user:
           return self.user.username
        return None   