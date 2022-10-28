import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import and_

from src.models.database import db
from src.models.club.movement import Movement
from src.models.club.member import Member
from src.models.club.suscription import Suscription
from src.services.settings import SettingsService

TODAY = datetime.date.today()

DATE_TO = datetime.date.today() + datetime.timedelta(days=1)
DATE_FROM = DATE_TO.replace(day=1)


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

    def _last_month_day(self, day: datetime.date) -> datetime.date:
        next_month = day.replace(day=28) + datetime.timedelta(days=4)
        return next_month - datetime.timedelta(days=next_month.day)

    def is_defaulter(
        self,
        member: Member,
        date_from: datetime.date = TODAY,
    ) -> bool:
        """Retorna si es moroso.

        Dado un Socio retorna si es deudor al día solicitado.

        Args:
            member (Member): Un socio
            date (datetime.date, optional): Fecha solicitada. Por defecto TODAY.

        Returns:
            Bool: True es moroso.
        """
        if date_from.day <= 10:
            member_movements = member.movements.filter(
                and_(
                    Movement.movement_type.in_(["S", "I", "C"]),
                    Movement.date.between(
                        date_from.replace(day=1), date_from.replace(day=11)
                    ),
                )
            ).all()
        else:
            member_movements = member.movements.filter(
                Movement.date.between(
                    date_from.replace(day=1), date_from + datetime.timedelta(days=1)
                )
            ).all()
       
        return True if sum(move.amount for move in member_movements) < 0 else False

    def get_balance(
        self,
        member: Member,
        date_from: datetime.date = DATE_FROM,
        date_to: datetime.date = DATE_TO,
    ) -> Decimal:
        """Retorna el balance.

        Dado un Socio retorna el balance de su cuenta
        al día de la fecha.

        Args:
            member (Member): Un socio
            date_from (datetime.date, optional): Fecha desde. Por defecto DATE_FROM.
            date_to (datetime.date, optional): Fecha hasta. Por defecto DATE_TO.

        Returns:
            Decimal: Monto del balance de cuenta
        """
        member_movements = member.movements.filter(
            Movement.date.between(date_from, date_to)
        ).all()
        return sum(move.amount for move in member_movements)

    def generate_mensual_payments(self, member: Member, month: int, year: int):
        date_from = datetime.date(year, month - 1, 1)
        date_to = self._last_month_day(date_from)
        previous_balance = self.get_balance(member=member)

        movements_for_add = list()

        residue_movement = self.residue(previous_balance, "Saldo mes anterior", member)
        interest_movement = self.interest(
            previous_balance, "Interes saldo mes anterior", member
        )

        movements_for_add.append(residue_movement)
        movements_for_add.append(interest_movement)

        for suscription in member.active_suscriptions:
            debit_movement = self.debit(
                suscription.amount, f"Debito {suscription.membership.name}", member
            )
            movements_for_add.append(debit_movement)

        db.session.add_all(movements_for_add)
        db.session.commit()

    def debit(self, amount, detail, member):
        movement = self._insert_movement(
            movement_type="D",
            amount=amount * -1,
            detail=detail,
            member=member,
        )
        return movement

    def credit(self, amount, detail, member):
        movement = self._insert_movement(
            movement_type="C",
            amount=amount,
            detail=detail,
            member=member,
        )
        return movement

    def residue(self, amount, detail, member):
        movement = self._insert_movement(
            movement_type="S",
            amount=amount,
            detail=detail,
            member=member,
        )
        return movement

    def interest(self, amount, detail, member):
        interest = self._settings_service.get_percentage_surcharge()
        movement = self._insert_movement(
            movement_type="I",
            amount=amount * Decimal(str((interest / 100))),
            detail=detail,
            member=member,
        )
        return movement

    def _insert_movement(self, movement_type, amount, detail, member):
        movement = Movement(
            movement_type=movement_type,
            amount=amount,
            detail=detail,
            member=member,
        )
        return movement
