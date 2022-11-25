import datetime
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
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
    __tablename__ = "movement"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    date= db.Column(db.DateTime, default=datetime.datetime.now)
    movement_type = db.Column(db.String(1), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    detail = db.Column(db.String(500), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("member.membership_number"))
    member = db.relationship("Member")

    def resume(self):
        movements_types = {
            "S": "Saldo mes anterior",
            "I": "Intereses sobre el saldo",
            "D": "Débito",
            "C": "Crédito",
        }
        data = dict()
        data["date"] = self.date
        data["amount"] = self.amount
        data["detail"] = self.detail
        data["movement_type"] = movements_types[self.movement_type]
        return data