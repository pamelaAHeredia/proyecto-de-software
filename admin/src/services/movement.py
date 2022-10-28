from calendar import month
from decimal import Decimal
from typing import List, Optional
import datetime


from src.models.database import db
from src.models.club.movement import Movement
from src.models.club.suscription import Suscription
from src.services.settings import SettingsService


class MovementService:
    """
    Clase que representa los servicios para el manejo de movimientos.
    """

    _instance = None
    _settings_service = SettingsService()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MovementService, cls).__new__(cls)
        return cls._instance

    # def get_balance(self, member_id):
    #     """Retorna el saldo.

    #     Arguments:
    #         member_id (int): Id del miembro del cual se desea conocer el saldo.

    #     Returns:
    #         int: El saldo, puede ser positivo si es que no debe o negativo si debe
    #     """
    #     movements = Movement.query.filter(date.month==datetime.datetime.now.month)
    #     if (movements is None):
    #         now = datetime.datetime.now
    #         movements = Movement.query.filter(date.month== (now + dateutil.relativedelta.relativedelta(months=-1))
    #         aux = 0
    #         for movement in movements
    #             aux += movement.amount
    #         return aux
    #     else:
    #         aux = 0
    #         for movement in movements
    #             aux += movement.amount
    #         return aux

    def insert_movement(self, movement_type, amount, detail, m):
        movement = Movement(
            movement_type=movement_type,
            amount=amount,
            detail=detail,
            member=m,
        )
        return movement

        # if (type=="Debito" and datetime.datetime.now().day==1 and not is_inscription):
        #     movements = Movement.query.filter_by(date.month = (now + dateutil.relativedelta.relativedelta(months=-1).month), date.year = (now + dateutil.relativedelta.relativedelta(months=-1).year)
        #     aux = 0
        #     for movement in movements
        #         aux += movement.amount
        #     saldo = Movement(datetime.datetime.now,"Saldo",aux,member_id)
        #     newMovement = Movement(datetime.datetime.now,"Debito",(amount*-1),member_id)
        #     db.session.add_all([saldo,newMovement])
        #     db.session.commit()
        # else:
        #     if (type=="Debito" and is_inscription):
        #         newDebito = Movement(datetime.datetime.now,"Debito",(amount*-1),member_id)
        #         newCredito = Movement(datetime.datetime.now,"Credito",amount,member_id)
        #         db.session.add_all([newDebito,newCredito])
        #         db.session.commit()
        #     else:
        #         if (type=="Credito" and)
        #         # Como aplicar en un credito, el interes? tipo si quisiera saber cuanto debo antes de pagar, me va a decir un saldo, y despues si cuando pago se aplica interes, estare pagando algo distinto
        #         # Debo tener dos If de Credito, uno antes del 10 y otro despues del 10 para lo de interes que todavia no se aplicar
        
        