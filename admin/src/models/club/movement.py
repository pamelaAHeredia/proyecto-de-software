import datetime
from src.models.database import db


class Movement(db.Model):
    """
    Clase que representa los movimientos

    Atributos
    ---------
    date : Date
        Indica la fecha del movimiento
    is_credit : Boolean
        Indica si el movimiento es de credito(true) o debito(false).
    amount : Int
        Indica el monto del movimiento.
    """

    id = db.Column(db.Integer, primary_key=True, unique=True)
    date= db.Column(db.DateTime, default=datetime.datetime.now)
    is_credit = db.Column(db.Boolean, default=True)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    suscription_id = db.Column(db.Integer, db.ForeignKey("suscription.id"))
    suscription = db.relationship("Suscription")