import datetime
from src.models.database import db


class Tariff(db.Model):
    """
    Clase usada para representar un Arancel

    Atributos
    ---------
    name : str

    is_active : Boolean
        Indica si la disciplina esta activa para la inscripción.
    deleted : Boolean
        Indica si la disciplina se sigue dando o no.
    """
    __tablename__ = "tariff"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date_from = db.Column(db.DateTime, default=datetime.datetime.now)
    date_to = db.Column(db.DateTime, nullable=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    membership_id = db.Column(db.Integer, db.ForeignKey("membership.id"))
    membership = db.relationship("Membership")
