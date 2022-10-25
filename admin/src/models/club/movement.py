import datetime
from src.models.database import db


class Movement(db.Model):
    """
    Clase que representa los movimientos

    Atributos
    ---------
    date : Date
        Indica la fecha del movimiento
    type : String
        El tipo de movimiento que es.
    amount : Int
        Indica el monto del movimiento.
    """

    id = db.Column(db.Integer, primary_key=True, unique=True)
    date= db.Column(db.DateTime, default=datetime.datetime.now)
    type = db.Column(db.String(4), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("member.membership_number"))
    member = db.relationship("Member")