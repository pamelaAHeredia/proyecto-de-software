from calendar import month
from decimal import Decimal
from typing import List, Optional
import datetime

from sqlalchemy import and_


from src.models.database import db
from src.models.club.movement import Movement
from src.models.club.member import Member
from src.models.club.suscription import Suscription
from src.services.settings import SettingsService
from src.errors.database import MinValueValueError
from src.services.paginator import Paginator

TODAY = datetime.date.today()
DATE_FROM = TODAY.replace(day=1)


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
        date_to: datetime.date = TODAY,
        specific_date: datetime.date = None,
        all: bool = False,
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
        if specific_date:
            member_movements = member.movements.filter(
                and_(
                    Movement.date.between(
                        specific_date.replace(day=1),
                        specific_date + datetime.timedelta(days=1),
                    ),
                    ~Movement.movement_type.in_(["S"]),
                )
            ).all()
            return sum(move.amount for move in member_movements)
        if all:
            member_movements = member.movements.filter(
                ~Movement.movement_type.in_(["S"])
            ).all()
            return sum(move.amount for move in member_movements)

        member_movements = member.movements.filter(
            Movement.date.between(date_from, date_to + datetime.timedelta(days=1))
        ).all()
        return sum(move.amount for move in member_movements)

    def get_movements(
        self,
        member: Member,
        specific_date: datetime.date = None,
        movement_type: str = None
    ) -> List[Movement]:
        """Retorna los movimientos.

        Dado un Socio retorna los movimiento de su cuenta
        al día de la fecha dada.

        Args:
            member (Member): Un socio
            specific_date (datetime.date, optional): Fecha hasta. Por defecto TODAY.

        Returns:
            list[Movement]: Lista de movimientos.
        """
        # member_movements = member.movements.filter(
        #     Movement.date.between(
        #         specific_date.replace(day=1),
        #         specific_date + datetime.timedelta(days=1),
        #     )
        # ).order_by(Movement.date)
        if movement_type and not specific_date:
            member_movements = member.movements.filter(
                Movement.movement_type == movement_type
            ).order_by(Movement.date)
        elif not movement_type and specific_date:
            member_movements = member.movements.filter(
                Movement.date.between(
                    specific_date.replace(day=1),
                    specific_date + datetime.timedelta(days=1),
                )
            ).order_by(Movement.date)
        else:
            member_movements = member.movements.order_by(Movement.date)
        return member_movements

    def list_paginated_movements(
        self, page: int, items_per_page: int, endpoint: str, member: Member
    ) -> Paginator:
        """Retorna un paginador con las disciplinas.

        Args:
            page (int): Numero de pagina.
            items_per_page (int): cantidad de registros por página.
            endpoint (str): endpoint para el armado del url_for.

        Returns:
            Paginator: Un paginador.
        """
        movements = self.get_movements(member)
        return Paginator(
            movements,
            page,
            items_per_page,
            endpoint,
            member_id=member.membership_number,
        )

    def generate_mensual_payments(self, member: Member, month: int, year: int):
        movement_date = datetime.datetime(year, month, 1, 0, 0, 0)
        month, year = (12, year - 1) if month == 1 else (month - 1, year)
        date_from = datetime.date(year, month, 1)
        date_to = self._last_month_day(date_from)
        print(date_from, date_to)

        previous_balance = self.get_balance(
            member=member, date_from=date_from, date_to=date_to
        )

        movements_for_add = list()

        residue_movement = self.residue(
            previous_balance, "Saldo mes anterior", member, movement_date=movement_date
        )
        interest_movement = self.interest(
            previous_balance if previous_balance < 0 else 0,
            "Interes saldo mes anterior",
            member,
            movement_date=movement_date,
        )

        movements_for_add.append(residue_movement)
        movements_for_add.append(interest_movement)

        for suscription in member.active_suscriptions:
            debit_movement = self.debit(
                suscription.amount,
                f"Debito {suscription.membership.name}",
                member,
                movement_date=movement_date,
            )
            movements_for_add.append(debit_movement)

        db.session.add_all(movements_for_add)
        db.session.commit()

    def debit(self, amount, detail, member, movement_date=None, with_commit=False):
        movement = self.insert_movement(
            movement_type="D",
            amount=amount if amount < 0 else amount * -1,
            detail=detail,
            member=member,
            movement_date=movement_date,
            with_commit=with_commit,
        )
        return movement

    def credit(self, amount, detail, member, movement_date=None, with_commit=False):
        movement = self.insert_movement(
            movement_type="C",
            amount=amount * -1 if amount < 0 else amount,
            detail=detail,
            member=member,
            movement_date=movement_date,
            with_commit=with_commit,
        )
        return movement

    def residue(self, amount, detail, member, movement_date=None, with_commit=False):
        movement = self.insert_movement(
            movement_type="S",
            amount=amount,
            detail=detail,
            member=member,
            movement_date=movement_date,
            with_commit=with_commit,
        )
        return movement

    def interest(self, amount, detail, member, movement_date=None, with_commit=False):
        interest = self._settings_service.get_percentage_surcharge()
        movement = self.insert_movement(
            movement_type="I",
            amount=amount * Decimal(str((interest / 100))),
            detail=detail,
            member=member,
            movement_date=movement_date,
            with_commit=with_commit,
        )

        return movement

    def insert_movement(
        self,
        movement_type,
        amount,
        detail,
        member,
        movement_date=datetime.datetime.now(),
        with_commit: bool = False,
    ):
        movement = Movement(
            date=movement_date,
            movement_type=movement_type,
            amount=amount,
            detail=detail,
            member=member,
        )
        if with_commit:
            db.session.add(movement)
            db.session.commit()
        return movement


    def api_member_movements(self, member, specific_date):
        data = dict()
        movements = self.get_movements(member=member, specific_date=specific_date)
        data["movements"] = [m.resume() for m in movements]
        return data